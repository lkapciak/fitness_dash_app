select
    *
from {{ source('health_connect', 'nutrition_record_table') }};