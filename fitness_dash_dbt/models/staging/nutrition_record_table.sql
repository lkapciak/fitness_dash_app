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

    meal_type,
    meal_name,
    
    energy,

    protein,
    total_fat,
    saturated_fat,
    monounsaturated_fat,
    polyunsaturated_fat,
    unsaturated_fat,
    trans_fat,
    energy_from_fat,
    total_carbohydrate,
    sugar,

    dietary_fiber,
    iron,
    vitamin_a,
    vitamin_b6,
    vitamin_b12,
    vitamin_c,
    vitamin_e,
    vitamin_d,
    vitamin_k,
	{{cast_unixepoch_to_datetime('local_date_time_start_time')}} as local_date_time_start_time,
	{{cast_unixepoch_to_datetime('local_date_time_end_time')}} as local_date_time_end_time

from {{ source('health_connect', 'nutrition_record_table') }}
{% if is_incremental() %}
where {{ cast_unixepoch_to_local_datetime('last_modified_time') }}
    > (select max(last_modified_time) from {{ this }})
{% endif %}