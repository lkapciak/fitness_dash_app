select
    row_id,
	{{cast_unixepoch_to_date(epoch_days)}} as epoch_days,
    record_type_id
from {{ source('health_connect', 'activity_date_table') }};