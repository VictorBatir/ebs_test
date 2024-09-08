from rest_framework_simplejwt.tokens import RefreshToken

from tasks.serializers import TaskSerializer
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from tasks.models import Task

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': RegisterSerializer(user).data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response ({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListView(APIView):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all().values('id', 'title')  # Selectăm doar id și title
        return Response(tasks, status=status.HTTP_200_OK)


class TaskDetailView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
            task_details = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'owner': task.user.username
            }
            return Response(task_details, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)