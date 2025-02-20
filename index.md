---
layout: home
---
Welcome to my automated TOI blog!
{% for post in site.posts %}
  <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
  <p>{{ post.date | date_to_string }}</p>
  <p>{{ post.content | truncatewords: 30 }}</p>
{% endfor %}
