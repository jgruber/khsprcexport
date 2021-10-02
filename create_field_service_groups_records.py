#!/usr/bin/env python3

import argparse
import json
import os
import sys

from dbfread import DBF

FSGROUP_FILE = 'Fsgroups.DBF'
NAMES_FILE = 'Names.DBF'

'''
Export field service group list from DBF files.

Each field service group in the Fsgroups.DBF file gets a dictionary in the list. 
The group dictionary includes the group ID, the group name, and list of publishers in the group.

The publishers are taken from the Names.DBF file. The pulishers list entry is a dictionary with 
the publishers ID, first and last name, gender (M|F), annointed (boolean), elder (boolean), 
ministerial_servant (boolean), regular_pioneer (boolean), date of birth (YYYY-MM-DD), and
date of baptism (YYYY-MM-DD).

Example:

[
    {
        "id": 1,
        "name": "Unassigned",
        "publishers": [
            {
                "id": 445,
                "last_name": "Doe",
                "first_name": "John",
                "gender": "M",
                "annointed": false,
                "elder": false,
                "ministerial_servant": false,
                "regular_pioneer": false,
                "date_of_birth": "2000-01-01",
                "date_of baptism": "2015-01-01"
            }      
        ]
    }
    ....
]    

'''


def export_field_service_groups(fsg_file_path, names_path, excludes=[]):
    names_db = DBF(names_path)
    # build a dictionary of fields we need for the PRC
    field_index = {}
    for idx, f in enumerate(names_db.field_names):
        field_index[f] = idx
    fsg_id_index = field_index['FSGROUP_ID']
    last_name_index = field_index['LASTNAME']
    first_name_index = field_index['FIRSTNAME']
    gender_index = field_index['GENDER']
    anointed_index = field_index['ANOINTED']
    elder_index = field_index['ELDER']
    ministerial_servant_index = field_index['SERVANT']
    regular_pioneer_index = field_index['PIONEER']
    do_birth_index = field_index['DOB']
    baptized_index = field_index['BAPTIZED']
    unbaptized_publisher_index = field_index['UBP']
    do_baptism_index = field_index['BAPTIZEDON']
    deceased_index = field_index['DECEASED']
    regular_aux_pioneer_index = field_index['AUX_PIONEE']

    publishers = {}
    fsg_n = {}
    for rec in names_db.records:
        vals = list(rec.values())
        fsg_id = vals[fsg_id_index]
        if not fsg_n or fsg_id not in fsg_n.keys():
            fsg_n[fsg_id] = []
        male = False
        female = False
        if vals[gender_index] == 2:
            female = True
        else:
            male = True
        anointed = False
        other_sheep = True
        if vals[anointed_index]:
            anointed = True
            other_sheep = False
        elder = False
        if vals[elder_index]:
            elder = True
        ministerial_servant = False
        if vals[ministerial_servant_index]:
            ministerial_servant = True
        regular_pioneer = False
        if vals[regular_pioneer_index]:
            regular_pioneer = True
        baptized = False
        if vals[baptized_index]:
            baptized = True
        unbaptized_publisher = False
        if vals[unbaptized_publisher_index]:
            unbaptized_publisher = True
        regular_aux_pioneer = False
        if vals[regular_aux_pioneer_index]:
            regular_aux_pioneer = True
        do_birth = vals[do_birth_index]
        if do_birth:
            do_birth = do_birth.strftime("%Y-%m-%d")
        else:
            do_birth = ''
        do_baptism = vals[do_baptism_index]
        if do_baptism:
            do_baptism = do_baptism.strftime("%Y-%m-%d")
        else:
            if unbaptized_publisher:
                do_baptism = 'UBP'
            else:
                do_baptism = ''
        deceased = False
        if vals[deceased_index]:
            deceased = True
        if not deceased:
            publishers[vals[0]] = {
                    'id': vals[0],
                    'last_name': vals[last_name_index],
                    'first_name': vals[first_name_index],
                    'male': male,
                    'female': female,
                    'anointed': anointed,
                    'other_sheep': other_sheep,
                    'elder': elder,
                    'ministerial_servant': ministerial_servant,
                    'regular_pioneer': regular_pioneer,
                    'regular_auxiliary_pioneer': regular_aux_pioneer,
                    'date_of_birth': do_birth,
                    'baptized': baptized,
                    'unbatized_publisher': unbaptized_publisher,
                    'date_immersed': do_baptism
                }
            fsg_n[fsg_id].append(
                publishers[vals[0]]
            )
            
    fsgs = []
    fsg_db = DBF(fsg_file_path)
    for rec in fsg_db.records:
        fsg = list(rec.values())
        if fsg[1] not in excludes:
            fsgs.append(
                {'id': fsg[0], 'name': fsg[1], 'publishers': fsg_n[fsg[0]]})
    return (fsgs, publishers)


'''
Print out a analysis of the field service groups
'''


def get_analysis(fsg_file_path, name_file_path, show_names=False):
    (fsgs, publishers) = export_field_service_groups(fsg_file_path, name_file_path)
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
    (fsgs, publishers) = export_field_service_groups(fsg_file_path, name_file_path)
    return json.dumps(
        fsgs,
        indent=2
    )


'''
Parse command arguments and excute export workflow
'''


def main():
    ap = argparse.ArgumentParser(
        prog='create_field_service_group_records',
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
        FSGROUP_FILE,
        NAMES_FILE
    ]

    for file in required_files:
        file_path = os.path.join(args.khsdatadir, file)
        if not os.path.exists(file_path):
            print('\nCan not find %s, a required file\n')
            sys.exit(1)

    if args.analysis:
        get_analysis(
            os.path.join(args.khsdatadir, FSGROUP_FILE),
            os.path.join(args.khsdatadir, NAMES_FILE))
    else:
        fsg_json = get_fsgs_json(
            os.path.join(args.khsdatadir, FSGROUP_FILE),
            os.path.join(args.khsdatadir, NAMES_FILE))

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
