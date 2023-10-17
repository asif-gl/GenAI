from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from .serializers import UserSerializers
from rest_framework.decorators import api_view
from .tests import qa_bot

# Create your views here.

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def final_result(request):
    if request.method == 'POST':
        data = request.data
        query = data.get('query', None)
        qa_result = qa_bot()
        response = qa_result({'query': query})
        return Response(response['result'])
    

@api_view(['POST'])
def pdf_loader(request):
    if request.method == 'POST':
        data = request.data
        query = data.get('query', None)
        qa_result = qa_bot()
        response = qa_result({'query': query})
        return Response(response)
