from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'author']
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'category': 'Категория',
            'author': 'Автор'
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if content == title:
            raise ValidationError(
                'Текст не должен совпадать с заголовком.'
            )

        return cleaned_data


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user