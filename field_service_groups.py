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


def get_analysis(fsg_file_path, name_file_path, show_names=False):
    (fsgs, publishers) = importers.create_field_service_groups(fsg_file_path, name_file_path)
    print("Field Service Group Analysis")
    print("----------------------------")
    print("Number of Groups: %d" % len(fsgs))
    num_of_publishers = 0
    for fsg in fsgs:
        publishers_in_fsg = len(fsg['publishers'])
        num_of_publishers = num_of_publishers + publishers_in_fsg
        print("Group: %s, Id: %d, Number Publishers: %d" % (
            fsg['name'], fsg['id'], publishers_in_fsg))
        if show_names:
            for p in fsg['publishers']:
                print("    %s %s - %d" %
                      (p['first_name'], p['last_name'], p['id']))
    print("Number of Publishers: %d" % num_of_publishers)


'''
Export the field service groups to JSON format
'''


def get_fsgs_json(fsg_file_path, name_file_path):
    (fsgs, publishers) = importers.create_field_service_groups(fsg_file_path, name_file_path)
    return json.dumps(
        fsgs,
        indent=2
    )


'''
Parse command arguments and excute export workflow
'''


def main():
    ap = argparse.ArgumentParser(
        prog='field_service_groups',
        usage='%(prog)s.py [options]',
        description='reads KHS DBF files and creates field service group JSON data file',
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
        constants.FSGROUP_FILE,
        constants.NAMES_FILE
    ]

    for file in required_files:
        file_path = os.path.join(args.khsdatadir, file)
        if not os.path.exists(file_path):
            print('\nCan not find %s, a required file\n')
            sys.exit(1)

    if args.analysis:
        get_analysis(
            os.path.join(args.khsdatadir, constants.FSGROUP_FILE),
            os.path.join(args.khsdatadir, constants.NAMES_FILE))
    else:
        fsg_json = get_fsgs_json(
            os.path.join(args.khsdatadir, constants.FSGROUP_FILE),
            os.path.join(args.khsdatadir, constants.NAMES_FILE))

        if args.jsonout:
            with open(args.jsonout, 'w') as jf:
                jf.write(fsg_json)
        else:
            print(fsg_json)


'''
The script was executed from the CLI directly, run main function
'''
if __name__ == "__main__":
    main()
