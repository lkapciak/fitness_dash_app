{{ 
	config(
		materialized="incremental", 
		incremental_strategy="delete+insert",
		unique_key="row_id"
		)
}}

select 
	row_id,
	uuid,
	{{cast_unixepoch_to_local_datetime('last_modified_time')}} as last_modified_time,
	client_record_id,
	client_record_version,
	device_info_id,
	app_info_id, 
	recording_method,
	dedupe_hash,
	{{cast_unixepoch_to_date('local_date')}} as local_date,
	{{cast_unixepoch_to_datetime('local_date_time')}} as local_date_time,
	round(100*height) as height
from {{ source('health_connect', 'height_record_table') }}
{% if is_incremental() %}
where {{ cast_unixepoch_to_local_datetime('last_modified_time') }}
    > (select max(last_modified_time) from {{ this }})
{% endif %}
