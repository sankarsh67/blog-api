from django.db import models
from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,filters,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from .models import Category,Post,Comment,Like
from .serializers import (UserRegisterSerializer,UserSerializer,PostListSerializer,PostDetailSerializer,CategorySerializer,CommentSerializer)
from .permissions import IsAuthorOrReadOnly
from .filters import PostFilter
from .pagination import PostPagination

class RegisterView(APIView):
    permission_classes  = [AllowAny]
    def post(self,request):
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User Registered Sucessfully',
                'user':UserSerializer(user).data
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','description']
    lookup_field = 'slug'

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title','content','author__username']
    ordering_fields = ['created_at','title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer
        
    def get_queryset(self):
 # Published posts for everyone
 # All posts (including drafts) for the author
        user = self.request.user
        if user.is_authenticated:
            return Post.objects.filter(
                models.Q(status='published') | models.Q(author=user)
            )
        return Post.objects.filter(status='published')
    
    def perform_create(self,serializer):
        serializer.save(author =self.request.user)
    
    @action(detail=True,methods=['post'],permission_classes=[IsAuthenticated])
    def like(self,request,pk=None):
        post =self.get_object()
        like,created = Like.objects.get_or_create(post=post,user=request.user)
        if created:
            return Response({'message':'Post liked','likes':post.likes.count()},status=status.HTTP_201_CREATED)
        
        else:
            like.delete()
            return Response({'message':'Post unliked','likes':post.likes.count()},status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)