from django.db import models
from django.contrib.auth.models import User

class DailySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    palace_theme = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    palace_image = models.ImageField(upload_to='palaces/', blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.date}"

class Task(models.Model):
    session = models.ForeignKey(DailySession, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=32)  # creative/analytical/physical/admin
    complexity = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(null=True, blank=True)  # Order of completion assigned by LLM, only for sub-tasks
    layer_image = models.ImageField(upload_to='layers/', blank=True, null=True)
    layer_revealed_image = models.ImageField(upload_to='layer_images/', blank=True, null=True, help_text='Image showing only this layer revealed')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_tasks')
    palace_image = models.ImageField(upload_to='palaces/', blank=True, null=True)
    complete_palace_image = models.ImageField(upload_to='complete_palaces/', blank=True, null=True)
    time_estimate = models.IntegerField(null=True, blank=True, help_text='Estimated time to complete in minutes')

    def __str__(self):
        base = str(self.title)
        if self.time_estimate is not None:
            base += f" ({self.time_estimate} min)"
        return base 