select
    parent_key,
    {{cast_unixepoch_to_datetime(segment_start_time)}} as segment_start_time,
    {{cast_unixepoch_to_datetime(segment_end_time)}} as segment_end_time,
    segment_type,
    repetitions_count,
    weight_grams,
    set_index,
    rate_of_perceived_exertion
from {{ source('health_connect', 'exercise_segments_table') }};