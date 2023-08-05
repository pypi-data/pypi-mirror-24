{%- extends 'markdown.tpl' -%}
{%- block input scoped -%}
{:.input}{{ super() }}
{%- endblock input %}

{% block output %}
{:.output}{{ super() }}
{% endblock output %}

{% block display_data %}
{:.display_data}{{ super() | replace()}}
{% endblock display_data %}

{% block execute_result %}
{:.execute_result}{{ super() }}
{% endblock execute_result %}
