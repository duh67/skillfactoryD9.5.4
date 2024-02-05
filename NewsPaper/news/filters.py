from django import forms
from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
from .models import Post, Author


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        lookup_expr='exact',
        label='Автор',
        empty_label='Все авторы',
    )
    datetime_post = DateFilter(
        field_name='datetime_post',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form'}),
        lookup_expr='date__gte',
        label='Опубликованы после'
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'datetime_post'
        ]