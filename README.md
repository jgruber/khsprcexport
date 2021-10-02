# khsprcexport
Create S-21 PDF or JSON Publisher Record Card exports from KHS DBF files

export_khs_to_prcs.py

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

## Utility modules

create_field_service_groups_records.py

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

create_field_service_records.py

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