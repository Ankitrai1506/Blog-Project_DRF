from rest_framework.views import APIView
from .serializer import BlogSerializer, CommentSerializer, LikeSerializer
from .models import Blog, Comment, Like
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

class PublicView(APIView):

    def get(self, request):
        blog= Blog.objects.all().order_by('-created_at')
        if request.GET.get('search'):
            search= request.GET.get('search')
            blogs= blog.filter(Q(title__icontains= search)| Q(blog_text__icontains= search))


        serializer= BlogSerializer(blog, many= True)

        for blog in serializer.data:
            blog_obj= Blog.objects.get(uid= blog['uid'])
            blog['comments']= CommentSerializer(blog_obj.comments.all(), many= True).data
            blog['likes']= LikeSerializer(blog_obj.likes.all(), many= True).data
            blog['like_count']= blog_obj.like_count
        return Response({'data': serializer.data, 'message': 'You have got all the blog'}, status= status.HTTP_200_OK)
    
    

class BlogView(APIView):
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]

    def post(self, request):
        data= request.data
        data['user']= request.user
        serializer= BlogSerializer(data= data)
        if serializer.is_valid():
            serializer.save(user= request.user)
            return Response({'data': serializer.data, 'message': 'blog is created'}, status= status.HTTP_201_CREATED)
        
        return Response({'data': serializer.errors, 'message': 'Invalid data'}, status= status.HTTP_400_BAD_REQUEST)
            

    def get(self, request):
        blog= Blog.objects.filter(user_id= request.user)
        serializer= BlogSerializer(blog, many= True)
        for blog in serializer.data:
            blog_obj= Blog.objects.get(uid= blog['uid'])
            blog['comments']= CommentSerializer(blog_obj.comments.all(), many= True).data
            blog['likes']= LikeSerializer(blog_obj.likes.all(), many= True).data
        return Response({'data':serializer.data}, status= status.HTTP_200_OK)
    

    def patch(self,request):

        data= request.data
        blog_uid= data.get('blog_id')



        if not blog_uid:
            return  Response({"message": 'blog_id is required'}, status= status.HTTP_400_BAD_REQUEST)
        

        blog= Blog.objects.get(uid= blog_uid)

        if request.user != blog.user:
            return Response({
                'data':{},
                'message': 'You are not authorized'}, status= status.HTTP_400_BAD_REQUEST)
        
        if not blog:
            return Response({
                'data':{},
                'message': 'blog_id not found'}, status= status.HTTP_400_BAD_REQUEST)
        
        serializer= BlogSerializer(blog, data= data, partial= True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data, 
                'message': 'Your blog is updated'}, status= status.HTTP_200_OK)
        
        return Response({
            'data':{},
            'message': 'Something worng'}, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        
        data= request.data 
        blog_uid= data.get('blog_id')

        if not blog_uid:
            return  Response({"message": 'blog_id is required'}, status= status.HTTP_400_BAD_REQUEST)


        blog= Blog.objects.get(uid= blog_uid)

        if request.user != blog.user:
            return Response({
                'data':{},
                'message':'you are not authorized' }, status= status.HTTP_400_BAD_REQUEST)
        
        if not blog:
            return Response({
                'data': {},
                'message': 'blog_id not found' }, status= status.HTTP_400_BAD_REQUEST)
        
        blog.delete()
        return Response({'message': 'blog deleted'}, status= status.HTTP_200_OK)
    

class CommentView(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes= [IsAuthenticated]

    def get(self, request):
        blog_uid= request.data.get('blog_id')

    

        if not blog_uid:
            return Response({'message': 'blog_ID is required'}, status= status.HTTP_400_BAD_REQUEST)
        
        blog= Blog.objects.get(uid= blog_uid, user= request.user)
        if not blog:
            return Response({'message': "Its not your blog, You cant see Comment "}, status= status.HTTP_404_NOT_FOUND)
        
        comments= blog.comments.all()
        serializer= CommentSerializer(comments, many= True)
        return Response({'data': serializer.data, 'message': "comment retrive"}, status= status.HTTP_200_OK)
    
    def post(self, request):
        blog_uid= request.data.get('blog_id')
        comment_text= request.data.get("comment")

        if not blog_uid:
            return Response({'message': "blog_id is required"}, status= status.HTTP_404_NOT_FOUND)

        blog= Blog.objects.get(uid= blog_uid)
        if not blog:
            return Response({'message': "blog not found"}, status= status.HTTP_404_NOT_FOUND)
        
        comments= Comment.objects.create(user= request.user, blog= blog, comment= comment_text)
        serializer= CommentSerializer(comments)
        return Response({'data': serializer.data, 'message': "comment added "}, status= status.HTTP_201_CREATED)
    

    def patch(self, request):
        comment_uid= request.data.get("comment_uid")
        new_text= request.data.get("comment")

        if not comment_uid:
            return Response({'message': "comment uid required"}, status= status.HTTP_404_NOT_FOUND)

        comment= Comment.objects.get(uid= comment_uid, user= request.user)
        if not comment:
            return Response({'message': "You are Not Authorized to update the comment"}, status= status.HTTP_404_NOT_FOUND)
        
        comment.comment= new_text
        comment.save()
        serializer= CommentSerializer(comment)
        return Response({'data': serializer.data, 'message': "comment Updated"}, status= status.HTTP_200_OK)

    def delete(self, request):
        comment_uid= request.data.get("comment_uid")

        comment= Comment.objects.get(uid= comment_uid, user= request.user)

        if not comment:
            return Response({"message": 'You are Not authorized to delete'}, status= status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({"message": 'Comment deleted'}, status= status.HTTP_200_OK)
    

class LikeView(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes= [IsAuthenticated]

    def post(self, request):
        blog_uid= request.data.get("blog_id")

        if not blog_uid:
            return Response({'message': 'Blog uid required'}, status= status.HTTP_400_BAD_REQUEST)
        
        blog= Blog.objects.get(uid= blog_uid)

        if not blog:
            return Response({'message': "blog not found"}, status= status.HTTP_404_NOT_FOUND)
        
        like, created = Like.objects.get_or_create(user=request.user, blog=blog)

        if created:
            blog.like_count += 1
            blog.save()
            return Response({'message': "Blog liked"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': "You have already liked this blog"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        blog_uid = request.data.get("blog_id")

        if not blog_uid:
            return Response({'message': 'Blog UID is required'}, status=status.HTTP_400_BAD_REQUEST)

        blog = Blog.objects.get(uid=blog_uid)
        if not blog:
            return Response({'message': "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        like = Like.objects.get(user=request.user, blog=blog)
        if like:
            # blog.like_count -= 1
            # blog.save()
            like.delete()
            return Response({'message': "Like removed"}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "You haven't liked this blog"}, status=status.HTTP_400_BAD_REQUEST)
