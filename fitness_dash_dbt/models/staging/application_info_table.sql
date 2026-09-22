{{
    config(
        materialized="incremental",
        incremental_strategy="append"
    )
}}

select
    *
from {{ source('health_connect', 'application_info_table') }}
{% if is_incremental() %}
where row_id > (select max(row_id) from {{ this }})
{% endif %};