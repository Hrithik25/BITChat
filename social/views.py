from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.views import View
from social import models, forms
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Create your views here.


class Wall(LoginRequiredMixin, ListView):    # This view will list all the posts
    context_object_name = 'posts'
    template_name = 'social/wall.html'
    login_url = 'auth/login'

    def get_queryset(self):    # This function will show a user posts of his/her friends only
        friendIds = [friend.person2.id for friend in models.Friends.objects.filter(person1 = self.request.user)]
        friendIds = friendIds + [friend.person1.id for friend in models.Friends.objects.filter(person2 = self.request.user)]

        return models.Post.objects.filter(user__in = friendIds).order_by('-created_at')

        #return models.Post.objects.filter(
        #     (Q(user__person1 = self.request.user.pk) | Q(user__person2 = self.request.user.pk)) &
        #     ~Q(user = self.request.user)
        # ).order_by('-created_at')


class Home(LoginRequiredMixin, ListView):
    context_object_name='posts'
    template_name='social/home.html'
    login_url='auth/login'

    def get_queryset(self):
        return models.Post.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        data=super().get_context_data(*args, **kwargs)
        data['post_form']=forms.PostForm()
        return data

class Users(ListView):
    queryset = models.User.objects.all()
    context_object_name = 'users'
    template_name = 'social/users.html'



class Post(View):
    def post(self, request):
        # files are stored in request.FILES
        form=forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            # if commit=False then save method will only return an object and will not commit data to database
            post=form.save(commit=False)
            post.user=request.user
            form.save()

        return redirect('/home/')

class PostLike(View):
    model = models.Post   

    def post(self, request, pk):
        post = self.model.objects.get(pk = pk)  # This will fetch the post using pk and put it into post variable
        models.Like.objects.create(post = post, user = request.user)
        return HttpResponse(code = 204)


class PostComment(View):
    model = models.Post
    form = forms.PostCommentForm

    def post(self, request, pk):
        post = self.model.objects.get(pk = pk)
        form = self.form(request.POST)

        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponse(code = 204)

        return HttpResponse(code = 400)    

        
class AddFriend(View):
    model = models.FriendRequest

    def post(self, request, pk):
                
