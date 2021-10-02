# khsprcexport
Create S-21 PDF or JSON Publisher Record Card exports from KHS DBF files

## install

```bash
git clone https://github.com/jgruber/khsprcexport.git
cd khsprcexport
python3 -m venv .venv
source .venv/bin/activate
# on window - .venv\Scripts\activate.bat
pip3 install -r requirements.txt
```

## run

*export_khs_to_prcs.py*

`export_khs_to_prcs.py --khsdatadir=[path to your DBF files]`

```bash
usage: export_khs_to_prcs.py [options]

reads KHS DBF files and creates S-21-E pdfs in a virtual card file

optional arguments:
  -h, --help            show this help message and exit
  --khsdatadir KHSDATADIR
                        path to KHS data files
  --outputdir OUTPUTDIR
                        path to output virtual card file
  --json                create reports json
  --pdf                 create S-21-E PDFs
  --pdftemplate PDFTEMPLATE
                        create S-21-E PDFs
  --zip                 create a zip archive the output folder
  --zipfilename ZIPFILENAME
                        the zip file to create
```

The output directory will contain either the JSON (`--json`) or S-21-E PDF (`--pdf`) publisher record cards arranged per sfl 22:12.

```
.
├── active
│   ├── pioneers
│   │   ├── Doe-Joannie.pdf
│   │   ├── Doe-John.pdf
│   │   └── Wise-Solomon.pdf
│   ├── SG_1
│   │   ├── Faithful-Abrahman.pdf
│   │   ├── Faithful-Sarah.pdf
│   │   └── Brave-Ruth.pdf
│   └── Unassigned
│       ├── Newly-Zack.pdf
│       └── Recent-Addus.pdf
├── AuxiliaryPioneers.pdf
├── inactive
│   └── Missing-Ima.pdf
├── Pioneers.pdf
└── Publishers.pdf
```

If the `--zip` option is used, the output directory will archived in a single zip file. The zip file name can be passed with the `--zipfilename` option or will be named with an ISO timestamp.

```
prcs-2021-10-01T20:53:41.729649.zip
```

## Utility modules

*create_field_service_groups_records.py*

```bash
usage: create_field_service_group_records.py [options]

reads KHS DBF files and creates field service group JSON data file

optional arguments:
  -h, --help            show this help message and exit
  --khsdatadir KHSDATADIR
                        path to KHS data files
  --jsonout JSONOUT     export JSON file
  --analysis            print analysis only
```

The exported fields service groups are in an intermediate JSON format with some embleshments. Running with with only the `--khsdatadir` will export the JSON format to stdout.

```json
[
  {
    "id": 1,
    "name": "Unassigned",
    "publishers": [
      {
        "id": 112,
        "last_name": "Doe",
        "first_name": "John",
        "male": true,
        "female": false,
        "anointed": false,
        "other_sheep": true,
        "elder": false,
        "ministerial_servant": false,
        "regular_pioneer": false,
        "regular_auxiliary_pioneer": false,
        "date_of_birth": "2000-01-01",
        "baptized": false,
        "unbatized_publisher": true,
        "date_immersed": "UBP"
      }
    ]
  }  
]
```

*create_field_service_records.py*

```bash
usage: create_field_service_records.py [options]

reads KHS DBF files and creates field service JSON data file

optional arguments:
  -h, --help            show this help message and exit
  --khsdatadir KHSDATADIR
                        path to KHS data files
  --jsonout JSONOUT     export JSON file
  --analysis            print analysis only
```

The field service records are exported in a intermediate JSON with minor embleshments. Running with with only the `--khsdatadir` will export the JSON format to stdout. The embleshed `timestamp` attribute make sorting reports simple.

```json
[
  {
    "publisher_id": 754,
    "year": 2021,
    "month": 1,
    "service_year": 2021,
    "placements": 4,
    "video_showings": 2,
    "hours": 6.0,
    "return_visits": 0,
    "studies": 0,
    "remarks": "",
    "pioneer": false,
    "auxiliary_pioneer": false,
    "timestamp": 1609480800.0
  }
]
```
