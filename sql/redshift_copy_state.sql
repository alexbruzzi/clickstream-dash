SELECT
  SUM(CASE WHEN state = 'failed' or state = 'success' or state = 'skipped' THEN 1 ELSE 0 END) as finished,
  SUM(CASE WHEN state = 'running' THEN 1 ELSE 0 END) as running,
  SUM(CASE WHEN state = 'queued' or state = 'scheduled' THEN 1 ELSE 0 END ) as future
FROM
  airflow_clickstream.airflow.task_instance
WHERE
  task_id LIKE 'redshift_copy_%';
