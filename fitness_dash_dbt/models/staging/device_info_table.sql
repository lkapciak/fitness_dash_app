select
    *
from {{ source('health_connect', 'device_info_table') }};