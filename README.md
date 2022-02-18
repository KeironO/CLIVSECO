# CLIVSECO

CLInical coder Verification of SEmi automated auto COder

## Installation and First Time Run

```
conda create --name clivseco --file pkgs.txt 
conda activate clivseco
python web/run.py
```

## API 'Documentation'

```python
import requests

yeee = {
    "clinical_finding": "CLI",
    "presenting_complaint": "PRE",
    "treatment_narrative": "TRE",
    "discharge_diagnoses" : "DIA",
    "allergy": "ALL"
}


id_table = {}

for no in nice_ones:
    nice_data = results[no]
    
    
    note_data = {k.lower(): str(v["value"]) for k, v in nice_data.items()}
    note_data["dal_id"] = no
    
    
    note_request = requests.post("http://127.0.0.1:5000/api/notes/new",
                                json=note_data)
    
    
    id_table[no] = note_request.json()["content"]["id"]
    
    for k, v in nice_data.items():
        
        auto_codes = {}
        
        for eid, entity in v["result"].items():
            if entity["icd10"] != []:
                for icd10 in entity["icd10"]:
                    
                    _annot = requests.post("http://127.0.0.1:5000/api/notes/add/autocode",
                    json={
                        "start": entity["start"],
                        "end": entity["end"],
                        "section": yeee[k.lower()],
                        "note_code": {
                            "code": icd10["chapter"].replace(".", ""),
                            "type": "DIAG",
                            "note_id": note_request.json()["content"]["id"]
                        }
                    })
                    

```

```python
for edal, _values in codes.items():
        
    for icd in _values["icd10s"]:
        _annot = requests.post("http://127.0.0.1:5000/api/notes/add/clinicalcode",
                    json={
                        "coded_by": "OSHEAMM",
                        "note_code": {
                            "code": icd,
                            "type": "DIAG",
                            "note_id": id_table[edal]
                        }
                    })
    
    for opcs in _values["opcs4"]:
        _annot = requests.post("http://127.0.0.1:5000/api/notes/add/clinicalcode",
                    json={
                        "coded_by": "OSHEAMM",
                        "note_code": {
                            "code": opcs,
                            "type": "PROC",
                            "note_id": id_table[edal]
                        }
                    })
```

## License

This project is proudly licensed under the [GNU General Public License v3.0](https://raw.githubusercontent.com/KeironO/CLIVSECO/dev/LICENSE).