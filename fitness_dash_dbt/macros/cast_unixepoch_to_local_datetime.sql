{% macro cast_unixepoch_to_local_datetime(unixepoch) %}
    strftime('%Y-%m-%d %H:%M:%S', datetime({{ unixepoch }}/1000, 'unixepoch', 'localtime'))
{% endmacro %}