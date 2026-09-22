{% macro cast_unixepoch_to_datetime(unixepoch) %}
    to_timestamp({{ unixepoch }} / 1000.0)
{% endmacro %}