with sleep_stages as (
    select
        sst.parent_key,
        sum(sst.stage_end_time - sst.stage_start_time) 
            filter (where ssm.sleep_stage_name = 'Wake-up') as wake_ups_time,
        sum(sst.stage_end_time - sst.stage_start_time) 
            filter (where ssm.sleep_stage_name = 'Light') as light_sleep_time,
        sum(sst.stage_end_time - sst.stage_start_time) 
            filter (where ssm.sleep_stage_name = 'Deep') as deep_sleep_time,
        sum(sst.stage_end_time - sst.stage_start_time) 
            filter (where ssm.sleep_stage_name = 'REM') as rem_stage_time,
        
        count(*) filter (where ssm.sleep_stage_name = 'Wake-up') as total_wake_ups_count,
        count(*) filter (where ssm.sleep_stage_name = 'Light') as total_light_sleep_count,
        count(*) filter (where ssm.sleep_stage_name = 'Deep') as total_deep_sleep_count,
        count(*) filter (where ssm.sleep_stage_name = 'REM') as total_rem_stage_count

    from {{ref('sleep_stages_table')}} sst
    left join {{ref('sleep_stages_map')}} ssm
        on ssm.sleep_stage_id = sst.stage_type
    group by parent_key
	order by parent_key
),
daily_user_sleep as (
	select
	    ssrt.row_id,
		ssrt.local_date_time_end_time::date - 1 as attribution_date,
		ssrt.local_date_time_start_time as sleep_start_time,
		ssrt.local_date_time_end_time as sleep_end_time,
		ssrt.local_date_time_end_time - ssrt.local_date_time_start_time as sleep_duration,
	    
	    ss.wake_ups_time,
	    ss.light_sleep_time,
	    ss.deep_sleep_time,
	    ss.rem_stage_time,
	    
	    ss.total_wake_ups_count,
	    ss.total_light_sleep_count,
	    ss.total_deep_sleep_count,
	    ss.total_rem_stage_count
	
	from {{ref('sleep_session_record_table')}} ssrt
	left join sleep_stages ss
	on ss.parent_key = ssrt.row_id
)
select * from daily_user_sleep