{{
    config(
        materialized="incremental",
        incremental_strategy="delete+insert",
        unique_key=["parent_key", "timestamp_millis"]
    )
}}

select
    parent_key,
    timestamp_millis,
    {{cast_unixepoch_to_local_datetime('timestamp_millis')}} as date_time,
    longitude,
    latitude,
    altitude
from {{ source('health_connect', 'exercise_route_table') }} src
{% if is_incremental() %}

where not exists (
    select 1
    from {{ this }} as existing
    where existing.parent_key = src.parent_key
      and existing.timestamp_millis = src.timestamp_millis
)

{% endif %}