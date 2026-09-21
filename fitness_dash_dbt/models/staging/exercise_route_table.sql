select
    parent_key,
    timestamp_millis,
    {{cast_unixepoch_to_local_datetime(timestamp_millis)}} as date_time,
    longitude,
    latitude,
    altitude,
from {{ source('health_connect', 'exercise_route_table') }};