{{
    config(
        materialized="table"
    )
}}

with ranked as (
    select
        *,
        row_number() over (partition by key order by loaded_at desc) as rn
    from {{ source('health_connect', 'preference_table') }}
)
select
    key,
    value
from ranked
where rn = 1