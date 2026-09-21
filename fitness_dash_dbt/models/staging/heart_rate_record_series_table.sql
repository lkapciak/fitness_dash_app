select
    parent_key,
    beats_per_minute,
    epoch_millis,
    {{cast_unixepoch_to_datetime(epoch_millis)}} as date_time
from {{ source('health_connect', 'heart_rate_record_series_table') }};