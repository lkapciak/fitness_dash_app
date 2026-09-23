{{
    config(
        materialized="incremental",
        incremental_strategy="append"
    )
}}

select distinct
    parent_key,
    {{cast_unixepoch_to_local_datetime('stage_start_time')}} as stage_start_time,
    {{cast_unixepoch_to_local_datetime('stage_end_time')}} as stage_end_time,
    stage_type
from {{ source('health_connect', 'sleep_stages_table') }} src

{% if is_incremental() %}
where not exists (
    select 1
    from {{ this }} s
    where s.parent_key = src.parent_key
      and s.stage_start_time = {{ cast_unixepoch_to_local_datetime('src.stage_start_time') }}
      and s.stage_end_time = {{ cast_unixepoch_to_local_datetime('src.stage_end_time') }}
      and s.stage_type = src.stage_type
)
{% endif %}