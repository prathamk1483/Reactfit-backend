# from django.db import models


# class ExerciseLibrary(models.Model):
#     """
#     Static database of exercises for the AI to choose from.
#     """
#     name = models.CharField(max_length=255, unique=True)
#     muscle_group = models.CharField(max_length=100)
#     equipment_required = models.CharField(max_length=100, blank=True)
#     # AI instruction field
#     form_cues = models.TextField(help_text="Text for AI to speak during vision correction")

#     def __str__(self):
#         return self.name