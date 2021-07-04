from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment  # Comment追加
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm  # CommentForm追加
from django.shortcuts import redirect
# Create your views here.


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('comment_detail', pk=comment.pk)
    else:
        form = CommentForm()

    print(post)

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': comments})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    form = CommentForm(request.POST)

    print(comment)
    return render(request, 'blog/comment_detail.html', {'comment': comment})
