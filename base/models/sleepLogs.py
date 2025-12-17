# from django.db import models
# from .appUsers import User
# from django.utils import timezone
# from django.core.validators import MinValueValidator, MaxValueValidator


# class SleepLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sleep_logs')
#     date = models.DateField(default=timezone.now)
#     total_hours = models.DecimalField(max_digits=4, decimal_places=2)
#     deep_sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
#     rem_sleep_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
#     recovery_score = models.IntegerField(
#         validators=[MinValueValidator(0), MaxValueValidator(100)],
#         help_text="AI-calculated score based on quality"
#     )

#     class Meta:
#         unique_together = ('user', 'date')