import requests
import json
from collections import namedtuple
from contextlib import closing
import sqlite3

from prefect import task, flow  # Cambio en los imports

# Las tasks (@task) se mantienen igual
@task
def get_complaint_data():
    r = requests.get("https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/", params={'size':10})
    response_json = json.loads(r.text)
    return response_json['hits']['hits']

@task
def parse_complaint_data(raw):
    complaints = []
    Complaint = namedtuple('Complaint', ['data_received', 'state', 'product', 'company', 'complaint_what_happened'])
    for row in raw:
        source = row.get('_source')
        this_complaint = Complaint(
            data_received=source.get('date_received'),
            state=source.get('state'),
            product=source.get('product'),
            company=source.get('company'),
            complaint_what_happened=source.get('complaint_what_happened')
        )
        complaints.append(this_complaint)
    return complaints

@task
def store_complaints(parsed):
    create_script = 'CREATE TABLE IF NOT EXISTS complaint (timestamp TEXT, state TEXT, product TEXT, company TEXT, complaint_what_happened TEXT)'
    insert_cmd = "INSERT INTO complaint VALUES (?, ?, ?, ?, ?)"
    
    with closing(sqlite3.connect("cfpbcomplaints.db")) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(create_script)  # Usa execute en lugar de executescript
            cursor.executemany(insert_cmd, [tuple(complaint) for complaint in parsed])  # Convierte namedtuples a tuplas
            conn.commit()

# Define el flujo con @flow
@flow
def my_etl_flow():
    raw = get_complaint_data()
    parsed = parse_complaint_data(raw)
    store_complaints(parsed)

# Ejecuta el flujo
if __name__ == "__main__":
    my_etl_flow()