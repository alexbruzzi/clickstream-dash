SELECT
    date_trunc('day', start_date) as d,
    count(1)
FROM
    airflow.task_instance
GROUP BY d
ORDER BY 1 DESC
LIMIT 7;
