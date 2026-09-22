{{
    config(
        materialized="incremental",
        incremental_strategy="append"
    )
}}

select
    row_id,
    {{ cast_unixepoch_to_date(epoch_days) }} AS epoch_days,
    record_type_id
from {{ source('health_connect', 'activity_date_table') }}
{% if is_incremental() %}
where row_id > (select max(row_id) from {{ this }})
{% endif %}