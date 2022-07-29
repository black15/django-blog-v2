from django import template
from ..models import Post

register = template.Library()

@register.simple_tag(name="all_posts") # to register the function as a simple tag
def total_posts():
        return Post.published_only.count()

@register.inclusion_tag('blog/recent_posts.html')
def recent_posts(num=4):
        recent = Post.published_only.order_by('publish')[:num]
        return {'recent_posts': recent}