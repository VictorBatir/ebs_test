from django.contrib import admin
from .models import Task, Comment, TaskTimer

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'status')
    list_filter = ('status', 'user')
    search_fields = ('title', 'user__username', 'description')
    ordering = ('-status', 'title')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at', 'content')
    search_fields = ('task__title', 'user__username', 'content')
    ordering = ('-created_at',)

class TaskTimerAdmin(admin.ModelAdmin):
    list_display = ('task', 'start_time', 'end_time', 'duration')
    list_filter = ('task', 'start_time', 'end_time')
    search_fields = ('task__title',)
    ordering = ('-start_time',)

admin.site.register(TaskTimer, TaskTimerAdmin)
