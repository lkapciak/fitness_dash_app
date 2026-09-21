select 
    *
from {{ source('health_connect', 'device_data_sources_table') }};