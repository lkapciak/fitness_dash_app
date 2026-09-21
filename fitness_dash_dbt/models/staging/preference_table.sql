select
    *
from {{ source('health_connect', 'preference_table') }};