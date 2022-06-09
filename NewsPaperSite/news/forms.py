from django.forms import ModelForm, TextInput, Textarea
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


from .models import Post, Common, Comment


class PostForm(ModelForm):

    class Meta:

        model = Post
        fields = ('category', 'heading', 'text')

        widgets ={
            'heading': TextInput(attrs={
                'class': 'from-control',
                'placeholder': 'Заголовок',
            }),
            'text': Textarea(attrs={
                'class': 'from-control',
                'placeholder': 'Текст',
            }),
        }


class CommentForm(ModelForm):

     class Meta:

         model = Comment
         fields = ('text',)

         widgets = {
             'text': Textarea(attrs={
                 'class': 'form-control',
                 'placeholder': 'Здесь можно оставить собственный комментарий',
                 'id': 'id_text_comment'

             })
         }


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        Common.objects.create(user=user)
        common = Group.objects.get(name='common')
        common.user_set.add(user)
        return user
