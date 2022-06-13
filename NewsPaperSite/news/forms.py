from allauth.account.forms import SignupForm
from django.forms import ModelForm, TextInput, Textarea, CheckboxSelectMultiple, EmailInput
from django.contrib.auth.models import Group


from .models import Post, Common, Comment, User


class PostForm(ModelForm):
    class Meta:

        model = Post
        fields = ('category', 'heading', 'text')

        widgets ={
            'heading': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок',
                'style': 'width:100%',
                'margin-top': '10px',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст',
                'style': 'width:100%',
                'margin-top': '10px',
            }),
            'category': CheckboxSelectMultiple()
        }


class CommentForm(ModelForm):
     class Meta:

         model = Comment
         fields = ('text',)

         widgets = {
             'text': Textarea(attrs={
                 'class': 'form-control',
                 'placeholder': 'Здесь можно оставить собственный комментарий',
                 'style': 'width:100%',
                 'margin-top': '10px',
             })
         }


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        Common.objects.create(user=user)
        common = Group.objects.get(name='common')
        common.user_set.add(user)
        return user


class UserEditForm(ModelForm):
    class Meta:

        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия',
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Электронная почта',
            })
        }

class CommonEditForm(ModelForm):
    class Meta:

        model = Common
        fields = ('image',)
