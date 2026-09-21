{% macro cast_unixepoch_to_date(unixepoch) %}
    replace(date({{ unixepoch }} * 86400, 'unixepoch'), '-', '-')
{% endmacro %}