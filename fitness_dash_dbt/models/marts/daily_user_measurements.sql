with 
daily_basal_metabolic_rate as (
	select
		cast(local_date as date) as local_date,
		avg(basal_metabolic_rate) as avg_basal_metabolic_rate
	from {{ ref('basal_metabolic_rate_record_table') }}
	group by local_date
	order by 1
),
daily_oxygen_saturation as (
	select
		cast(local_date as date) as local_date,
		avg(percentage) as avg_oxygen_saturation
	from {{ ref('oxygen_saturation_record_table') }}
	group by local_date
),
daily_height as (
	select
	    d.local_date,
	    h.height
	from 
		(
		    select generate_series(
		        min(cast(local_date as date)),
		        current_date,
		        INTERVAL '1 day'
		    )::date AS local_date
		    from {{ ref('height_record_table') }}
		) d
	left join lateral (
	    select height
	    from {{ ref('height_record_table') }} h
	    where h.local_date::date <= d.local_date
	    order by h.local_date desc
	    limit 1
	) h on TRUE
	order by d.local_date
),
daily_body_fat as (
	select
		cast(local_date as date) as local_date,
		avg(percentage) as avg_body_fat
	from {{ ref('body_fat_record_table') }}
	group by local_date
),
daily_resting_heart_rate as (
	select
		cast(local_date as date) as local_date,
		avg(beats_per_minute) as avg_resting_bpm
	from {{ ref('resting_heart_rate_record_table') }}
	group by local_date
),
daily_weight as (
	select
		cast(local_date as date) as local_date,
		avg(weight_kg) as avg_weight
	from {{ ref('weight_record_table') }}
	group by local_date
),

daily_user_measurements as (
	select * 
	from daily_basal_metabolic_rate
	full join daily_oxygen_saturation using(local_date)
	full join daily_height using(local_date)
	full join daily_body_fat using(local_date)
	full join daily_resting_heart_rate using(local_date)
	full join daily_weight using(local_date)
)
select * from daily_user_measurements