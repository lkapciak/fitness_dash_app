select
	local_date::date as local_date,
	sum(energy)/1000 as kcal_consumed,
	sum(protein) as protein_consumed,
	sum(total_carbohydrate) as carbs_consumed,
	sum(sugar) as sugar_consumed,
	sum(total_fat) as fat_consumed,
	sum(dietary_fiber) as fiber_consumed
from {{ ref('nutrition_record_table') }}
group by local_date