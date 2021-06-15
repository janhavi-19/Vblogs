from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Categories, Comment, TrendingEmailNotification, Thoughts
from .forms import PostForm, CategoriesForm, UpdatePostForm, AddThoughtsView, AddComment  
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from hitcount.views import HitCountDetailView
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template
from django.conf import settings
from datetime import datetime,date,timedelta, timezone
# Create your views here.
trending_posts_per_user = []
trending_posts_user_id = []
trending_posts_email = []

  
def home(request):
    today_date = datetime.today() - timedelta(days=7)
    post_model = Post.objects.all().order_by('-published_date')[:4]
    trending_posts = Post.objects.all().order_by('-hit_count_generic__hits')[:3]
    trending_posts_notifications = TrendingEmailNotification.objects.filter(date_last_sent=today_date)
    for trending_post in trending_posts:
        if trending_post.author_id == request.user.id:
            trending_posts_per_user.append(trending_post)
    list_count = len(trending_posts_per_user)
    if trending_posts_notifications.count() > 0:
        send_email_from_app(request)
    categories_model = Categories.objects.all()
    return render(request,'home.html',{"Post":post_model,"Categories":categories_model,"trending_posts":trending_posts,"trending_posts_notifications": trending_posts_notifications})


# class HomeView(ListView):
#     post_model = Post.objects.all()
#     categories_model = Categories.objects.all()
#     template_name = 'home.html'
#     ordering = ['-id'] order by id

    # context_object_name = 'home_list'    
    # template_name = 'home.html'
    # queryset = Individual.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     context['Post'] = Post.objects.all()
    #     # context['Category_List'] = Categories.objects.all()
    #     return context


class BlogDetailView(HitCountDetailView):
    model=Post
    template_name = 'blog_details.html'
    count_hit=True

    def get_context_data(self, *args, **kwargs):
        context = super (BlogDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        similarid=Post.objects.values('author_id').filter(id=self.kwargs['pk'])
        similarBlogs = Post.objects.filter(author_id__in=similarid)

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context["liked"] = liked
        context['similarBlogs'] = similarBlogs

        context.update({
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        })

        return context

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    # fields = '__all__' 
    # if you don't want all
    # fields = ('title','body')

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = UpdatePostForm

class DeletePostView(DeleteView):
    model=Post
    fields = '__all__'
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('home')

class AddCategoryView(CreateView):
    model = Categories
    template_name = 'add_category.html'
    form_class = CategoriesForm

    def form_valid(self, form):
        form.instance.created_by_id = self.request.user.id
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('home')


def CategoryView(request, cats):
    category_posts = Post.objects.filter(Categories__icontains = cats.replace('-',' '))
    # category_posts = Post.objects.all()
    return render(request, 'categories.html',{'cats':cats.title().replace('-',' '), 'category_posts': category_posts})

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False 
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('blog-detail', args=[str(pk)]))

def AboutView(request):
    return render(request,'about_us.html',{})

def ContactUsView(request):
    return render(request,'contactus.html',{})

class AllBlogsView(ListView):
    model = Post
    template_name = 'all_blogs.html'

def searchCategory(request):
    query=request.GET['query']  
    category_meta_titles = Categories.objects.values('title').filter(Meta_Titles__icontains= query)
    if category_meta_titles.count()>0:
        category_posts = Post.objects.filter(Categories__icontains = category_meta_titles)
    else :
        category_posts = Post.objects.filter(Categories__icontains = query)
    return render(request, 'searchCategory.html',{'query':query.title(), 'category_posts': category_posts})

def search(request):
    query=request.GET.get('query')
    #query2=request.GET.get('query').split()
    if len(query)>78:
        allPosts=Post.objects.none()
    else: 
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsBody= Post.objects.filter(body__icontains=query)
        allPostsAuthorL= Post.objects.filter(author__last_name__icontains=query)
        allPostsAuthor= Post.objects.filter(author__first_name__icontains=query)
        allPostsCategories=Post.objects.filter(Categories__icontains=query)
        #qset1 =  reduce(operator.__or__, [Q(author__first_name__icontains=qu) | Q(author__last_name__icontains=qu) for qu in query])
       # allPostFull=Post.objects.filter(qset1).distinct()
        allPosts=allPostsTitle.union(allPostsBody,allPostsAuthor,allPostsAuthorL,allPostsCategories)
    params={'allPosts': allPosts, 'query': query}
    return render(request,'search.html',params)
    
class AddCommentView(CreateView):
    model=Comment
    template_name = 'add_comment.html'
    form_class = AddComment  
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog-detail', kwargs={'pk': self.kwargs['pk']})

class ThoughtsView(CreateView):
    model=Thoughts
    template_name = 'add_thoughts.html'
    form_class = AddThoughtsView 
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog-detail', kwargs={'pk': self.kwargs['pk']})

def ContactUsView(request):
    if request.method =="POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name'] 
        email = request.POST['email']
        review = request.POST['review']
        send_mail(
            'Review By :- ' + first_name +''+ last_name, #subject
            review, #body
            email, #from email
            ['janhavikalwar19@gmail.com','akshayamohan.2401@gmail.com','nikita.emberi123@gmail.com',''] #to email
        )
        return redirect('home')
    else:
        return render(request,'contactus.html',{})


def send_email_from_app(request):
    html_tpl_path = 'email_templates/notifications.html'
    today_date = datetime.today() - timedelta(days=7)
    trending_posts = Post.objects.all().order_by('-hit_count_generic__hits')[:3]
    trending_posts_email =  TrendingEmailNotification.objects.filter(date_last_sent=today_date).select_related('user')
    for i in trending_posts_email:
        user_id = i.user.id
        email_html_template = get_template(html_tpl_path).render({"trending_posts":trending_posts, "user_id":user_id})
        receiver_email = i.user.email
        email_msg = EmailMessage('Greetings from vBlogs!',
                                email_html_template, 
                                settings. APPLICATION_EMAIL,
                                [receiver_email],
                                reply_to = [settings.APPLICATION_EMAIL]
                                )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently = False)
        TrendingEmailNotification.objects.filter(user_id=user_id).update(date_last_sent = date.today())

class Overview(HitCountDetailView):
    model=Post
    template_name = 'overview.html'

    def get_context_data(self, *args, **kwargs):
        l = []
        category_count = []
        context = super (Overview, self).get_context_data(*args, **kwargs)
        post = get_object_or_404(Post, id = self.kwargs['pk'])
        post_id = self.kwargs['pk']
        trending_posts = Post.objects.all().order_by('-hit_count_generic__hits')[:3]
        for trending_post in trending_posts:
            if trending_post.id == post_id:
                l.append(trending_post)
                break
        total_likes = post.total_likes()
        # likes = post_likes.objects.filter(post_id = self.kwargs['pk'])
        context["post"] = post
        context['likes'] = total_likes
        context["trending_posts"] = trending_posts
        context["list_count"] = len(l)
        context["l"] = l
        # context["likes"] = likes
        # context["trending_posts_count"] = trending_posts.count()
        return context
