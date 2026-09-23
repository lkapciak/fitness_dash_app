{{
    config(
        materialized="incremental",
        incremental_strategy="delete+insert",
        unique_key=["parent_key", "segment_start_time", "segment_end_time"]
    )
}}

select
    parent_key,
    {{cast_unixepoch_to_local_datetime('segment_start_time')}} as segment_start_time,
    {{cast_unixepoch_to_local_datetime('segment_end_time')}} as segment_end_time,
    segment_type,
    repetitions_count,
    weight_grams,
    set_index,
    rate_of_perceived_exertion
from {{ source('health_connect', 'exercise_segments_table') }} src

{% if is_incremental() %}

where not exists (
    select 1
    from {{ this }} as existing
    where existing.parent_key = src.parent_key
      and existing.segment_start_time = {{ cast_unixepoch_to_local_datetime('src.segment_start_time') }}
      and existing.segment_end_time = {{ cast_unixepoch_to_local_datetime('src.segment_end_time') }}
)

{% endif %}