# from django.db import models
# from .habits import Habit
# from django.utils import timezone
# from django.core.validators import MinValueValidator, MaxValueValidator


# class HabitLog(models.Model):
#     """
#     Daily tracking of habits.
#     """
#     habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
#     date = models.DateField(default=timezone.now)
#     status = models.BooleanField(default=False)
#     mood_rating = models.IntegerField(
#         validators=[MinValueValidator(1), MaxValueValidator(10)],
#         null=True, blank=True,
#         help_text="User's subjective feeling, useful for AI context"
#     )

#     class Meta:
#         unique_together = ('habit', 'date')