#!/usr/bin/env python3

import os
import sys
import json
import argparse
import datetime
import dateutil.relativedelta as drd
import pypdftk
import zipfile

import create_field_service_groups_records as fsgs
import create_field_service_records as srs

FSGROUP_FILE = 'Fsgroups.DBF'
NAMES_FILE = 'Names.DBF'
FIELD_SERVICE_FILE = 'Field_service.DBF'

FSGS = None
FSRECS = None
PUBLISHERS = None

EXCLUDE_FSG_BY_NAME = []

PDF_TEMPLATE_FILE = None


def _write_json_file(file_name, objs):
    with open(file_name, 'w') as jf:
        jf.write(json.dumps(objs, indent=2))


def _write_pdf_file(file_name, objs):
    fill_data = {}
    fill_data['Name'] = objs['header']['name']
    fill_data['Date immersed'] = objs['header']['date_immersed']
    fill_data['Date of birth'] = objs['header']['date_of_birth']
    if objs['header']['male']:
        fill_data['Check Box1'] = 'Yes'
    if objs['header']['female']:
        fill_data['Check Box2'] = 'Yes'
    if objs['header']['other_sheep']:
        fill_data['Check Box3'] = 'Yes'
    if objs['header']['anointed']:
        fill_data['Check Box4'] = 'Yes'
    if objs['header']['elder']:
        fill_data['Check Box5'] = 'Yes'
    if objs['header']['ministerial_servant']:
        fill_data['Check Box6'] = 'Yes'
    if objs['header']['regular_pioneer']:
        fill_data['Check Box7'] = 'Yes'
    service_years = list(objs['summary'].keys())
    if len(service_years) > 0:
        fill_data['Service Year'] = service_years[0]
        fill_data['1-Place_Total'] = objs['summary'][service_years[0]
                                                     ]['total_placements']
        fill_data['1-Video_Total'] = objs['summary'][service_years[0]
                                                     ]['total_video_showings']
        fill_data['1-Hours_Total'] = objs['summary'][service_years[0]
                                                     ]['total_hours']
        fill_data['1-RV_Total'] = objs['summary'][service_years[0]
                                                  ]['total_return_visits']
        fill_data['1-Studies_Total'] = objs['summary'][service_years[0]
                                                       ]['total_studies']
        fill_data['RemarksTotal'] = "%d Reports" % objs['summary'][service_years[0]
                                                                   ]['number_of_reports']
        fill_data['1-Place_Average'] = objs['summary'][service_years[0]
                                                       ]['avg_placements']
        fill_data['1-Video_Average'] = objs['summary'][service_years[0]
                                                       ]['avg_video_showings']
        fill_data['1-Hours_Average'] = objs['summary'][service_years[0]]['avg_hours']
        fill_data['1-RV_Average'] = objs['summary'][service_years[0]
                                                    ]['avg_return_visits']
        fill_data['1-Studies_Average'] = objs['summary'][service_years[0]]['avg_studies']
        for rep in objs['reports']:
            if rep['service_year'] == service_years[0]:
                if rep['month'] == 9:
                    fill_data['1-Place_1'] = rep['placements']
                    fill_data['1-Video_1'] = rep['return_visits']
                    fill_data['1-Hours_1'] = rep['hours']
                    fill_data['1-RV_1'] = rep['return_visits']
                    fill_data['1-Studies_1'] = rep['studies']
                    fill_data['RemarksSeptember'] = rep['remarks']
                if rep['month'] == 10:
                    fill_data['1-Place_2'] = rep['placements']
                    fill_data['1-Video_2'] = rep['return_visits']
                    fill_data['1-Hours_2'] = rep['hours']
                    fill_data['1-RV_2'] = rep['return_visits']
                    fill_data['1-Studies_2'] = rep['studies']
                    fill_data['RemarksOctober'] = rep['remarks']
                if rep['month'] == 11:
                    fill_data['1-Place_3'] = rep['placements']
                    fill_data['1-Video_3'] = rep['return_visits']
                    fill_data['1-Hours_3'] = rep['hours']
                    fill_data['1-RV_3'] = rep['return_visits']
                    fill_data['1-Studies_3'] = rep['studies']
                    fill_data['RemarksNovember'] = rep['remarks']
                if rep['month'] == 12:
                    fill_data['1-Place_4'] = rep['placements']
                    fill_data['1-Video_4'] = rep['return_visits']
                    fill_data['1-Hours_4'] = rep['hours']
                    fill_data['1-RV_4'] = rep['return_visits']
                    fill_data['1-Studies_4'] = rep['studies']
                    fill_data['RemarksDecember'] = rep['remarks']
                if rep['month'] == 1:
                    fill_data['1-Place_5'] = rep['placements']
                    fill_data['1-Video_5'] = rep['return_visits']
                    fill_data['1-Hours_5'] = rep['hours']
                    fill_data['1-RV_5'] = rep['return_visits']
                    fill_data['1-Studies_5'] = rep['studies']
                    fill_data['RemarksJanuary'] = rep['remarks']
                if rep['month'] == 2:
                    fill_data['1-Place_6'] = rep['placements']
                    fill_data['1-Video_6'] = rep['return_visits']
                    fill_data['1-Hours_6'] = rep['hours']
                    fill_data['1-RV_6'] = rep['return_visits']
                    fill_data['1-Studies_6'] = rep['studies']
                    fill_data['RemarksFebruary'] = rep['remarks']
                if rep['month'] == 3:
                    fill_data['1-Place_7'] = rep['placements']
                    fill_data['1-Video_7'] = rep['return_visits']
                    fill_data['1-Hours_7'] = rep['hours']
                    fill_data['1-RV_7'] = rep['return_visits']
                    fill_data['1-Studies_7'] = rep['studies']
                    fill_data['RemarksMarch'] = rep['remarks']
                if rep['month'] == 4:
                    fill_data['1-Place_8'] = rep['placements']
                    fill_data['1-Video_8'] = rep['return_visits']
                    fill_data['1-Hours_8'] = rep['hours']
                    fill_data['1-RV_8'] = rep['return_visits']
                    fill_data['1-Studies_8'] = rep['studies']
                    fill_data['RemarksApril'] = rep['remarks']
                if rep['month'] == 5:
                    fill_data['1-Place_9'] = rep['placements']
                    fill_data['1-Video_9'] = rep['return_visits']
                    fill_data['1-Hours_9'] = rep['hours']
                    fill_data['1-RV_9'] = rep['return_visits']
                    fill_data['1-Studies_9'] = rep['studies']
                    fill_data['RemarksMay'] = rep['remarks']
                if rep['month'] == 6:
                    fill_data['1-Place_10'] = rep['placements']
                    fill_data['1-Video_10'] = rep['return_visits']
                    fill_data['1-Hours_10'] = rep['hours']
                    fill_data['1-RV_10'] = rep['return_visits']
                    fill_data['1-Studies_10'] = rep['studies']
                    fill_data['RemarksJune'] = rep['remarks']
                if rep['month'] == 7:
                    fill_data['1-Place_11'] = rep['placements']
                    fill_data['1-Video_11'] = rep['return_visits']
                    fill_data['1-Hours_11'] = rep['hours']
                    fill_data['1-RV_11'] = rep['return_visits']
                    fill_data['1-Studies_11'] = rep['studies']
                    fill_data['RemarksJuly'] = rep['remarks']
                if rep['month'] == 8:
                    fill_data['1-Place_12'] = rep['placements']
                    fill_data['1-Video_12'] = rep['return_visits']
                    fill_data['1-Hours_12'] = rep['hours']
                    fill_data['1-RV_12'] = rep['return_visits']
                    fill_data['1-Studies_12'] = rep['studies']
                    fill_data['RemarksAugust'] = rep['remarks']
    if len(service_years) > 1:
        fill_data['Service Year_2'] = service_years[1]
        fill_data['2-Place_Total'] = objs['summary'][service_years[1]
                                                     ]['total_placements']
        fill_data['2-Video_Total'] = objs['summary'][service_years[1]
                                                     ]['total_video_showings']
        fill_data['2-Hours_Total'] = objs['summary'][service_years[1]
                                                     ]['total_hours']
        fill_data['2-RV_Total'] = objs['summary'][service_years[1]
                                                  ]['total_return_visits']
        fill_data['2-Studies_Total'] = objs['summary'][service_years[1]
                                                       ]['total_studies']
        fill_data['RemarksTotal_2'] = "%d Reports" % objs['summary'][service_years[1]
                                                                     ]['number_of_reports']
        fill_data['2-Place_Average'] = objs['summary'][service_years[1]
                                                       ]['avg_placements']
        fill_data['2-Video_Average'] = objs['summary'][service_years[1]
                                                       ]['avg_video_showings']
        fill_data['2-Hours_Average'] = objs['summary'][service_years[1]]['avg_hours']
        fill_data['2-RV_Average'] = objs['summary'][service_years[1]
                                                    ]['avg_return_visits']
        fill_data['2-Studies_Average'] = objs['summary'][service_years[1]]['avg_studies']
        for rep in objs['reports']:
            if rep['service_year'] == service_years[1]:
                if rep['month'] == 9:
                    fill_data['2-Place_1'] = rep['placements']
                    fill_data['2-Video_1'] = rep['return_visits']
                    fill_data['2-Hours_1'] = rep['hours']
                    fill_data['2-RV_1'] = rep['return_visits']
                    fill_data['2-Studies_1'] = rep['studies']
                    fill_data['RemarksSeptember_2'] = rep['remarks']
                if rep['month'] == 10:
                    fill_data['2-Place_2'] = rep['placements']
                    fill_data['2-Video_2'] = rep['return_visits']
                    fill_data['2-Hours_2'] = rep['hours']
                    fill_data['2-RV_2'] = rep['return_visits']
                    fill_data['2-Studies_2'] = rep['studies']
                    fill_data['RemarksOctober_2'] = rep['remarks']
                if rep['month'] == 11:
                    fill_data['2-Place_3'] = rep['placements']
                    fill_data['2-Video_3'] = rep['return_visits']
                    fill_data['2-Hours_3'] = rep['hours']
                    fill_data['2-RV_3'] = rep['return_visits']
                    fill_data['2-Studies_3'] = rep['studies']
                    fill_data['RemarksNovember_2'] = rep['remarks']
                if rep['month'] == 12:
                    fill_data['2-Place_4'] = rep['placements']
                    fill_data['2-Video_4'] = rep['return_visits']
                    fill_data['2-Hours_4'] = rep['hours']
                    fill_data['2-RV_4'] = rep['return_visits']
                    fill_data['2-Studies_4'] = rep['studies']
                    fill_data['RemarksDecember_2'] = rep['remarks']
                if rep['month'] == 1:
                    fill_data['2-Place_5'] = rep['placements']
                    fill_data['2-Video_5'] = rep['return_visits']
                    fill_data['2-Hours_5'] = rep['hours']
                    fill_data['2-RV_5'] = rep['return_visits']
                    fill_data['2-Studies_5'] = rep['studies']
                    fill_data['RemarksJanuary_2'] = rep['remarks']
                if rep['month'] == 2:
                    fill_data['2-Place_6'] = rep['placements']
                    fill_data['2-Video_6'] = rep['return_visits']
                    fill_data['2-Hours_6'] = rep['hours']
                    fill_data['2-RV_6'] = rep['return_visits']
                    fill_data['2-Studies_6'] = rep['studies']
                    fill_data['RemarksFebruary_2'] = rep['remarks']
                if rep['month'] == 3:
                    fill_data['2-Place_7'] = rep['placements']
                    fill_data['2-Video_7'] = rep['return_visits']
                    fill_data['2-Hours_7'] = rep['hours']
                    fill_data['2-RV_7'] = rep['return_visits']
                    fill_data['2-Studies_7'] = rep['studies']
                    fill_data['RemarksMarch_2'] = rep['remarks']
                if rep['month'] == 4:
                    fill_data['2-Place_8'] = rep['placements']
                    fill_data['2-Video_8'] = rep['return_visits']
                    fill_data['2-Hours_8'] = rep['hours']
                    fill_data['2-RV_8'] = rep['return_visits']
                    fill_data['2-Studies_8'] = rep['studies']
                    fill_data['RemarksApril_2'] = rep['remarks']
                if rep['month'] == 5:
                    fill_data['2-Place_9'] = rep['placements']
                    fill_data['2-Video_9'] = rep['return_visits']
                    fill_data['2-Hours_9'] = rep['hours']
                    fill_data['2-RV_9'] = rep['return_visits']
                    fill_data['2-Studies_9'] = rep['studies']
                    fill_data['RemarksMay_2'] = rep['remarks']
                if rep['month'] == 6:
                    fill_data['2-Place_10'] = rep['placements']
                    fill_data['2-Video_10'] = rep['return_visits']
                    fill_data['2-Hours_10'] = rep['hours']
                    fill_data['2-RV_10'] = rep['return_visits']
                    fill_data['2-Studies_10'] = rep['studies']
                    fill_data['RemarksJune_2'] = rep['remarks']
                if rep['month'] == 7:
                    fill_data['2-Place_11'] = rep['placements']
                    fill_data['2-Video_11'] = rep['return_visits']
                    fill_data['2-Hours_11'] = rep['hours']
                    fill_data['2-RV_11'] = rep['return_visits']
                    fill_data['2-Studies_11'] = rep['studies']
                    fill_data['RemarksJuly_2'] = rep['remarks']
                if rep['month'] == 8:
                    fill_data['2-Place_12'] = rep['placements']
                    fill_data['2-Video_12'] = rep['return_visits']
                    fill_data['2-Hours_12'] = rep['hours']
                    fill_data['2-RV_12'] = rep['return_visits']
                    fill_data['2-Studies_12'] = rep['studies']
                    fill_data['RemarksAugust_2'] = rep['remarks']
    pypdftk.fill_form(PDF_TEMPLATE_FILE, fill_data, file_name)


def _get_service_years():
    now = datetime.datetime.now()
    first_service_year = now.year
    if now.month == 10 and now.day < 15:
        first_service_year = first_service_year - 1
    second_service_year = first_service_year + 1
    return (first_service_year, second_service_year)


def _get_past_six_months():
    now = datetime.datetime.now()
    # still collecting for last month
    if now.day < 15:
        now = now - drd.relativedelta(months=1)
    m1 = now - drd.relativedelta(months=6)
    m2 = now - drd.relativedelta(months=5)
    m3 = now - drd.relativedelta(months=4)
    m4 = now - drd.relativedelta(months=3)
    m5 = now - drd.relativedelta(months=2)
    m6 = now - drd.relativedelta(months=1)
    return [
        {'month': m1.month, 'year': m1.year},
        {'month': m2.month, 'year': m2.year},
        {'month': m3.month, 'year': m3.year},
        {'month': m4.month, 'year': m4.year},
        {'month': m5.month, 'year': m5.year},
        {'month': m6.month, 'year': m6.year},
    ]


def _get_months_in_service_year(service_year):
    return [
        {'month': 9, 'year': service_year - 1},
        {'month': 10, 'year': service_year - 1},
        {'month': 11, 'year': service_year - 1},
        {'month': 12, 'year': service_year - 1},
        {'month': 1, 'year': service_year},
        {'month': 2, 'year': service_year},
        {'month': 3, 'year': service_year},
        {'month': 4, 'year': service_year},
        {'month': 5, 'year': service_year},
        {'month': 6, 'year': service_year},
        {'month': 7, 'year': service_year},
        {'month': 8, 'year': service_year}
    ]


def _populate_fsgs(khsdatadir):
    global FSGS, PUBLISHERS
    (FSGS, PUBLISHERS) = fsgs.export_field_service_groups(
        os.path.join(khsdatadir, FSGROUP_FILE),
        os.path.join(khsdatadir, NAMES_FILE),
        EXCLUDE_FSG_BY_NAME)


def _populate_fsrecs(khsdatadir):
    global FSRECS
    FSRECS = srs.export_field_service(
        os.path.join(khsdatadir, FIELD_SERVICE_FILE))


def _load_data(khsdatadir):
    _populate_fsgs(khsdatadir)
    _populate_fsrecs(khsdatadir)


def _make_dir_name(string):
    return ''.join(c for c in string if c.isalnum).rstrip().replace(' ', '_')


def _zipdir(zipfilename, directory):
    zf = zipfile.ZipFile(zipfilename, 'w')
    for dirname, subdirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(dirname, filename)
            target_path = file_path.replace(directory, '')
            zf.write(file_path, target_path)
    zf.close()


def _get_pioneers_ids():
    pioneer_ids = []
    for fsg in FSGS:
        for pub in fsg['publishers']:
            if pub['regular_pioneer']:
                pioneer_ids.append(pub['id'])
    return pioneer_ids


def _get_inactive_ids():
    inactive_ids = []
    months_of_interest = _get_past_six_months()
    pub_index = {}
    for sr in FSRECS:
        # for each zero report
        if sr['hours'] == 0.0:
            for y_m in months_of_interest:
                # validate it is in the months of interest
                if sr['year'] == y_m['year'] and sr['month'] == y_m['month']:
                    # add the publisher_id to the dictionary index
                    # with a value of the number of zero hour reports
                    # for that publish
                    if sr['publisher_id'] not in pub_index.keys():
                        pub_index[sr['publisher_id']] = 1
                    else:
                        #pub_index[sr['publisher_id']] += 1
                        pub_index[sr['publisher_id']
                                  ] = pub_index[sr['publisher_id']] + 1
    # add any publisher_ids to the return array
    # if they have zero hours for 6 months
    for pid in pub_index.keys():
        if pub_index[pid] > 5:
            inactive_ids.append(pid)
    return inactive_ids


def _get_reports(pids):
    reports = []
    (first_year, second_year) = _get_service_years()
    sy1_months = _get_months_in_service_year(first_year)
    sy2_months = _get_months_in_service_year(second_year)
    for sr in FSRECS:
        if sr['publisher_id'] in pids:
            for m in sy1_months:
                if m['month'] == sr['month'] and m['year'] == sr['year']:
                    reports.append(sr)
            for m in sy2_months:
                if m['month'] == sr['month'] and m['year'] == sr['year']:
                    reports.append(sr)
    return sorted(reports, key=lambda i: i['timestamp'])


def _get_reports_totals_avgs(reports=[]):
    service_years = {}
    for rep in reports:
        if rep['service_year'] not in service_years.keys():
            service_years[rep['service_year']] = {
                'total_placements': 0,
                'avg_placements': 0,
                'total_video_showings': 0,
                'avg_video_showings': 0,
                'total_hours': 0,
                'avg_hours': 0,
                'total_return_visits': 0,
                'avg_return_visits': 0,
                'total_studies': 0,
                'avg_studies': 0,
                'number_of_reports': 0
            }
        service_years[rep['service_year']
                      ]['number_of_reports'] = service_years[rep['service_year']]['number_of_reports'] + 1
        service_years[rep['service_year']]['total_placements'] = service_years[rep['service_year']
                                                                               ]['total_placements'] + rep['placements']
        service_years[rep['service_year']]['total_video_showings'] = service_years[rep['service_year']
                                                                                   ]['total_video_showings'] + rep['video_showings']
        service_years[rep['service_year']
                      ]['total_hours'] = service_years[rep['service_year']]['total_hours'] + rep['hours']
        service_years[rep['service_year']]['total_return_visits'] = service_years[rep['service_year']
                                                                                  ]['total_return_visits'] + rep['return_visits']
        service_years[rep['service_year']]['total_studies'] = service_years[rep['service_year']
                                                                            ]['total_studies'] + rep['studies']
    for sy in service_years.keys():
        if service_years[sy]['number_of_reports'] > 0:
            service_years[sy]['avg_placements'] = round(
                (service_years[sy]['total_placements'] / service_years[sy]['number_of_reports']), 2)
            service_years[sy]['avg_video_showings'] = round(
                (service_years[sy]['total_video_showings'] / service_years[sy]['number_of_reports']), 2)
            service_years[sy]['avg_hours'] = round(
                (service_years[sy]['total_hours'] / service_years[sy]['number_of_reports']), 2)
            service_years[sy]['avg_return_visits'] = round(
                (service_years[sy]['total_return_visits'] / service_years[sy]['number_of_reports']), 2)
            service_years[sy]['avg_studies'] = round(
                (service_years[sy]['total_studies'] / service_years[sy]['number_of_reports']), 2)
    return service_years


def _get_publisher_header(pid):
    header = {
        'name': '',
        'date_of_birth': '',
        'date_immersed': '',
        'male': False,
        'female': False,
        'other_sheep': False,
        'anointed': False,
        'elder': False,
        'ministerial_servant': False,
        'regular_pioneer': False,
        'file_name_prefix': ''
    }
    if pid in PUBLISHERS.keys():
        publisher = PUBLISHERS[pid]
        file_name_prefix = "".join(
            x for x in "%s-%s" % (
                publisher['last_name'], publisher['first_name'])
            if x.isalnum() or x in "-")
        header['file_name_prefix'] = file_name_prefix
        header['name'] = "%s, %s" % (
            publisher['last_name'], publisher['first_name'])
        header['date_of_birth'] = publisher['date_of_birth']
        header['date_immersed'] = publisher['date_immersed']
        header['male'] = publisher['male']
        header['female'] = publisher['female']
        header['other_sheep'] = publisher['other_sheep']
        header['anointed'] = publisher['anointed']
        header['elder'] = publisher['elder']
        header['ministerial_servant'] = publisher['ministerial_servant']
        header['regular_pioneer'] = publisher['regular_pioneer']
    return header


def _generate_dummy_report():
    service_years = _get_service_years()
    report = {
        'header': _get_publisher_header('unknown')
    }
    report['summary'] = {}
    report['reports'] = []
    for sy in service_years:
        report['summary'][sy] = {
            'total_placements': 0,
            'avg_placements': 0,
            'total_video_showings': 0,
            'avg_video_showings': 0,
            'total_hours': 0,
            'avg_hours': 0,
            'total_return_visits': 0,
            'avg_return_visits': 0,
            'total_studies': 0,
            'avg_studies': 0,
            'number_of_reports': 0
        }
        report['reports'] = report['reports'] + [
            {
                'publisher_id': 0,
                'year': sy - 1,
                'month': 9,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': "",
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy - 1,
                'month': 10,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy - 1,
                'month': 11,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy - 1,
                'month': 12,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy,
                'month': 1,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy,
                'month': 2,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy,
                'month': 3,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy,
                'month': 4,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy,
                'month': 5,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy,
                'month': 6,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy,
                'month': 7,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0
            },
            {
                'publisher_id': 0,
                'year': sy,
                'month': 8,
                'service_year': sy,
                'placements': 0,
                'video_showings': 0,
                'hours': 0.0,
                'return_visits': 0,
                'studies': 0,
                'remarks': '',
                'pionner': False,
                'auxiliary_pioneer': False,
                'timestamp': 0

            }
        ]
    return report


def _generate_pioneer_reports(output_dir, json_output=False, pdf_output=True):
    # collect pioneer publisher ids
    pioneer_ids = _get_pioneers_ids()
    # make pioneer report header
    pid_headers = {}
    for pid in pioneer_ids:
        pid_headers[pid] = _get_publisher_header(pid)
    # collect reports for pioneers in prc service years
    pioneer_service_reports = _get_reports(pioneer_ids)
    # create reports
    output_dir = os.path.join(output_dir, 'active', 'pioneers')
    reports_by_pid = {}
    for pr in pioneer_service_reports:
        if pr['publisher_id'] not in reports_by_pid.keys():
            header = _get_publisher_header(pr['publisher_id'])
            reports_by_pid[pr['publisher_id']] = {
                'header': header,
                'reports': []
            }
        reports_by_pid[pr['publisher_id']]['reports'].append(pr)
    for pid in reports_by_pid.keys():
        reports_by_pid[pid]['summary'] = _get_reports_totals_avgs(
            reports_by_pid[pid]['reports'])
    if json_output:
        os.makedirs(output_dir, exist_ok=True)
        # write out json pioneer reports
        for r in reports_by_pid.keys():
            report_out_file = "%s.json" % reports_by_pid[r]['header']['file_name_prefix']
            report_out_path = os.path.join(
                output_dir, report_out_file)
            _write_json_file(report_out_path, reports_by_pid[r])
    if pdf_output:
        os.makedirs(output_dir, exist_ok=True)
        # write out S-21 pdf
        for r in reports_by_pid.keys():
            report_out_file = "%s.pdf" % reports_by_pid[r]['header']['file_name_prefix']
            report_out_path = os.path.join(
                output_dir, report_out_file)
            _write_pdf_file(report_out_path, reports_by_pid[r])
    return pioneer_ids


def _generate_inactive_reports(output_dir, json_output=False, pdf_output=True):
    # collect inactive publisher ids
    inactive_ids = _get_inactive_ids()
    # colect reports for inactive in prc service years
    inactive_service_reports = _get_reports(inactive_ids)
    # create reports
    output_dir = os.path.join(output_dir, 'inactive')
    reports_by_pid = {}
    for pr in inactive_service_reports:
        if pr['publisher_id'] not in reports_by_pid.keys():
            header = _get_publisher_header(pr['publisher_id'])
            reports_by_pid[pr['publisher_id']] = {
                'header': header,
                'reports': []
            }
        reports_by_pid[pr['publisher_id']]['reports'].append(pr)
    for pid in reports_by_pid.keys():
        reports_by_pid[pid]['summary'] = _get_reports_totals_avgs(
            reports_by_pid[pid]['reports'])
    if json_output:
        os.makedirs(output_dir, exist_ok=True)
        # write out json inactive reports
        for r in reports_by_pid.keys():
            report_out_file = "%s.json" % reports_by_pid[r]['header']['file_name_prefix']
            report_out_path = os.path.join(
                output_dir, report_out_file)
            _write_json_file(report_out_path, reports_by_pid[r])
    if pdf_output:
        os.makedirs(output_dir, exist_ok=True)
        # write out S-21 pdf
        for r in reports_by_pid.keys():
            report_out_file = "%s.pdf" % reports_by_pid[r]['header']['file_name_prefix']
            report_out_path = os.path.join(
                output_dir, report_out_file)
            _write_pdf_file(report_out_path, reports_by_pid[r])
    return inactive_ids


def _generate_fsg_reports(output_dir, pioneer_ids=None, inactive_ids=None, json_output=False, pdf_output=True):
    # collect pioneer publisher ids
    if pioneer_ids is None:
        pioneer_ids = _get_pioneers_ids()
    # collect inactive publisher ids
    if inactive_ids is None:
        inactive_ids = _get_inactive_ids()
    # create a list of field service group report objects
    fsg_pub_ids = {}
    for fsg in FSGS:
        # get publisher ids in this service group
        pub_ids = []
        for pub in fsg['publishers']:
            if (pub['id'] not in pioneer_ids) and (pub['id'] not in inactive_ids):
                pub_ids.append(pub['id'])
        # collect reports for this service group
        fsg_reports = _get_reports(pub_ids)
        # create reports
        fsg_output_dir = os.path.join(
            output_dir, 'active', _make_dir_name(fsg['name']))
        reports_by_pid = {}
        for pr in fsg_reports:
            if pr['publisher_id'] not in reports_by_pid.keys():
                reports_by_pid[pr['publisher_id']] = {
                    'header': _get_publisher_header(pr['publisher_id']),
                    'reports': []
                }
            reports_by_pid[pr['publisher_id']]['reports'].append(pr)
        for pid in reports_by_pid.keys():
            reports_by_pid[pid]['summary'] = _get_reports_totals_avgs(
                reports_by_pid[pid]['reports'])
        if json_output:
            os.makedirs(fsg_output_dir, exist_ok=True)
            for r in reports_by_pid.keys():
                report_out_file = "%s.json" % reports_by_pid[r]['header']['file_name_prefix']
                report_out_path = os.path.join(
                    fsg_output_dir, report_out_file)
                _write_json_file(report_out_path, reports_by_pid[r])
        if pdf_output:
            os.makedirs(fsg_output_dir, exist_ok=True)
            for r in reports_by_pid.keys():
                report_out_file = "%s.pdf" % reports_by_pid[r]['header']['file_name_prefix']
                report_out_path = os.path.join(
                    fsg_output_dir, report_out_file)
                _write_pdf_file(report_out_path, reports_by_pid[r])
        fsg_pub_ids[fsg['id']] = pub_ids
    return fsg_pub_ids


def _generate_summary_reports(output_dir, json_output=False, pdf_output=True):
    service_years = _get_service_years()
    # initial report data dictionaries
    pioneer_reports = _generate_dummy_report()
    pioneer_reports['header']['name'] = 'Pioneer Summary'
    pioneer_reports['header']['file_name_prefix'] = 'Pioneers'
    auxiliary_pioneer_reports = _generate_dummy_report()
    auxiliary_pioneer_reports['header']['name'] = 'Auxiliary Pioneer Summary'
    auxiliary_pioneer_reports['header']['file_name_prefix'] = 'AuxiliaryPioneers'
    publisher_reports = _generate_dummy_report()
    publisher_reports['header']['name'] = 'Auxiliary Pioneer Summary'
    publisher_reports['header']['file_name_prefix'] = 'Publishers'

    first_sy_month_indexes = {9: 0, 10: 1, 11: 2, 12: 3,
                              1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11}
    second_sy_month_indexes = {9: 12, 10: 13, 11: 14, 12: 15,
                               1: 16, 2: 17, 3: 18, 4: 19, 5: 20, 6: 21, 7: 22, 8: 23}

    for sr in FSRECS:
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
        _write_json_file(report_out_path, pioneer_reports)
        report_out_file = "%s.json" % auxiliary_pioneer_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        _write_json_file(report_out_path, auxiliary_pioneer_reports)
        report_out_file = "%s.json" % publisher_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        _write_json_file(report_out_path, publisher_reports)
    if pdf_output:
        os.makedirs(output_dir, exist_ok=True)
        report_out_file = "%s.pdf" % pioneer_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        _write_pdf_file(report_out_path, pioneer_reports)
        report_out_file = "%s.pdf" % auxiliary_pioneer_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        _write_pdf_file(report_out_path, auxiliary_pioneer_reports)
        report_out_file = "%s.pdf" % publisher_reports['header']['file_name_prefix']
        report_out_path = os.path.join(output_dir, report_out_file)
        _write_pdf_file(report_out_path, publisher_reports)


'''
Parse command arguments and excute export workflow
'''


def main():
    ap = argparse.ArgumentParser(
        prog='export_khs_to_prcs',
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
        help='create S-21-E PDFs',
        default=None,
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

    pdf_template_file = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)), 'templates', 'S-21-E.pdf')

    if args.pdftemplate:
        pdf_template_file = args.pdftemplate

    required_files = [
        FSGROUP_FILE,
        NAMES_FILE,
        FIELD_SERVICE_FILE
    ]

    if args.pdf:
        required_files.append(pdf_template_file)
        global PDF_TEMPLATE_FILE
        PDF_TEMPLATE_FILE = pdf_template_file

    for file in required_files:
        file_path = os.path.join(args.khsdatadir, file)
        if not os.path.exists(file_path):
            print('\nCan not find %s, a required file\n')
            sys.exit(1)

    _load_data(args.khsdatadir)
    pioneer_ids = _generate_pioneer_reports(
        args.outputdir, args.json, args.pdf)
    inactive_ids = _generate_inactive_reports(
        args.outputdir, args.json, args.pdf)
    _generate_fsg_reports(args.outputdir, pioneer_ids,
                          inactive_ids, args.json, args.pdf)
    _generate_summary_reports(args.outputdir, args.json, args.pdf)

    if args.zip:
        _zipdir(args.zipfilename, args.outputdir)


'''
The script was executed from the CLI directly, run main function
'''
if __name__ == "__main__":
    main()
