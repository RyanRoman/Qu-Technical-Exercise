import json, pathlib
DATA=json.loads((pathlib.Path(__file__).parents[3]/'data/mock_timeseries.json').read_text())
def query(duid:str,circuit:int,start:str,end:str):
    return [row for row in DATA if row['duid']==duid and row['circuit_number']==circuit]