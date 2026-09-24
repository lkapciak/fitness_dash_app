with total_calories_burned as (
    select
        local_date,
        sum(energy)/1000 as total_kcal
    from {{ref('total_calories_burned_record_table')}}
    group by local_date
),
active_calories_burned as (
    select
        local_date,
        sum(energy)/1000 as active_kcal
    from {{ref('active_calories_burned_record_table')}}
    group by local_date
)
select 
    * 
from total_calories_burned tcb
left join active_calories_burned acb
    using(local_date)
order by local_date;