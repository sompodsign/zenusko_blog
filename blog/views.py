from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, HttpResponseRedirect
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, PostForm, EditPostForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def post(request):  # post an article
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('blog:post_list')
    else:
        post_form = PostForm()
    return render(request, 'blog/new_post.html',
                  context={'post_form': post_form,

                           })


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 5)  # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post_list.html',
                  {'posts': posts,
                   'tag': tag})


def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s"
            send_mail(subject, message, 'shampadsh@gmail.com', [cd['to']])
            if True:
                sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {
        'post': post,
        'form': form,
        'sent': sent, })


def post_find(request, y, m, d, p):
    post = get_object_or_404(Post, slug=p,
                             publish__year=y,
                             publish__month=m,
                             publish__day=d)
    if request.user.is_authenticated and request.user == post.author:
        return post
    else:
        post = get_object_or_404(Post, slug=p,
                                 status="published",
                                 publish__year=y,
                                 publish__month=m,
                                 publish__day=d)
        return post


def post_detail(request, year, month, day, post):
    post = post_find(request, year, month, day, post)
    # list of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            # save the comment to the database
            new_comment.save()
            messages.success(request, 'You have successfully added the comment. Thanks!')
            # return HttpResponseRedirect(request.path)
            return HttpResponseRedirect(request.path_info)
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   # 'new_comment': new_comment,
                   'comment_form': comment_form,

                   })


@login_required
def edit_post(request, id):
    post_obj = Post.objects.get(pk=id)
    data = {
        'title': post_obj.title,
        'subheading': post_obj.subheading,
        'body': post_obj.body,
        'status': post_obj.status,
    }
    if request.user == post_obj.author:
        if request.method == "POST":
            next_path = request.GET.get('next')
            form = EditPostForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                post_obj.title = cd['title']
                post_obj.subheading = cd['subheading']
                post_obj.body = cd['body']
                post_obj.status = cd['status']
                post_obj.update = True
                post_obj.save()
                if next_path is not None:
                    return redirect(next_path)
                else:
                    return redirect("blog:post_list")

    return render(request, 'blog/edit_post.html',
                  {'edit_post_form': EditPostForm(initial=data),
                   'post': post_obj,
                   })


@login_required
def delete_post(request, id):
    post_obj = Post.objects.get(pk=id)
    next_path = request.GET.get('next')
    if request.user == post_obj.author:
        post_obj.delete()
        if next_path is not None:
            return redirect(next_path)
        else:
            return redirect("blog:post_list")
    else:
        return redirect('blog:post_list')


def contact(request):
    return render(request, 'blog/contact.html')


@login_required
def author_posts(request):
    author = request.user
    posts = Post.objects.filter(author=author)
    return render(request,
                  'blog/author_posts.html',
                  {'posts': posts})
