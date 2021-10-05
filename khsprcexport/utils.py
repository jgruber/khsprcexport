import os
import datetime
import dateutil.relativedelta as drd
import zipfile

from khsprcexport import importers

def get_service_years():
    now = datetime.datetime.now()
    first_service_year = now.year
    if now.month == 10 and now.day < 15:
        first_service_year = first_service_year - 1
    second_service_year = first_service_year + 1
    return (first_service_year, second_service_year)


def get_past_six_months():
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


def get_months_in_service_year(service_year):
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


def make_dir_name(string):
    return ''.join(c for c in string if c.isalnum).rstrip().replace(' ', '_')


def zipdir(zipfilename, directory):
    zf = zipfile.ZipFile(zipfilename, 'w')
    for dirname, subdirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(dirname, filename)
            target_path = file_path.replace(directory, '')
            zf.write(file_path, target_path)
    zf.close()


def get_pioneers_ids(fsgs=None, khsdatadir=None):
    if not fsgs and khsdatadir:
        (fsgs, publishers) = importers.populate_fsgs(khsdatadir)
    pioneer_ids = []
    for fsg in fsgs:
        for pub in fsg['publishers']:
            if pub['regular_pioneer']:
                pioneer_ids.append(pub['id'])
    return pioneer_ids


def get_inactive_ids(fsrecords=None, khsdatadir=None):
    if not fsrecords and khsdatadir:
        fsrecords = importers.populate_fsrecs(khsdatadir)
    inactive_ids = []
    months_of_interest = get_past_six_months()
    pub_index = {}
    for sr in fsrecords:
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


def get_reports(publisher_ids=[], fsrecords=None, khsdatadir=None):
    if not fsrecords and khsdatadir:
        fsrecords = importers.populate_fsrecs(khsdatadir)
    reports = []
    (first_year, second_year) = get_service_years()
    sy1_months = get_months_in_service_year(first_year)
    sy2_months = get_months_in_service_year(second_year)
    for sr in fsrecords:
        if sr['publisher_id'] in publisher_ids:
            for m in sy1_months:
                if m['month'] == sr['month'] and m['year'] == sr['year']:
                    reports.append(sr)
            for m in sy2_months:
                if m['month'] == sr['month'] and m['year'] == sr['year']:
                    reports.append(sr)
    return sorted(reports, key=lambda i: i['timestamp'])


def get_reports_totals_avgs(reports=[]):
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
        service_years[rep['service_year']]['number_of_reports'] = (
            service_years[rep['service_year']]['number_of_reports'] + 1)
        service_years[rep['service_year']]['total_placements'] = (
            service_years[rep['service_year']]['total_placements'] + rep['placements'])
        service_years[rep['service_year']]['total_video_showings'] = (
            service_years[rep['service_year']]['total_video_showings'] + rep['video_showings'])
        service_years[rep['service_year']]['total_hours'] = (
            service_years[rep['service_year']]['total_hours'] + rep['hours'])
        service_years[rep['service_year']]['total_return_visits'] = (
            service_years[rep['service_year']]['total_return_visits'] + rep['return_visits'])
        service_years[rep['service_year']]['total_studies'] = (
            service_years[rep['service_year']]['total_studies'] + rep['studies'])
    for sy in service_years.keys():
        if service_years[sy]['number_of_reports'] > 0:
            service_years[rep['service_year']]['total_hours'] = round(
                service_years[rep['service_year']]['total_hours'] + rep['hours'], 2)
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


def get_publisher_header(publisher_id=None, publishers={}, khsdatadir=None):
    if not publishers and khsdatadir:
        (fsgs, publishers) = importers.populate_fsgs(khsdatadir)
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
    if publishers and publisher_id in publishers.keys():
        publisher = publishers[publisher_id]
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


def generate_dummy_report():
    service_years = get_service_years()
    report = {
        'header': get_publisher_header('unknown')
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