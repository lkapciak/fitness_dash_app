{% macro cast_unixepoch_to_datetime(unixepoch) %}
    strftime('%Y-%m-%d %H:%M:%S', datetime({{ unixepoch }}/1000, 'unixepoch'))
{% endmacro %}