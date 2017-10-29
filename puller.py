"""
Fetch data from Airflow's metadata database.
"""

import datetime
import os
import time

import pandas as pd
import psycopg2

AIRFLOW_POSTGRES = os.environ['AIRFLOW_POSTGRES']

conn = psycopg2.connect(AIRFLOW_POSTGRES)

all_dfs = {}

queries = [
    (
        'task_instance_state_groups',
        'select state, count(*) from task_instance group by state;',
    ),
    (
        'task_instance_count_by_day',
        open('sql/task_instance_count_by_day.sql').read(),
    ),
    (
        'redshift_copy_state',
        open('sql/redshift_copy_state.sql').read(),
    )
]

for filename, _ in queries:
    all_dfs[filename] = pd.DataFrame()

i = 0

#task instance state groups over a 5 minute span.
while i <= 5:
# for i in range(2):
    print(f'run {i}')
    print(filename)

    for filename, query in queries:
        ts = datetime.datetime.now()
        df = pd.read_sql(query, conn)
        df['timestamp'] = ts

        all_dfs[filename] = all_dfs[filename].append(df, ignore_index=True, verify_integrity=True)

        all_dfs[filename].to_json(f'data/{filename}.json')

    time.sleep(60)
    i += 1
