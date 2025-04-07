from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class RegisterView(APIView):

    def post(self,request):

        try:
            data= request.data
            serializer= RegisterSerializer(data= data)
            if not serializer.is_valid():
                return Response({'data': serializer.errors,'message': 'Somthing went worng'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({'data': {},'message':"your Account is created"}, status=status.HTTP_201_CREATED)


        except Exception as e:
            return Response({'data':{},'message': 'Somthing went worng'}, status=status.HTTP_400_BAD_REQUEST)
        


class LoginView(APIView):

    def post(self, request):

        try:
            
            data= request.data
            serializer= LoginSerializer(data= data)

            if not serializer.is_valid():
                 return Response({'data': serializer.errors,'message': 'Somthing went worng'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            user = serializer.validated_data
            response= serializer.get_jwt_token(user)
            return Response(response, status= status.HTTP_200_OK)
            

        except Exception as e:

              return Response({'data':{},'message': 'Somthing went worng'}, status=status.HTTP_400_BAD_REQUEST)





