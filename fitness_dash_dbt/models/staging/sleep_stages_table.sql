select
    parent_key,
    {{cast_unixepoch_to_datetime(stage_start_time)}} as stage_start_time,
    {{cast_unixepoch_to_datetime(stage_end_time)}} as stage_end_time,
    stage_type
from {{ source('health_connect', 'sleep_stages_table') }};