{{
    config(
        materialized="incremental",
        incremental_strategy="append"
    )
}}

select 
    *
from {{ source('health_connect', 'device_data_sources_table') }}
{% if is_incremental() %}
where row_id > (select max(row_id) from {{ this }})
{% endif %};