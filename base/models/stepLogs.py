# from django.db import models
# from .appUsers import User
# from django.utils import timezone

# class StepLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='step_logs')
#     date = models.DateField(default=timezone.now)
#     steps_count = models.PositiveIntegerField(default=0)
#     calories_burned = models.PositiveIntegerField(default=0)
#     distanceKm = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
#     timeTaken = models.IntegerField(default=0)
#     class Meta:
#         unique_together = ('user', 'date')