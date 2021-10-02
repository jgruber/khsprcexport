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

The pypdftk python module requires that the pdftk application be installed and available on the path for the user running the script.

See installation for the server install at:

https://www.pdflabs.com/tools/pdftk-server/

The linux version, `pdftk`, is included in the standard package respositories for every major distribution. Try your package manager for a quck install. 

```bash
sudo apt install pdftk
```

Or, you just run it in a container.. :-).

## Running the create_publisher_record_cards.py Report Script in a Conatiner

Clone the repository:

```bash
git clone https://github.com/jgruber/khsprcexport.git
cd khsprcexport
```

Build the docker container:

```bash
docker build -t "khsprcexport:latest" .
```

Run the container with two volume mounts:

/data = Your KHS data directory

/output = The output path for your PDF S-21-E output

```bash
docker run --rm -v /KHS/data:/data  -v /tmp/backups/output:/output khsprcexport:latest
```

## Running Report Scripts Locally

Createing Pubisher Record cards with *create_publisher_record_cards.py*

`create_publisher_record_cards.py --khsdatadir=[path to your DBF files] [--json|pdf]`

```bash
usage: create_publisher_record_cards.py [options]

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
                        S-21-E.pdf original PDF template file - default is ./templates/S-21_E.pdf
  --zip                 create a zip archive the output folder
  --zipfilename ZIPFILENAME
                        the zip file to create
```

The output directory will contain either the JSON (`--json`) or S-21-E PDF (`--pdf`) publisher record cards arranged per sfl 22:12.

```bash
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

```bash
prcs-2021-10-01T20:53:41.729649.zip
```

## Utility modules

Exporting or Analyzing Service Groups with *field_service_groups.py*

```bash
usage: field_service_groups.py [options]

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

If you run with the `--analysis` option you will get a summary of the service group data.

```bash
./field_service_groups.py --khsdatadir=./data --analysis
Field Service Group Analysis
----------------------------
Number of Groups: 7
Group: Unassigned, Id: 1, Number Publishers: 53
Group: SG 1, Id: 4, Number Publishers: 23
Group: SG 2, Id: 5, Number Publishers: 42
Group: SG 3, Id: 6, Number Publishers: 36
Group: SG 4, Id: 8, Number Publishers: 33
Group: SG 5, Id: 10, Number Publishers: 36
Group: SG 6, Id: 12, Number Publishers: 37
Number of Publishers: 260

```

Exporting or Analyzing Service Reports with *field_service_records.py*

```bash
usage: field_service_records.py [options]

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

If you run with the `--analysis` option you will get a summary of the service group data.

```bash
./field_service_records.py --khsdatadir=./data --analysis
Field Service Report Analysis
----------------------------
Number of Reports: 7586
Number of distinct publishers: 258
Number of zero hour reports: 1786
Earliest report: 1-2016
Latest report: 12-2022
Active Publishers: 138
Irregular Publishers: 21
```
