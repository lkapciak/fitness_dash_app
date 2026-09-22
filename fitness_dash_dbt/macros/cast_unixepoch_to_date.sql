{% macro cast_unixepoch_to_date(unixepoch) %}
    date '1970-01-01' + ({{ unixepoch }} * interval '1 day')
{% endmacro %}