{% macro cast_unixepoch_to_local_datetime(unixepoch) %}
    to_timestamp({{ unixepoch }} / 1000.0) at time zone 'Europe/Warsaw'
{% endmacro %}