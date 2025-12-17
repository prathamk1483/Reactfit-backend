# from django.db import models
# from .appUsers import User
# from django.utils import timezone


# class DailySummary(models.Model):
#     """
    # Pre-computed summary for the 'Dashboard' and 'AI Context'.
#     Instead of querying 5 tables, the AI reads this one row to know the user's status.
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_summaries')
#     date = models.DateField(default=timezone.now)
    
#     # Aggregated Metrics
#     total_sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
#     total_water_ml = models.PositiveIntegerField(default=0)
#     total_steps = models.PositiveIntegerField(default=0)
#     habits_completed_count = models.PositiveIntegerField(default=0)
#     workout_performed = models.BooleanField(default=False)
#     description = models.TextField(max_length=1000,default="")
    
#     # AI Readiness Score
#     readiness_score = models.IntegerField(
#         default=0,
#         help_text="0-100 score calculated by AI based on sleep/stress/activity"
#     )

#     class Meta:
#         unique_together = ('user', 'date')