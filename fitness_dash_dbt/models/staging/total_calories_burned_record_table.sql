{{ 
	config(
		materialized="table"
		)
}}

with total_calories_burned_record_table as (
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
		{{cast_unixepoch_to_datetime('local_date_time_start_time')}} as local_date_time_start_time,
		{{cast_unixepoch_to_datetime('local_date_time_end_time')}} as local_date_time_end_time,
		energy,
		row_number() over (partition by row_id order by loaded_at desc) as rn
	from {{ source('health_connect', 'total_calories_burned_record_table') }}
)
select * from total_calories_burned_record_table
where rn = 1 -- only choose the latest state from bronze