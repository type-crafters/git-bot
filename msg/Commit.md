{# 
Variables: 
    - str repository: El nombre del repositorio que lanzó el evento. 
    - str platform: La plataforma de Git que aloja el repositorio (GitHub, GitLab, etc.) 
    - str branch: El nombre de la rama donde se realizó el commit. 
    - str author: El nombre del autor que realizó el push a la rama. 
    - list[str] commits: Una lista de diccionarios conteniendo información de cada commit en el push. 
#}

## 🔔 Nuevo commit en {{ repository }}

🏗️ Plataforma: {{ platform }}
📂 Branch: `{{ branch }}`
👤 Autor: {{ author }}
📝 Commits ({{ commits | length }}):

{% for commit in commits[:5] -%}
* `{{ commit.id[:7] }}` - {{ commit.message }} ([{{ commit.author.name }}](mailto:{{ commit.author.email }}))
{% endfor %}

{% if commits | length > 5 %}
...y {{ commits | length - 5 }} commit{% if commits | length > 6 %}s{%endif%} más.
{% endif %}

🔗 [Ver cambios]({{ commit_url }})
