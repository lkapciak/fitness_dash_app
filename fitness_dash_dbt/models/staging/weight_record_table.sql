SELECT 
	row_id,
	hex(uuid) as uuid,
	{{cast_unixepoch_to_local_datetime(last_modified_time)}} as last_modified_time,
	client_record_id,
	client_record_version,
	device_info_id,
	app_info_id, 
	recording_method,
	hex(dedupe_hash) as dedupe_hash,
	{{cast_unixepoch_to_date(local_date)}} as local_date,
	{{cast_unixepoch_to_datetime(local_date_time)}} as local_date_time,
	round(weight) as weight,
	round(weight)/1000 as weight_kg
from {{ source('health_connect', 'weight_record_table') }};
