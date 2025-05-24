from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *

# Create your views here.

def mainpage(request) :
     return render(request, 'main/mainpage.html');

def secondpage(request) :
     posts = Post.objects.all()
     return render(request, 'main/secondpage.html', {'posts' : posts});


def new_post(request) :
     return render(request, 'main/new-post.html')

def delete_comment(request, id) :
     comment = get_object_or_404(Comment, pk = id)
     post_id = comment.post.id
     delete_comment = Comment.objects.get(pk=id)
     delete_comment.delete()
     return redirect('main:detail', post_id)

def detail(request, id) :
     post = get_object_or_404(Post, pk=id)
     if request.method =='GET':
          comments = Comment.objects.filter(post=post)
          return render(request, 'main/detail.html', {'post' : post, 'comments':comments})

     elif request.method == 'POST':
          new_comment = Comment()
          new_comment.post = post
          new_comment.writer = request.user
          new_comment.content = request.POST['content']
          new_comment.pub_date = timezone.now()
          new_comment.save()
          return redirect('main:detail', id)


def edit(request, id):
     edit_post = Post.objects.get(pk=id)
     return render(request, 'main/edit.html',  {"post": edit_post})

def update(request, id):
     update_post = Post.objects.get(pk=id)
     if request.user.is_authenticated and request.user == update_post.writer:
          update_post.title = request.POST['title']
          update_post.feeling = request.POST['feeling']
          update_post.content = request.POST['content']
          update_post.status = request.POST['status']
          update_post.created_at = timezone.now()

          if request.FILES.get('image'):
               update_post.image = request.FILES.get('image')

          update_post.tags.clear()
          lines = update_post.content.split('\n')
          tag_list = []
          for line in lines:
               words = line.split()
               for w in words:
                    if w.startswith('#') and len(w) > 1:
                         tag_list.append(w[1:])
          tag_list = list(set(tag_list))
          for t in tag_list:
               tag, _ = Tag.objects.get_or_create(name=t)
               update_post.tags.add(tag)

          update_post.save()
          return redirect('main:detail', update_post.id)
     return redirect ('accounts:login', update_post.id)

def delete(request, id):
     delete_post = Post.objects.get(pk=id)
     delete_post.delete()
     return redirect('main:secondpage')

def create(request):
     if request.user.is_authenticated:
          new_post = Post()

          new_post.title = request.POST['title']
          new_post.feeling = request.POST['feeling']
          new_post.content = request.POST['content']
          new_post.status = request.POST['status']
          new_post.created_at = timezone.now()
          new_post.image = request.FILES.get('image')
          new_post.writer=request.user
          new_post.save()

          lines = new_post.content.split('\n')
          tag_list = []

          for line in lines :
               words = line.split()
               for w in words:
                    if w.startswith('#') and len(w) > 1:  # '#'만 있는 경우 제외
                         tag_list.append(w[1:])  # '#' 제거 후 저장

          # 중복 제거
          tag_list = list(set(tag_list))

          for t in tag_list:
               tag, _ = Tag.objects.get_or_create(name=t)
               new_post.tags.add(tag)

          return redirect('main:detail', new_post.id)
     
     else:
          return redirect('accounts:login')
     
def tag_list(request):
     tags = Tag.objects.all()
     return render(request, 'main/tag-list.html', {'tags':tags})

def tag_posts(request, tag_id):
     tag=get_object_or_404(Tag, id=tag_id)
     posts=tag.posts.all()
     return render(request, 'main/tag-post.html', {
          'tag' : tag,
          'posts' : posts
     })

def likes (request, post_id):
     post = get_object_or_404(Post, id = post_id)
     if request.user in post.like.all():
          post.like.remove(request.user)
          post.like_count -=1
          post.save()

     else :
          post.like.add(request.user)
          post.like_count +=1
          post.save()
     
     return redirect ('main:detail', post.id)