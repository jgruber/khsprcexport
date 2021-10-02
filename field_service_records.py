#!/usr/bin/env python3

import argparse
import json
import os
import sys

from khsprcexport import constants
from khsprcexport import importers
from khsprcexport import utils


'''
Print out a analysis of the field service groups
'''


def get_analysis(fs_file_path):
    fs_reports = importers.create_field_service_reports(fs_file_path)
    print("Field Service Report Analysis")
    print("----------------------------")
    print("Number of Reports: %d" % len(fs_reports))
    lowest_month_in_year = 1
    lowest_year = 999999
    highest_month_in_year = 12
    highest_year = 0
    number_zero_hour = 0
    publisher_reports = {}
    pioneer_reports = 0
    auxiliary_pioneer_reports = 0
    active_publishers = {}

    last_six_months = utils.get_past_six_months()

    for rep in fs_reports:
        if rep['year'] <= lowest_year:
            lowest_year = rep['year']
            if rep['month'] < lowest_month_in_year:
                lowest_month_in_year = rep['month']
        if int(rep['year']) > highest_year:
            highest_year = int(rep['year'])
            if rep['month'] > highest_month_in_year:
                highest_month_in_year = rep['month']
        if rep['publisher_id'] not in publisher_reports:
            publisher_reports[rep['publisher_id']] = 1
        else:
            publisher_reports[rep['publisher_id']
                              ] = publisher_reports[rep['publisher_id']] + 1
        if rep['hours'] == 0:
            number_zero_hour += 1
        if rep['pioneer']:
            pioneer_reports += 1
        if rep['auxiliary_pioneer']:
            auxiliary_pioneer_reports += 1
        for m in last_six_months:
            if rep['year'] == m['year'] and rep['month'] == m['month'] and rep['hours'] > 0:
                if rep['publisher_id'] not in active_publishers:
                    active_publishers[rep['publisher_id']] = 1
                else:
                    active_publishers[rep['publisher_id']
                                      ] = active_publishers[rep['publisher_id']] + 1

    irregular_publishers = 0
    for pid in active_publishers.keys():
        if active_publishers[pid] < 6:
            irregular_publishers += 1

    print("Number of distinct publishers: %d" % len(publisher_reports.keys()))
    print("Number of zero hour reports: %s" % number_zero_hour)
    print("Earliest report: %d-%d" % (lowest_month_in_year, lowest_year))
    print("Latest report: %d-%d" % (highest_month_in_year, highest_year))
    print("Active Publishers: %d" % len(active_publishers.keys()))
    print("Irregular Publishers: %d" % irregular_publishers)


'''
Export service reports in JSON format
'''


def get_fs_json(fs_file_path):
    return json.dumps(
        importers.create_field_service_reports(fs_file_path),
        indent=2
    )


'''
Parse command arguments and excute export workflow
'''


def main():
    ap = argparse.ArgumentParser(
        prog='field_service_records',
        usage='%(prog)s.py [options]',
        description='reads KHS DBF files and creates field service JSON data file',
    )
    ap.add_argument(
        '--khsdatadir',
        help='path to KHS data files',
        required=True
    )
    ap.add_argument(
        '--jsonout',
        help='export JSON file',
        required=False,
        default=''
    )
    ap.add_argument(
        '--analysis',
        help='print analysis only',
        action='store_true'
    )
    args = ap.parse_args()

    required_files = [
        constants.FIELD_SERVICE_FILE
    ]

    for file in required_files:
        file_path = os.path.join(args.khsdatadir, file)
        if not os.path.exists(file_path):
            print('\nCan not find %s, a required file\n')
            sys.exit(1)

    if args.analysis:
        get_analysis(
            os.path.join(args.khsdatadir, constants.FIELD_SERVICE_FILE))
    else:
        fs_json = get_fs_json(
            os.path.join(args.khsdatadir, constants.FIELD_SERVICE_FILE))
        if args.jsonout:
            with open(args.jsonout, 'w') as jf:
                jf.write(fs_json)
        else:
            print(fs_json)


'''
The script was executed from the CLI directly, run main function
'''
if __name__ == "__main__":
    main()
