{{
    config(
        materialized="incremental",
        incremental_strategy="append"
    )
}}

select
    parent_key,
    rate,
    epoch_millis,
    {{cast_unixepoch_to_datetime('epoch_millis')}} as date_time
from {{ source('health_connect', 'steps_cadence_record_table') }} src

{% if is_incremental() %}
where not exists (
    select 1
    from {{ this }} s
    where s.parent_key = src.parent_key
      and s.epoch_millis = src.epoch_millis
)
{% endif %}