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
    {{cast_unixepoch_to_datetime(epoch_millis)}} as date_time
from {{ source('health_connect', 'steps_cadence_record_table') }}

{% if is_incremental() %}
where not exists (
    select 1
    from {{ this }} s
    where s.parent_key = steps_cadence_record_table.parent_key
      and s.epoch_millis = steps_cadence_record_table.epoch_millis
)
{% endif %}