#!/usr/bin/env python3

from khsprcexport import exporters
import os
import sys
import argparse
import datetime

import khsprcexport.constants as constants
import khsprcexport.importers as importers
import khsprcexport.utils as utils


def _generate_pioneer_reports(output_dir, fsgs, publishers, fsrecords, json_output=False, pdf_output=True, pdf_template_file=None):
    # collect pioneer publisher ids
    pioneer_ids = utils.get_pioneers_ids(fsgs)
    # make pioneer report header
    pid_headers = {}
    for pid in pioneer_ids:
        pid_headers[pid] = utils.get_publisher_header(pid, publishers)
    # collect reports for pioneers in prc service years
    pioneer_service_reports = utils.get_reports(pioneer_ids, fsrecords)
    # create reports
    output_dir = os.path.join(output_dir, 'active', 'pioneers')
    reports_by_pid = {}
    for pr in pioneer_service_reports:
        if pr['publisher_id'] not in reports_by_pid.keys():
            header = utils.get_publisher_header(pr['publisher_id'], publishers)
            reports_by_pid[pr['publisher_id']] = {
                'header': header,
                'reports': []
            }
        reports_by_pid[pr['publisher_id']]['reports'].append(pr)
    for pid in reports_by_pid.keys():
        reports_by_pid[pid]['summary'] = utils.get_reports_totals_avgs(
            reports_by_pid[pid]['reports'])
    if json_output:
        os.makedirs(output_dir, exist_ok=True)
        # write out json pioneer reports
        for r in reports_by_pid.keys():
            report_out_file = "%s.json" % reports_by_pid[r]['header']['file_name_prefix']
            report_out_path = os.path.join(
                output_dir, report_out_file)
            exporters.write_json_file(report_out_path, reports_by_pid[r])
    if pdf_output:
        os.makedirs(output_dir, exist_ok=True)
        # write out S-21 pdf
        for r in reports_by_pid.keys():
            report_out_file = "%s.pdf" % reports_by_pid[r]['header']['file_name_prefix']
            report_out_path = os.path.join(
                output_dir, report_out_file)
            exporters.write_pdf_file(
                report_out_path, reports_by_pid[r], pdf_template_file)
    return pioneer_ids


def _generate_inactive_reports(output_dir, fsgs, publishers, fsrecords, json_output=False, pdf_output=True, pdf_template_file=None):
    # collect inactive publisher ids
    inactive_ids = utils.get_inactive_ids(fsrecords)
    # colect reports for inactive in prc service years
    inactive_service_reports = utils.get_reports(inactive_ids, fsrecords)
    # create reports
    output_dir = os.path.join(output_dir, 'inactive')
    reports_by_pid = {}
    for pr in inactive_service_reports:
        if pr['publisher_id'] not in reports_by_pid.keys():
            header = utils.get_publisher_header(pr['publisher_id'], publishers)
            reports_by_pid[pr['publisher_id']] = {
                'header': header,
                'reports': []
            }
        reports_by_pid[pr['publisher_id']]['reports'].append(pr)
    for pid in reports_by_pid.keys():
        reports_by_pid[pid]['summary'] = utils.get_reports_totals_avgs(
            reports_by_pid[pid]['reports'])
    if json_output:
        os.makedirs(output_dir, exist_ok=True)
        # write out json inactive reports
        for r in reports_by_pid.keys():
            report_out_file = "%s.json" % reports_by_pid[r]['header']['file_name_prefix']
            report_out_path = os.path.join(
                output_dir, report_out_file)
            exporters.write_json_file(report_out_path, reports_by_pid[r])
    if pdf_output:
        os.makedirs(output_dir, exist_ok=True)
        # write out S-21 pdf
        for r in reports_by_pid.keys():
            report_out_file = "%s.pdf" % reports_by_pid[r]['header']['file_name_prefix']
            report_out_path = os.path.join(
                output_dir, report_out_file)
            exporters.write_pdf_file(
                report_out_path, reports_by_pid[r], pdf_template_file)
    return inactive_ids


def _generate_fsg_reports(output_dir, fsgs, publishers, fsrecords, json_output=False, pdf_output=True, pdf_template_file=None):
    # collect pioneer publisher ids
    pioneer_ids = utils.get_pioneers_ids(fsgs)
    # collect inactive publisher ids
    inactive_ids = utils.get_inactive_ids(fsrecords)
    # create a list of field service group report objects
    fsg_pub_ids = {}
    for fsg in fsgs:
        # get publisher ids in this service group
        pub_ids = []
        for pub in fsg['publishers']:
            if (pub['id'] not in pioneer_ids) and (pub['id'] not in inactive_ids):
                pub_ids.append(pub['id'])
        # collect reports for this service group
        fsg_reports = utils.get_reports(pub_ids, fsrecords)
        # create reports
        fsg_output_dir = os.path.join(
            output_dir, 'active', utils.make_dir_name(fsg['name']))
        reports_by_pid = {}
        for pr in fsg_reports:
            if pr['publisher_id'] not in reports_by_pid.keys():
                reports_by_pid[pr['publisher_id']] = {
                    'header': utils.get_publisher_header(pr['publisher_id'], publishers),
                    'reports': []
                }
            reports_by_pid[pr['publisher_id']]['reports'].append(pr)
        for pid in reports_by_pid.keys():
            reports_by_pid[pid]['summary'] = utils.get_reports_totals_avgs(
                reports_by_pid[pid]['reports'])
        if json_output:
            os.makedirs(fsg_output_dir, exist_ok=True)
            for r in reports_by_pid.keys():
                report_out_file = "%s.json" % reports_by_pid[r]['header']['file_name_prefix']
                report_out_path = os.path.join(
                    fsg_output_dir, report_out_file)
                exporters.write_json_file(report_out_path, reports_by_pid[r])
        if pdf_output:
            os.makedirs(fsg_output_dir, exist_ok=True)
            for r in reports_by_pid.keys():
                report_out_file = "%s.pdf" % reports_by_pid[r]['header']['file_name_prefix']
                report_out_path = os.path.join(
                    fsg_output_dir, report_out_file)
                exporters.write_pdf_file(
                    report_out_path, reports_by_pid[r], pdf_template_file)
        fsg_pub_ids[fsg['id']] = pub_ids
    return fsg_pub_ids


def _generate_summary_reports(output_dir, fsgs, publishers, fsrecords, json_output=False, pdf_output=True, pdf_template_file=None):
    service_years = utils.get_service_years()
    # initial report data dictionaries
    pioneer_reports = utils.generate_dummy_report()
    pioneer_reports['header']['name'] = 'Pioneer Summary'
    pioneer_reports['header']['file_name_prefix'] = 'Pioneers'
    auxiliary_pioneer_reports = utils.generate_dummy_report()
    auxiliary_pioneer_reports['header']['name'] = 'Auxiliary Pioneer Summary'
    auxiliary_pioneer_reports['header']['file_name_prefix'] = 'AuxiliaryPioneers'
    publisher_reports = utils.generate_dummy_report()
    publisher_reports['header']['name'] = 'Auxiliary Pioneer Summary'
    publisher_reports['header']['file_name_prefix'] = 'Publishers'

    first_sy_month_indexes = {9: 0, 10: 1, 11: 2, 12: 3,
                              1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11}
    second_sy_month_indexes = {9: 12, 10: 13, 11: 14, 12: 15,
                               1: 16, 2: 17, 3: 18, 4: 19, 5: 20, 6: 21, 7: 22, 8: 23}

    for sr in fsrecords:
        if sr['service_year'] in service_years:
            month_index = 0
            if sr['service_year'] == service_years[0]:
                month_index = first_sy_month_indexes[sr['month']]
            if sr['service_year'] == service_years[1]:
                month_index = second_sy_month_indexes[sr['month']]
            if sr['pioneer']:
                rs = pioneer_reports['summary'][sr['service_year']]
                rs['total_placements'] = rs['total_placements'] + sr['placements']
                rs['total_video_showings'] = rs['total_video_showings'] + \
                    sr['video_showings']
                rs['total_hours'] = rs['total_hours'] + sr['hours']
                rs['total_return_visits'] = rs['total_placements'] + \
                    sr['placements']
                rs['total_studies'] = rs['total_placements'] + sr['placements']
                rs['number_of_reports'] = rs['number_of_reports'] + 1
                mr = pioneer_reports['reports'][month_index]
                mr['placements'] = mr['placements'] + sr['placements']
                mr['video_showings'] = mr['video_showings'] + sr['video_showings']
                mr['hours'] = mr['hours'] + sr['hours']
                mr['return_visits'] = mr['return_visits'] + sr['hours']
                mr['studies'] = mr['studies'] + sr['studies']
                if isinstance(mr['remarks'], str):
                    mr['remarks'] = 0
                mr['remarks'] = mr['remarks'] + 1
            elif sr['auxiliary_pioneer']:
                rs = auxiliary_pioneer_reports['summary'][sr['service_year']]
                rs['total_placements'] = rs['total_placements'] + sr['placements']
                rs['total_video_showings'] = rs['total_video_showings'] + \
                    sr['video_showings']
                rs['total_hours'] = rs['total_hours'] + sr['hours']
                rs['total_return_visits'] = rs['total_placements'] + \
                    sr['placements']
                rs['total_studies'] = rs['total_placements'] + sr['placements']
                rs['number_of_reports'] = rs['number_of_reports'] + 1
                mr = auxiliary_pioneer_reports['reports'][month_index]
                mr['placements'] = mr['placements'] + sr['placements']
                mr['video_showings'] = mr['video_showings'] + sr['video_showings']
                mr['hours'] = mr['hours'] + sr['hours']
                mr['return_visits'] = mr['return_visits'] + sr['hours']
                mr['studies'] = mr['studies'] + sr['studies']
                if isinstance(mr['remarks'], str):
                    mr['remarks'] = 0
                mr['remarks'] = mr['remarks'] + 1
            else:
                rs = publisher_reports['summary'][sr['service_year']]
                rs['total_placements'] = rs['total_placements'] + sr['placements']
                rs['total_video_showings'] = rs['total_video_showings'] + \
                    sr['video_showings']
                rs['total_hours'] = rs['total_hours'] + sr['hours']
                rs['total_return_visits'] = rs['total_placements'] + \
                    sr['placements']
                rs['total_studies'] = rs['total_placements'] + sr['placements']
                rs['number_of_reports'] = rs['number_of_reports'] + 1
                mr = publisher_reports['reports'][month_index]
                mr['placements'] = mr['placements'] + sr['placements']
                mr['video_showings'] = mr['video_showings'] + sr['video_showings']
                mr['hours'] = mr['hours'] + sr['hours']
                mr['return_visits'] = mr['return_visits'] + sr['hours']
                mr['studies'] = mr['studies'] + sr['studies']
                if isinstance(mr['remarks'], str):
                    mr['remarks'] = 0
                mr['remarks'] = mr['remarks'] + 1
    # calculate averages
    for sy in service_years:
        pioneer_reports['summary'][sy]['avg_placements'] = round(
            (pioneer_reports['summary'][sy]['total_placements'] / pioneer_reports['summary'][sy]['number_of_reports']), 2)
        pioneer_reports['summary'][sy]['avg_video_showings'] = round(
            (pioneer_reports['summary'][sy]['total_video_showings'] / pioneer_reports['summary'][sy]['number_of_reports']), 2)
        pioneer_reports['summary'][sy]['avg_hours'] = round(
            (pioneer_reports['summary'][sy]['total_hours'] / pioneer_reports['summary'][sy]['number_of_reports']), 2)
        pioneer_reports['summary'][sy]['avg_return_visits'] = round(
            (pioneer_reports['summary'][sy]['total_return_visits'] / pioneer_reports['summary'][sy]['number_of_reports']), 2)
        pioneer_reports['summary'][sy]['avg_studies'] = round(
            (pioneer_reports['summary'][sy]['total_studies'] / pioneer_reports['summary'][sy]['number_of_reports']), 2)
        auxiliary_pioneer_reports['summary'][sy]['avg_placements'] = round(
            (auxiliary_pioneer_reports['summary'][sy]['total_placements'] / auxiliary_pioneer_reports['summary'][sy]['number_of_reports']), 2)
        auxiliary_pioneer_reports['summary'][sy]['avg_video_showings'] = round(
            (auxiliary_pioneer_reports['summary'][sy]['total_video_showings'] / auxiliary_pioneer_reports['summary'][sy]['number_of_reports']), 2)
        auxiliary_pioneer_reports['summary'][sy]['avg_hours'] = round(
            (auxiliary_pioneer_reports['summary'][sy]['total_hours'] / auxiliary_pioneer_reports['summary'][sy]['number_of_reports']), 2)
        auxiliary_pioneer_reports['summary'][sy]['avg_return_visits'] = round(
            (auxiliary_pioneer_reports['summary'][sy]['total_return_visits'] / auxiliary_pioneer_reports['summary'][sy]['number_of_reports']), 2)
        auxiliary_pioneer_reports['summary'][sy]['avg_studies'] = round(
            (auxiliary_pioneer_reports['summary'][sy]['total_studies'] / auxiliary_pioneer_reports['summary'][sy]['number_of_reports']), 2)
        publisher_reports['summary'][sy]['avg_placements'] = round(
            (publisher_reports['summary'][sy]['total_placements'] / publisher_reports['summary'][sy]['number_of_reports']), 2)
        publisher_reports['summary'][sy]['avg_video_showings'] = round(
            (publisher_reports['summary'][sy]['total_video_showings'] / publisher_reports['summary'][sy]['number_of_reports']), 2)
        publisher_reports['summary'][sy]['avg_hours'] = round(
            (publisher_reports['summary'][sy]['total_hours'] / publisher_reports['summary'][sy]['number_of_reports']), 2)
        publisher_reports['summary'][sy]['avg_return_visits'] = round(
            (publisher_reports['summary'][sy]['total_return_visits'] / publisher_reports['summary'][sy]['number_of_reports']), 2)
        publisher_reports['summary'][sy]['avg_studies'] = round(
            (publisher_reports['summary'][sy]['total_studies'] / publisher_reports['summary'][sy]['number_of_reports']), 2)

    # clean up remarks labels
    for r in pioneer_reports['reports']:
        r['remarks'] = "%d reports" % r['remarks']
    for r in auxiliary_pioneer_reports['reports']:
        r['remarks'] = "%d reports" % r['remarks']
    for r in publisher_reports['reports']:
        r['remarks'] = "%d reports" % r['remarks']
    if json_output:
        os.makedirs(output_dir, exist_ok=True)
        report_out_file = "%s.json" % pioneer_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        exporters.write_json_file(report_out_path, pioneer_reports)
        report_out_file = "%s.json" % auxiliary_pioneer_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        exporters.write_json_file(report_out_path, auxiliary_pioneer_reports)
        report_out_file = "%s.json" % publisher_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        exporters.write_json_file(report_out_path, publisher_reports)
    if pdf_output:
        os.makedirs(output_dir, exist_ok=True)
        report_out_file = "%s.pdf" % pioneer_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        exporters.write_pdf_file(
            report_out_path, pioneer_reports, pdf_template_file)
        report_out_file = "%s.pdf" % auxiliary_pioneer_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        exporters.write_pdf_file(
            report_out_path, auxiliary_pioneer_reports, pdf_template_file)
        report_out_file = "%s.pdf" % publisher_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        exporters.write_pdf_file(
            report_out_path, publisher_reports, pdf_template_file)


'''
Parse command arguments and excute export workflow
'''


def main():
    ap = argparse.ArgumentParser(
        prog='create_publisher_record_cards',
        usage='%(prog)s.py [options]',
        description='reads KHS DBF files and creates S-21-E pdfs in a virtual card file',
    )
    ap.add_argument(
        '--khsdatadir',
        help='path to KHS data files',
        required=True
    )
    ap.add_argument(
        '--outputdir',
        help='path to output virtual card file',
        default='./prc_cardbox',
    )
    ap.add_argument(
        '--json',
        help='create reports json',
        action='store_true'
    )
    ap.add_argument(
        '--pdf',
        help='create S-21-E PDFs',
        action='store_true',
    )
    ap.add_argument(
        '--pdftemplate',
        help='S-21-E.pdf original PDF template file - default is ./templates/S-21_E.pdf',
        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates', 'S-21-E.pdf'),
        required=False
    )
    ap.add_argument(
        '--zip',
        help='create a zip archive the output folder',
        action='store_true'
    )
    ap.add_argument(
        '--zipfilename',
        help='the zip file to create',
        required=False,
        default='prcs-%s.zip' % datetime.datetime.now().isoformat()
    )

    args = ap.parse_args()

    required_files = [
        os.path.join(args.khsdatadir, constants.FSGROUP_FILE),
        os.path.join(args.khsdatadir, onstants.NAMES_FILE),
        os.path.join(args.khsdatadir, constants.FIELD_SERVICE_FILE)
    ]

    if args.pdf:
        required_files.append(args.pdftemplate)

    for file_path in required_files:
        if not os.path.exists(file_path):
            print("\nCan not find %s, a required file\n" % file_path)
            sys.exit(1)

    # load data from KHS data
    (fsgs, publishers, fsrecords) = importers.load_khs_data(args.khsdatadir)

    # generate the pionner PRC reports
    _generate_pioneer_reports(
        args.outputdir, fsgs, publishers, fsrecords, args.json, args.pdf, args.pdftemplate)
    # generate the inactive PRC reports
    _generate_inactive_reports(
        args.outputdir, fsgs, publishers, fsrecords, args.json, args.pdf, args.pdftemplate)
    # generate the fields service group reports
    _generate_fsg_reports(args.outputdir, fsgs, publishers,
                          fsrecords, args.json, args.pdf, args.pdftemplate)
    # generate the summary PRC reports
    _generate_summary_reports(args.outputdir, fsgs, publishers,
                              fsrecords, args.json, args.pdf, args.pdftemplate)
    # optionally zip up the reports
    if args.zip:
        utils.zipdir(args.zipfilename, args.outputdir)


'''
The script was executed from the CLI directly, run main function
'''
if __name__ == "__main__":
    main()
