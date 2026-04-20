from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView,CategoryViewSet,CommentViewSet,PostViewSet
router = DefaultRouter()
router.register('categories',CategoryViewSet,basename='category')
router.register('posts', PostViewSet,basename='post')

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',obtain_auth_token,name='login'),
    
    path('',include(router.urls)),
    
    path('posts/<int:post_pk>/comments/', CommentViewSet.as_view({'get':'list','post':'create'}),name='post-comments'),
    path('posts/<int:post_pk>/comments/<int:pk>/',CommentViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'}),name='post-comment-detail'),
]