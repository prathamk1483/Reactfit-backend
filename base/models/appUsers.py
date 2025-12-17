from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission # Add imports

# --- 1. CORE USER MODEL (Identity) ---
class AppUsers(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Super Admin'       # User of the Project
        APP_USER = 'APP_USER', 'App User'

    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    class ActivityLevels(models.TextChoices):
        SEDENTARY = 'sedentary', 'Sedentary'
        LIGHT = 'light', 'Lightly Active'
        MODERATE = 'moderate', 'Moderately Active'
        VERYACTIVE = 'very', 'Very Active'
        EXTREME = 'extreme', 'Extremely Active'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.APP_USER)
    # Biometrics
    firstName = models.CharField(default="",max_length=50)
    lastName = models.CharField(default="",max_length=50)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.MALE)
    country = models.CharField(default="India",max_length=50)
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    weight = models.FloatField(help_text="Current weight in kg", null=True, blank=True)
    activityLevel = models.CharField(max_length=20, choices=ActivityLevels.choices, default=ActivityLevels.MODERATE)

    # AI Context
    primaryGoal = models.TextField(help_text="User's main objective (e.g., 'Hypertrophy', 'Marathon')")
    protocol = models.CharField(default="Generate",max_length=50)
    # injuryistory = models.TextField(blank=True, help_text="Context for AI to avoid dangerous exercises")

    def __str__(self):
        return self.username

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    def save(self, *args, **kwargs):
        # AUTOMATION: If role is ADMIN, give them Django Admin access automatically
        if self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        else:
            # Ensure App Users never get admin access
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)
    groups = models.ManyToManyField(
        Group,
        related_name='appuser_set',  # Unique name to avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='appuser_set',  # Unique name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# --- 2. RPG STATS (The "Gamification" Layer) ---
# class UserRPGStats(models.Model):
#     """
#     Tracks the 'RPG' attributes of the user. 
#     These are calculated by the AI based on workout logs.
#     Range: 0-100 (Leveling system).
#     """
#     user = models.OneToOneField(AppUsers, on_delete=models.CASCADE, related_name="rpg_stats")
    
#     # Core Attributes
#     strength_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     endurance_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     flexibility_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     recovery_score = models.IntegerField(default=0, help_text="Based on sleep/rest consistency", validators=[MinValueValidator(0), MaxValueValidator(100)])
    
#     # Consistency Logic
#     consistency_streak = models.IntegerField(default=0, help_text="Current daily streak")
#     total_workouts = models.IntegerField(default=0)
    
#     last_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username} Stats (Str: {self.strength_score})"


# # --- 3. BODY PART ANATOMY (The "Heatmap" Data) ---
# class BodyPartMetrics(models.Model):
#     """
#     Granular strength tracking for specific muscle groups.
#     Used to generate the 'Body Heatmap' in the UI.
#     """
#     user = models.OneToOneField(AppUsers, on_delete=models.CASCADE, related_name="body_metrics")
    
#     # Upper Body
#     chest_level = models.FloatField(default=0.0, help_text="Calculated from Bench/Pushups")
#     back_level = models.FloatField(default=0.0, help_text="Calculated from Pullups/Rows")
#     arms_level = models.FloatField(default=0.0)
#     shoulders_level = models.FloatField(default=0.0)
    
#     # Lower Body
#     quads_level = models.FloatField(default=0.0, help_text="Calculated from Squats")
#     hamstrings_level = models.FloatField(default=0.0, help_text="Calculated from Deadlifts")
#     calves_level = models.FloatField(default=0.0)
#     glutes_level = models.FloatField(default=0.0)
    
#     # Core
#     core_strength = models.FloatField(default=0.0)

#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username} Body Metrics"


# # --- 4. ACHIEVEMENTS (Badges) ---
# class Achievement(models.Model):
#     """
#     Stores all possible achievements in the system.
#     """
#     class Category(models.TextChoices):
#         STRENGTH = 'strength', 'Strength'
#         CONSISTENCY = 'consistency', 'Consistency'
#         ENDURANCE = 'endurance', 'Endurance'
    
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     category = models.CharField(max_length=20, choices=Category.choices)
#     icon_url = models.URLField(blank=True, null=True) # Link to S3 or static image
#     condition_logic = models.JSONField(help_text="JSON rule for AI to check if unlocked") 
    
#     def __str__(self):
#         return self.name

# class UserAchievement(models.Model):
#     """
#     Link table: Which user unlocked which achievement and when.
#     """
#     user = models.ForeignKey(AppUsers, on_delete=models.CASCADE, related_name="achievements")
#     achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
#     unlocked_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ('user', 'achievement') # Prevent duplicate badges

#     def __str__(self):
#         return f"{self.user.username} - {self.achievement.name}"