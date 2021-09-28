#!/usr/bin/env python3

import argparse
import json
import os
import sys

from dbfread import DBF

FIELD_SERVICE_FILE = 'Field_service.DBF'

'''
Export field service reports from the Field_service.DBF file.

Each field service report is added to a list of report dictionaries.

Each report dictionary contains the publisher_id who submitted the report, the year(int), the month(int),
the placements(int), the video_showings(int), hours(int), return_visits(int), studies(int), and
a remarks field (string).

Example:

[
  {
    "publisher_id": 674,
    "year": "2016",
    "month": "09",
    "placements": 0,
    "video_showings": 0,
    "hours": 7.0,
    "return_visits": 2,
    "studies": 0,
    "remarks": ""
  }
  ...
] 
'''
def export_field_service(fs_file_path):
    fs_db = DBF(fs_file_path)
    # build a dictionary of fields we need for the PRC
    field_index = {}
    for idx, f in enumerate(fs_db.field_names):
        field_index[f] = idx
    publisher_id_index = field_index['NAMES_ID']
    year_month_index = field_index['YEARMONTH']
    placements_indx = field_index['PLACEMENTS']
    video_showings_index = field_index['VIDEOS']
    hours_index = field_index['HOURS']
    return_visits_index = field_index['RVS']
    studies_index = field_index['STUDIES']
    remarks_index = field_index['REMARKS']

    fs_reports = []
    for rec in fs_db.records:
        vals = list(rec.values())
        fs_reports.append(
            {
                'publisher_id': vals[publisher_id_index],
                'year': int(vals[year_month_index][0:4]),
                'month': int(vals[year_month_index][-2:]),
                'placements': vals[placements_indx],
                'video_showings': vals[video_showings_index],
                'hours': vals[hours_index],
                'return_visits': vals[return_visits_index],
                'studies': vals[studies_index],
                'remarks': vals[remarks_index]
            }
        )
    return fs_reports

'''
Print out a analysis of the field service groups
'''
def get_analysis(fs_file_path):
    fs_reports = export_field_service(fs_file_path)
    print("Field Service Report Analysis")
    print("----------------------------")
    print("Number of Reports: %d" % len(fs_reports))
    lowest_month_in_year = 1
    lowest_year = 999999
    highest_month_in_year = 12
    highest_year = 0
    number_zero_hour = 0
    publisher_reports = {}
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
    print("Number of publishers: %d" % len(publisher_reports.keys()))
    print("Number of zero hour reports: %s" % number_zero_hour)
    print("Earliest report: %d-%d" % (lowest_month_in_year, lowest_year))
    print("Latest report: %d-%d" % (highest_month_in_year, highest_year))

'''
Export service reports in JSON format
'''
def get_fs_json(fs_file_path):
    return json.dumps(
        export_field_service(fs_file_path),
        indent=2
    )

'''
Parse command arguments and excute export workflow
'''
def main():
    ap = argparse.ArgumentParser(
        prog='create_field_service_records',
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
        FIELD_SERVICE_FILE
    ]

    for file in required_files:
        file_path = os.path.join(args.khsdatadir, file)
        if not os.path.exists(file_path):
            print('\nCan not find %s, a required file\n')

    if args.analysis:
        get_analysis(
            os.path.join(args.khsdatadir, FIELD_SERVICE_FILE))
    else:
        fs_json = get_fs_json(
            os.path.join(args.khsdatadir, FIELD_SERVICE_FILE))
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
