from turtle import pos
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count, Q

from blog.forms import SharePostViaEmail, CommentForm
from .models import Post, Comment

# Create your views here.
# class PostsList(ListView):
#         queryset                = Post.published_only.all().order_by('publish')
#         context_object_name     = 'posts'
#         paginate_by             = 3
#         template_name           = 'blog/home.html'

def posts_list(request, tag_slug=None):
        context = {}
        
        _tag = None
        published_posts         = Post.published_only.all().order_by('publish')
        alltags                 = Post.tags.all() 

        if tag_slug:
                _tag = get_object_or_404(
                        Tag,
                        slug=tag_slug,
                )
                published_posts         = Post.published_only.filter(tags__in=[_tag]).order_by('publish')

        paginator = Paginator(published_posts, 3) # 3 posts in each page

        page = request.GET.get('page')
        try:
                posts = paginator.page(page)
        except PageNotAnInteger:
                # If page is not an integer deliver the first page
                posts = paginator.page(1)
        except EmptyPage:
                # If page is out of range deliver last page of results
                posts = paginator.page(paginator.num_pages)

        context['posts']        = posts
        context['page']         = page
        context['tag']          = _tag
        context['tags']         = alltags
        
        return render(request, 'blog/home.html', context)

# Search function 
def search_posts(request):
        context = {}
        try:
                query   = request.GET['search']
                posts   = Post.published_only.filter(Q(title__icontains=query) | Q(slug__icontains=query) | Q(body__icontains=query) | Q(author__username__icontains=query) | Q(tags__name__icontains=query))
                
                if posts:
                        context['filtered_posts'] = posts
                        context['query']          = query
                        return render(request, 'blog/home.html', context)
                else :
                        return redirect('blog:post_list')
        except KeyError:
                return redirect('blog:post_list')

# List post detail in one page 
def post_details(request, slug, year, month, day):
        context = {}

        post    = get_object_or_404(
                Post,
                slug            = slug,
                status          = 'published',
                publish__year   = year,
                publish__month  = month,
                publish__day    = day,
        )
        # List of active comments for this post | commentx is the related_name argument in post field in the Comment Module
        comments        = post.commentx.filter(active=True)
        comment_add     = None 

        if request.method == "POST":
                form = CommentForm(request.POST)
                if form.is_valid():
                        name    = form.cleaned_data['name']
                        email   = form.cleaned_data['email']
                        body    = form.cleaned_data['body']

                        # Comment.objects.create(
                        #         Post,
                        #         name  = name,
                        #         email = email,
                        #         body  = body
                        # )
                        comment_add = form.save(commit=False)
                        comment_add.post = post
                        comment_add.save()
        else:
                form = CommentForm()

        post_tags_ids   = post.tags.values_list("id", flat=True)
        similar_posts   = Post.published_only.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts   = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
        
        context['post']                 = post
        context['form']                 = form
        context['comments']             = comments
        context['comment']              = comment_add
        context['similar_posts']        = similar_posts

        return render(request, 'blog/post/details.html', context)

# Share post by E-mail 
def share_post(request, post_id):
        context = {}

        post    = get_object_or_404(
                Post,
                id=post_id,
                status='published'
        )
        sent = False

        if request.method == 'POST':
        # Form was submitted
                form = SharePostViaEmail(request.POST)
                if form.is_valid():
                # Form fields are valid
                        cd = form.cleaned_data
                        post_url = request.build_absolute_uri( post.get_absolute_url() )
                        subject         = f"{cd['name']} shared a post with you"
                        message         = f"You can read about {post.title} at {post_url}"\
                                          f" {cd['name']}'s comments : {cd['comments']}"
                        send_mail(subject, message, request.user.email,[ cd['to'] ])
                        sent = True
        else:
        # If it is a get request
                form = SharePostViaEmail()
        
        context['post']  = post
        context['form']  = form
        context['sent']  = sent

        return render(request, 'blog/post/share.html', context)
