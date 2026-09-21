select
    row_id,
    reader_app_id,
    writer_app_id,
    record_type,
    {{cast_unixepoch_to_local_datetime(read_time)}} as read_time,
    write_time
from {{ source('health_connect', 'read_access_logs_table') }};