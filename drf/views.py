from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from .serializers import BlogSerializer, CommentSerializer
from .pagination import CustomPagination
from blogapp.models import Blog, Comment



# Create your views here.

class BlogModelViewSet(ModelViewSet):
    serializer_class = BlogSerializer 
    # queryset = Blog.objects.all()
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'body']
    
    
    def get_queryset(self):
        queryset = Blog.objects.all()
        category = self.request.query_params.get("category") 
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset
        
    
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_serializer_context(self):
        if self.request.user:
            user = self.request.user 
            return {"user": user}
    
   
    def update(self, request, *args, **kwargs):
        blog = self.get_object() 
        if request.user != blog.user:
            return Response({"error": "You are not permitted to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
 
    def destroy(self, request, *args, **kwargs):
        blog = self.get_object()
        if request.user != blog.user:
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)





class CommentModelViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        blog_id = self.kwargs.get("blog_pk")
        comments = Comment.objects.filter(blog_id=blog_id)
        return comments
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_serializer_context(self):
        blog_id = self.kwargs.get("blog_pk")
        blog = Blog.objects.get(id=blog_id)
        user = self.request.user
        return{"blog": blog, "user": user}

    
    def update(self, request, *args, **kwargs):
        comment = self.get_object() 
        if request.user != comment.user:
            return Response({"error": "You are not permitted to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
 
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user != comment.user:
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
