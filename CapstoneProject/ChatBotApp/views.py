from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from .serializers import UserSerializers, UserProfileSerializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from .rag import qa_bot, set_custom_prompt
from langchain import PromptTemplate

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        if user is not None:
            if user.is_active:
                login(request, user)

                return Response({'access_token': access_token}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Successfully SignUp.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):    
    user = request.user

    if request.method == 'GET':
        serializer = UserSerializers(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    # Perform any additional logout logic if needed
    logout(request)  # Remove the authentication token
    return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_bot(request):
    if request.method == 'POST':
        data = request.data
        query = data.get('query', None)
        qa_prompt = set_custom_prompt()
        qa_result = qa_bot(qa_prompt)
        response = qa_result({'query': query})
        return Response(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_learning_path(request):
    if request.method == 'POST':
        data = request.data

        # Define your prompt templates
        learning_template = """Design a personalized learning path on {question} for software development. explain the concepts to start learning and explain the step-by-step process to achieve the goal. Give some references..
        Context: {context}

        Only return the helpful answer below and nothing else.
        Helpful answer:

        """
        LEARNING_PROMPT = PromptTemplate(template=learning_template, input_variables=['context', 'question'])

        query = data.get('query', None)
        qa_prompt = LEARNING_PROMPT
        qa_result = qa_bot(qa_prompt)
        response = qa_result({'query': query})
        return Response(response)

    