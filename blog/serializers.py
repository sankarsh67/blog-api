from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category,Post,Like,Comment

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length = 6)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id','username','email','password','password2']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password dont match')
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields  = ['id','username','email']
        
class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id','name','slug','description', 'post_count']
        read_only_fields = ['slug']
    
    def get_post_count(self,obj):
        return obj.posts.count()
    
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source = 'author.username')
    class Meta :
        model = Comment
        fields  = ['id','author_name','content','created_at']
        read_only_fields = ['author_name','created_at']       
        
        
class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source = 'author.username')
    category_name = serializers.ReadOnlyField(source = 'category.name')
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','title','slug','author_name','category_name','excerpt','status','comment_count','like_count','created_at']
        
    def get_comment_count(self,obj):
        return obj.comments.count()
    def get_like_count(self,obj):
        return obj.likes.count()
    
class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source = 'author.username')
    category_name = serializers.ReadOnlyField(source = 'category.name')
    comments = CommentSerializer(many=True,read_only =True)
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields  = ['id','title','slug','author_name','category','category_name','content','excerpt','status','comments','comment_count','like_count','is_liked','created_at','updated_at']
        read_only_fields = ['slug','author_name']
        
    def get_comment_count(self,obj):
        return obj.comments.count()
    def get_like_count(self,obj):
        return obj.likes.count()
    def get_is_liked(self,obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated :
            return obj.likes.filter(user=request.user).exists()
        return False