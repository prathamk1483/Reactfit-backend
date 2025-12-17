# from django.db import models
# from .appUsers import User

# class WorkoutSession(models.Model):
#     """
#     Represents a single gym session.
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
#     start_time = models.DateTimeField(auto_now_add=True)
#     end_time = models.DateTimeField(null=True, blank=True)
#     name = models.CharField(max_length=255, default="Custom Workout")
    
#     # AI Feedback Loop
#     ai_generated_plan = models.BooleanField(default=False, help_text="Was this suggested by ReactFit AI?")
#     difficulty_rating = models.IntegerField(null=True, blank=True, help_text="RPE (1-10) for the whole session")
#     notes = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.name} - {self.start_time.date()}"
