{{
    config(
        materialized="table"
    )
}}

with ranked as (
    select
        row_id,
        health_data_category,
        app_id_priority_order,
        row_number() over (partition by health_data_category order by loaded_at desc) as rn
    from {{ source('health_connect', 'health_data_category_priority_table') }}
)

select
    row_id,
    health_data_category,
    app_id_priority_order
from ranked
where rn = 1