{{
    config(
        materialized="incremental",
        incremental_strategy="delete+insert",
        unique_key=["parent_key", "epoch_millis"]
    )
}}

select
    parent_key,
    beats_per_minute,
    epoch_millis,
    {{cast_unixepoch_to_datetime(epoch_millis)}} as date_time
from {{ source('health_connect', 'heart_rate_record_series_table') }} src
{% if is_incremental() %}

where not exists (
    select 1
    from {{ this }} as existing
    where existing.parent_key = src.parent_key
      and existing.epoch_millis = src.epoch_millis
)

{% endif %};