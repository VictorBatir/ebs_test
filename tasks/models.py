from datetime import timezone

from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilizatorul care a creat sarcina

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_task_user = None
        if not is_new:
            old_task_user = Task.objects.get(pk=self.pk).user

        super().save(*args, **kwargs)

        if is_new or (old_task_user != self.user):
            self.send_email_notification()

    def send_email_notification(self):
        subject = 'Noua sarcină asignată: {}'.format(self.title)
        message = 'Salut {},\n\nAi fost asignat la o nouă sarcină: {}\nDescriere: {}\nStatus: {}'.format(
            self.user.first_name, self.title, self.description, self.status
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],  # Emailul utilizatorului asignat
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  # Comment content
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.task}'

class TaskTimer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f'Task {self.task.title} - Timer'

    def stop_timer(self):
        self.end_time = timezone.now()
        self.duration = self.end_time - self.start_time
        self.save()
