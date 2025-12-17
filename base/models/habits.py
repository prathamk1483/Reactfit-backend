# from django.db import models
# from .appUsers import User

# class Habit(models.Model):
#     """
#     Defines the habit itself (e.g., 'Cold Plunge', 'Read 10 pages').
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     frequency = models.CharField(max_length=50, default="Daily")
#     target_time = models.TimeField(null=True, blank=True, help_text="Time for reminder")
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name