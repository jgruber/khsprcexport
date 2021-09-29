#!/usr/bin/env python3

import os
import sys
import json
import argparse
import datetime

import create_field_service_groups_records as fsgs
import create_field_service_records as srs

def _get_collection_months_dictionary():
    now = datetime.datetime.now()
    first_service_year = now.year
    if now.month < 9:
        first_service_year - 1
    second_service_year = first_service_year + 1
    months = [
        {
            'service_year': first_service_year,
            'total_placements_field': '1-Place_Total',
            'total_video_showings_field': '1-Video_Total',
            'total_hours_field': '1-Hours_Total',
            'total_return_visits_field': '1-RV_Total',
            'total_studies_field': '1-Studies_Total',
            'average_placements_field': '1-Place_Average',
            'average_video_showings_field': '1-Video_Average',
            'average_hours_field': '1-Hours_Average',
            'average_return_visits_field': '1-RV_Average',
            'average_studies_field': '1-Studies_Average',
            'months': []
        },
        {
            'service_year': second_service_year,
            'total_placements_field': '2-Place_Total',
            'total_video_showings_field': '2-Video_Total',
            'total_hours_field': '2-Hours_Total',
            'total_return_visits_field': '2-RV_Total',
            'total_studies_field': '2-Studies_Total',
            'average_placements_field': '2-Place_Average',
            'average_video_showings_field': '2-Video_Average',
            'average_hours_field': '2-Hours_Average',
            'average_return_visits_field': '2-RV_Average',
            'average_studies_field': '2-Studies_Average',
            'months': []
        }
    ]
    remark_fields = [
        'RemarksSeptember',
        'RemarksOctober',
        'RemarksNovember',
        'RemarksDecember',
        'RemarksJanuary',
        'RemarksFebruary',
        'RemarksMarch',
        'RemarksApril',
        'RemarksMay',
        'RemarksJune',
        'RemarksJuly',
        'RemarksAugust'
    ]
    for page in range(2):
        page_indx = page + 1
        for indx, mi in enumerate([9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]):
            field_index = indx + 1
            year = months[page]['service_year']
            if mi > 8:
                year = months[page]['service_year'] - 1
            remarks_suffix = ''
            if page > 0:
                remarks_suffix = '_2'
            months[page]['months'].append({
                'year': year,
                'month': mi,
                'placements_field': '%d-Place_%d' % (page_indx, field_index),
                'video_showings_field': '%d-Video_%d' % (page_indx, field_index),
                'hours_field': '%d-Hours_%d' % (page_indx, field_index),
                'return_visits_field': '%d-RV_%d' % (page_indx, field_index),
                'studies_field': '%d-Studies_%d' % (page_indx, field_index),
                'remarks_field': '%s%s' % (remark_fields[indx], remarks_suffix)
            })
    return months

'''
Parse command arguments and excute export workflow
'''
def main():
    ap = argparse.ArgumentParser(
        prog='export_khs_to_prcs.py',
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
        default='./prcexport',
        required=True
    )
    ap.add_argument(
        '--zip',
        help='create a zip archive the output folder',
        action='store_true'
    )
    
    
    print(json.dumps(_get_collection_months_dictionary(), indent=2))



'''
The script was executed from the CLI directly, run main function
'''
if __name__ == "__main__":
    main()