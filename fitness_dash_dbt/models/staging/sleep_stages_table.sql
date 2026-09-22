{{
    config(
        materialized="incremental",
        incremental_strategy="append"
    )
}}

select
    parent_key,
    {{cast_unixepoch_to_datetime(stage_start_time)}} as stage_start_time,
    {{cast_unixepoch_to_datetime(stage_end_time)}} as stage_end_time,
    stage_type
from {{ source('health_connect', 'sleep_stages_table') }}

{% if is_incremental() %}
where not exists (
    select 1
    from {{ this }} s
    where s.parent_key = sleep_stages_table.parent_key
      and s.stage_start_time = {{ cast_unixepoch_to_datetime(stage_start_time) }}
      and s.stage_end_time = {{ cast_unixepoch_to_datetime(stage_end_time) }}
      and s.stage_type = sleep_stages_table.stage_type
)
{% endif %}