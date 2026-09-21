select
    parent_key,
    rate,
    epoch_millis,
    {{cast_unixepoch_to_datetime(epoch_millis)}} as epoch_millis
from {{ source('health_connect', 'steps_cadence_record_table') }};