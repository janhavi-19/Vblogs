from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .models import Post, Categories
from django.urls import reverse_lazy
# Create your views here.

def home(request):
    post_model = Post.objects.all()
    categories_model = Categories.objects.all()
    return render(request,'home.html',{"Post":post_model,"Categories":categories_model})

#def blog-delete(DeleteView):
 #   post_model=Post.objects.get (id=id)
  #  post.delete()
   # message.success(request, 'Post has been deleted successfully')
    #return redirect('home')


class BlogUpdateView(UpdateView):
    model=Post
    fields = ['title', 'body']
    template_name = 'blog_update.html'
    success_url = reverse_lazy('home')
   
class BlogDeleteView(DeleteView):
    model=Post
    fields = '__all__'
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('home')

class BlogDetailView(DetailView):
    model=Post
    template_name = 'blog_details.html'
    
#class HomeView(ListView):
#     post_model = Post.objects.all()
#     categories_model = Categories.objects.all()
#     template_name = 'home.html'
    # context_object_name = 'home_list'    
    # template_name = 'home.html'
    # queryset = Individual.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super(HomeView, self).get_context_data(**kwargs)
    #     context['Post'] = Post.objects.all()
    #     # context['Category_List'] = Categories.objects.all()
    #     return context


