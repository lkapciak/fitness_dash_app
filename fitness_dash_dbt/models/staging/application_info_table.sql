select
    *
from {{ source('health_connect', 'application_info_table') }};