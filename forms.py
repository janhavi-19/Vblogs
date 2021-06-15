from django import forms
from .models import Post,Categories,Profile, Thoughts,Comment
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

# choices = [('education','education'),('sports','sports')]
choices = Categories.objects.all().values_list('title','title')
choice_list = []
for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm):
    class Meta : 
        model = Post
        fields = ('title','author','Categories','Poster','body','snippet')

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Add Title'}),
            'author' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'user name','id' : 'correct_user','type':'hidden'}),
            # 'author' : forms.Select(attrs={'class': 'form-control'}),
            'Categories' : forms.CheckboxSelectMultiple(choices=choice_list,attrs={'class' : 'form-check-input'}),
            'body' : forms.Textarea(attrs={'class': 'form-control'}),
            'snippet' : forms.Textarea(attrs={'class': 'form-control','placeholder':"Add a liitle text to display on post card."}),
        }

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author','Categories','Poster','body','snippet')
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Add Title'}),
            'author' : forms.TextInput(attrs={'class': 'form-control','placeholder' : 'user name','id' : 'correct_user','type':'hidden'}),
            'Categories' : forms.CheckboxSelectMultiple(choices=choice_list,attrs={'class' : 'form-check-input'}),
            'body' : forms.Textarea(attrs={'class': 'form-control'}),
            'snippet' : forms.Textarea(attrs={'class': 'form-control','placeholder':"Add a liitle text to display on post card."}),
        }

class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','Profile_pic','personal_website_url','twitter_url','instagram_url','facebook_url','linkedin_url')

        widgets= {
            'bio' : forms.Textarea(attrs={'class': 'form-control','placeholder':'Add Title'}),
            # 'Profile_pic' : forms.TextInput(attrs={'class': 'form-control'}),
            'personal_website_url' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'https://'}),
            'twitter_url' : forms.TextInput(attrs={'class' : 'form-control','placeholder':'https://'}),
            'instagram_url' : forms.TextInput(attrs={'class': 'form-control','placeholder':'https:'}),
            'facebook_url' : forms.TextInput(attrs={'class': 'form-control','placeholder':"https://"}),
            'linkedin_url' : forms.TextInput(attrs={'class': 'form-control','placeholder':"https://"}),
        }

class UpdateProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','Profile_pic','personal_website_url','twitter_url','instagram_url','facebook_url','linkedin_url')

        widgets= {
            'bio' : forms.Textarea(attrs={'class': 'form-control','placeholder':'Add Title'}),
            # 'Profile_pic' : forms.TextInput(attrs={'class': 'form-control'}),
            'personal_website_url' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'https://'}),
            'twitter_url' : forms.TextInput(attrs={'class' : 'form-control','placeholder':'https://'}),
            'instagram_url' : forms.TextInput(attrs={'class': 'form-control','placeholder':'https:'}),
            'facebook_url' : forms.TextInput(attrs={'class': 'form-control','placeholder':"https://"}),
            'linkedin_url' : forms.TextInput(attrs={'class': 'form-control','placeholder':"https://"}),
        }

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ('title','Meta_Titles')

        widgets= {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Add Title'}),
            'Meta_Titles' : forms.Textarea(attrs={'class': 'form-control','placeholder':'Add meta titles separated by comma'}),
        }

    def clean_title(self):
        cleaned_data = super(CategoriesForm, self).clean()
        title = cleaned_data['title']
        try:
            Categories.objects.get(title=cleaned_data['title'])
            raise forms.ValidationError('This category already exists')
        except Categories.DoesNotExist:
            pass

        # Always return the full collection of cleaned data.
        return title
    
    def clean_Meta_Titles(self):
        cleaned_data = super(CategoriesForm, self).clean()
        Meta_Titles = cleaned_data['Meta_Titles']
        try:
            Categories.objects.get(Meta_Titles__icontains=cleaned_data['Meta_Titles'])
            raise forms.ValidationError('This category already exists')
        except Categories.DoesNotExist:
            pass

        # Always return the full collection of cleaned data.
        return Meta_Titles

class AddThoughtsView(forms.ModelForm):
    class Meta:
        model = Thoughts
        fields=('thoughts',)

        widgets= {
            'thoughts' : forms.Textarea(attrs={'class': 'form-control','placeholder':'Please use appropriate Language'})
        }
    
class AddComment(forms.ModelForm) :
    class Meta:
        model = Comment
        fields = ('name','body')

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Your Name'}),
            'body' : forms.Textarea(attrs={'class': 'form-control','placeholder':'Please use respectful language while commenting'}),
        }

class SignupForm(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username', 'first_name','last_name','email']
        labels={'first_name': 'First Name','last_name': 'Last Name','email': 'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'}),
        'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.EmailInput(attrs={'class':'form-control'})
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_('Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

