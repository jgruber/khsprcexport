import os
import datetime

from khsprcexport import constants

from dbfread import DBF

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


def create_field_service_groups(fsg_file_path, names_path, excludes=[]):
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
    moved_date_index = field_index['MOVE_DATE']

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
        moved_date = vals[moved_date_index]
        if moved_date:
            moved_date = moved_date.strftime("%Y-%m-%d")
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
                'date_immersed': do_baptism,
                'moved_date': moved_date
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


def create_field_service_reports(fs_file_path):
    fs_db = DBF(fs_file_path)
    # build a dictionary of fields we need for the PRC
    field_index = {}
    for idx, f in enumerate(fs_db.field_names):
        field_index[f] = idx
    publisher_id_index = field_index['NAMES_ID']
    year_month_index = field_index['YEARMONTH']
    placements_index = field_index['PLACEMENTS']
    video_showings_index = field_index['VIDEOS']
    hours_index = field_index['HOURS']
    return_visits_index = field_index['RVS']
    studies_index = field_index['STUDIES']
    remarks_index = field_index['REMARKS']
    par_index = field_index['PAR']

    fs_reports = []
    for rec in fs_db.records:
        vals = list(rec.values())

        auxiliary_pioneer = False
        pioneer = False
        if vals[par_index] == 2:
            auxiliary_pioneer = True
        if vals[par_index] == 3:
            pioneer = True
        year = int(vals[year_month_index][0:4])
        month = int(vals[year_month_index][-2:])
        service_year = year
        if month > 8:
            service_year = year + 1
        if vals[placements_index] is None:
            vals[placements_index] = 0
        if vals[video_showings_index] is None:
            vals[video_showings_index] = 0
        if vals[hours_index] is None:
            vals[hours_index] = 0
        if vals[return_visits_index] is None:
            vals[return_visits_index] = 0
        if vals[studies_index] is None:
            vals[studies_index] = 0
        fs_reports.append(
            {
                'publisher_id': vals[publisher_id_index],
                'year': year,
                'month': month,
                'service_year': service_year,
                'placements': vals[placements_index],
                'video_showings': vals[video_showings_index],
                'hours': vals[hours_index],
                'return_visits': vals[return_visits_index],
                'studies': vals[studies_index],
                'remarks': vals[remarks_index],
                'pioneer': pioneer,
                'auxiliary_pioneer': auxiliary_pioneer,
                'timestamp': datetime.datetime.strptime("%d-%d" % (year, month), '%Y-%m').timestamp()
            }
        )
    return fs_reports


def populate_fsgs(khsdatadir=None, exclude_fsg_names=[]):
    (fsgs, publishers) = create_field_service_groups(
        os.path.join(khsdatadir, constants.FSGROUP_FILE),
        os.path.join(khsdatadir, constants.NAMES_FILE),
        exclude_fsg_names)
    return (fsgs, publishers)


def populate_fsrecs(khsdatadir):
    return create_field_service_reports(
        os.path.join(khsdatadir, constants.FIELD_SERVICE_FILE))


def load_khs_data(khsdatadir):
    (fsgs, publishers) = populate_fsgs(khsdatadir)
    fsrecs = populate_fsrecs(khsdatadir)
    return (fsgs, publishers, fsrecs)
