import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name',lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__username',lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices = Post.STATUS_CHOICES)
    from_date = django_filters.DateFilter(field_name= 'created_at',lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at',lookup_expr='lte')
    
    class Meta:
        model = Post
        fields = ['title','category','author','status','from_date','to_date']