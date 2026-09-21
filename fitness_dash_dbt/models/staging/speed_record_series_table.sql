select
    parent_key,
    speed,
    epoch_millis,
    {{cast_unixepoch_to_datetime(epoch_millis)}} as date_time
from {{ source('health_connect', 'speed_record_table') }};
