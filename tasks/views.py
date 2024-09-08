from datetime import timedelta, datetime

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from tasks.models import Task, Comment, TaskTimer
from tasks.serializers import TaskSerializer


class TaskListView(APIView):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all().values('id', 'title')
        return Response(tasks, status=status.HTTP_200_OK)


class MyTasksListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


@api_view(['POST'])
def add_comment_to_task(request):
    task_id = request.data.get('task_id')
    comment_text = request.data.get('comment')

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    comment = Comment.objects.create(task=task, comment=comment_text)

    return Response({'comment_id': comment.id}, status=status.HTTP_201_CREATED)


class StartTaskTimerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        TaskTimer.objects.create(task=task, user=request.user)

        return Response({"message": "Timer started successfully for task {}".format(task.title)},
                        status=status.HTTP_201_CREATED)


@api_view(['POST'])
def stop_task_timer(request, task_id):
    try:
        task_timer = TaskTimer.objects.filter(task_id=task_id, end_time__isnull=True).last()
        if task_timer is None:
            return Response({'error': 'No active timer found for this task.'}, status=status.HTTP_400_BAD_REQUEST)

        task_timer.stop_timer()

        return Response({
            'message': 'Timer stopped successfully',
            'task_id': task_id,
            'duration': task_timer.duration
        }, status=status.HTTP_200_OK)

    except TaskTimer.DoesNotExist:
        return Response({'error': 'Task timer not found.'}, status=status.HTTP_404_NOT_FOUND)


@require_POST
def add_task_timer(request):
    task_id = request.POST.get('task_id')
    date = request.POST.get('date')
    duration_minutes = int(request.POST.get('duration'))

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)

    try:
        start_time = datetime.strptime(date, '%Y-%m-%d')
        end_time = start_time + timedelta(minutes=duration_minutes)
        duration = timedelta(minutes=duration_minutes)

        task_timer = TaskTimer.objects.create(
            task=task,
            start_time=start_time,
            end_time=end_time,
            duration=duration
        )

        return JsonResponse({'status': 'success', 'message': 'Timer added successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)