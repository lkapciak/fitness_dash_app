select
    *
from {{ source('health_connect', 'health_data_category_priority_table') }};