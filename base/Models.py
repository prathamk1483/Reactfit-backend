"""
ReactFit - Django Models
Precision Wellness Ecosystem Backend
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

# ═══════════════════════════════════════════════════════════════
# CORE USER MODEL
# ═══════════════════════════════════════════════════════════════

class User(AbstractUser):
    """Extended User model with ReactFit-specific fields"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly Active'),
        ('moderate', 'Moderately Active'),
        ('very', 'Very Active'),
        ('extreme', 'Extremely Active'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic Info
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Biometrics
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    current_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    target_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Activity Profile
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, default='moderate')
    
    # Goals & Preferences
    daily_step_goal = models.IntegerField(default=10000)
    daily_water_goal_ml = models.IntegerField(default=2000)
    target_sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, default=8.0)
    
    # AI Preferences
    ai_coaching_enabled = models.BooleanField(default=True)
    preferred_workout_time = models.TimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    onboarding_completed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
    
    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    @property
    def bmi(self):
        if self.current_weight_kg and self.height_cm:
            height_m = float(self.height_cm) / 100
            return float(self.current_weight_kg) / (height_m ** 2)
        return None


# ═══════════════════════════════════════════════════════════════
# WORKOUT SYSTEM
# ═══════════════════════════════════════════════════════════════

class Exercise(models.Model):
    """Exercise library - templates for all exercises"""
    
    CATEGORY_CHOICES = [
        ('strength', 'Strength Training'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility'),
        ('balance', 'Balance'),
        ('sports', 'Sports'),
    ]
    
    MUSCLE_GROUP_CHOICES = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('shoulders', 'Shoulders'),
        ('arms', 'Arms'),
        ('core', 'Core'),
        ('legs', 'Legs'),
        ('full_body', 'Full Body'),
        ('cardio', 'Cardio'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_GROUP_CHOICES)
    
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    
    # Metadata
    difficulty_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3
    )
    equipment_required = models.CharField(max_length=200, blank=True)
    is_compound = models.BooleanField(default=False)
    
    # Computer Vision Support
    supports_form_tracking = models.BooleanField(default=False)
    supports_rep_counting = models.BooleanField(default=False)
    
    # System
    is_custom = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_exercises')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'exercises'
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'muscle_group']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Workout(models.Model):
    """Individual workout session"""
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    
    title = models.CharField(max_length=200, blank=True)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    ai_generated = models.BooleanField(default=False)
    ai_prompt = models.TextField(blank=True)  # Store the prompt if AI-generated
    
    # Analytics
    total_volume_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estimated_calories_burned = models.IntegerField(null=True, blank=True)
    
    # Ratings (1-5 scale)
    difficulty_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    energy_level_before = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    energy_level_after = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'workouts'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title or 'Workout'} ({self.date})"
    
    def calculate_duration(self):
        """Calculate workout duration from start/end times"""
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            self.duration_minutes = int(delta.total_seconds() / 60)
            return self.duration_minutes
        return None


class WorkoutExercise(models.Model):
    """Exercises within a workout session"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    
    order = models.IntegerField(default=0)  # Order in the workout
    
    # Planned vs Actual
    target_sets = models.IntegerField(default=3)
    target_reps = models.IntegerField(null=True, blank=True)
    target_duration_seconds = models.IntegerField(null=True, blank=True)  # For timed exercises
    target_weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    completed_sets = models.IntegerField(default=0)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'workout_exercises'
        ordering = ['order']
        unique_together = ['workout', 'order']
    
    def __str__(self):
        return f"{self.workout.title} - {self.exercise.name}"


class ExerciseSet(models.Model):
    """Individual sets within a workout exercise"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name='sets')
    
    set_number = models.IntegerField()
    reps = models.IntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    distance_meters = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Computer Vision Data
    form_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # 0-100
    cv_rep_count = models.IntegerField(null=True, blank=True)
    cv_analyzed = models.BooleanField(default=False)
    
    # Metadata
    rest_seconds = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'exercise_sets'
        ordering = ['set_number']
        unique_together = ['workout_exercise', 'set_number']
    
    def __str__(self):
        return f"Set {self.set_number}: {self.reps} reps @ {self.weight_kg}kg"
    
    @property
    def volume(self):
        """Calculate volume (reps × weight)"""
        if self.reps and self.weight_kg:
            return float(self.reps) * float(self.weight_kg)
        return 0


# ═══════════════════════════════════════════════════════════════
# BIO-TRACKING MODULES
# ═══════════════════════════════════════════════════════════════

class SleepLog(models.Model):
    """Daily sleep tracking"""
    
    QUALITY_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Fair'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sleep_logs')
    
    date = models.DateField()  # Date of waking up
    bedtime = models.DateTimeField()
    wake_time = models.DateTimeField()
    
    # Calculated
    duration_hours = models.DecimalField(max_digits=4, decimal_places=2)
    
    # Quality Metrics
    quality_rating = models.IntegerField(choices=QUALITY_CHOICES, null=True, blank=True)
    interruptions = models.IntegerField(default=0)
    deep_sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    rem_sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sleep_logs'
        ordering = ['-date']
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.duration_hours}h)"
    
    def save(self, *args, **kwargs):
        # Auto-calculate duration
        if self.bedtime and self.wake_time:
            delta = self.wake_time - self.bedtime
            self.duration_hours = round(delta.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)


class WaterIntakeLog(models.Model):
    """Water intake tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='water_logs')
    
    date = models.DateField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    amount_ml = models.IntegerField()
    
    class Meta:
        db_table = 'water_intake_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.amount_ml}ml on {self.date}"


class StepLog(models.Model):
    """Daily step count tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='step_logs')
    
    date = models.DateField(default=timezone.now)
    step_count = models.IntegerField(default=0)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    active_minutes = models.IntegerField(null=True, blank=True)
    calories_burned = models.IntegerField(null=True, blank=True)
    
    # Source tracking
    source = models.CharField(max_length=50, default='manual')  # manual, fitbit, apple_health, etc.
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'step_logs'
        ordering = ['-date']
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.step_count} steps on {self.date}"


class BodyMetric(models.Model):
    """Body measurements tracking over time"""
    
    METRIC_TYPE_CHOICES = [
        ('weight', 'Weight'),
        ('body_fat', 'Body Fat %'),
        ('muscle_mass', 'Muscle Mass'),
        ('chest', 'Chest'),
        ('waist', 'Waist'),
        ('hips', 'Hips'),
        ('thigh', 'Thigh'),
        ('bicep', 'Bicep'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='body_metrics')
    
    date = models.DateField(default=timezone.now)
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPE_CHOICES)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=10)  # kg, cm, %, etc.
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'body_metrics'
        ordering = ['-date', 'metric_type']
        indexes = [
            models.Index(fields=['user', 'metric_type', 'date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_metric_type_display()}: {self.value}{self.unit}"


# ═══════════════════════════════════════════════════════════════
# MINDSET MODULE
# ═══════════════════════════════════════════════════════════════

class Habit(models.Model):
    """User-defined habits to track"""
    
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom Days'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    
    # Custom frequency (for 'custom' type)
    target_days_per_week = models.IntegerField(null=True, blank=True)
    
    # Metadata
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'habits'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"


class HabitLog(models.Model):
    """Daily habit completion tracking"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'habit_logs'
        ordering = ['-date']
        unique_together = ['habit', 'date']
        indexes = [
            models.Index(fields=['habit', 'date']),
        ]
    
    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"{self.habit.name} - {self.date} {status}"


class MoodLog(models.Model):
    """Daily mood & motivation tracking"""
    
    MOOD_CHOICES = [
        (1, 'Very Low'),
        (2, 'Low'),
        (3, 'Neutral'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_logs')
    
    date = models.DateField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    mood_rating = models.IntegerField(choices=MOOD_CHOICES)
    motivation_rating = models.IntegerField(choices=MOOD_CHOICES)
    stress_level = models.IntegerField(choices=MOOD_CHOICES)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'mood_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - Mood: {self.get_mood_rating_display()} ({self.date})"


# ═══════════════════════════════════════════════════════════════
# AI INTERACTION LAYER
# ═══════════════════════════════════════════════════════════════

class AIConversation(models.Model):
    """AI chat conversation threads"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    
    title = models.CharField(max_length=200, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'ai_conversations'
        ordering = ['-last_message_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title or 'Conversation'}"


class AIMessage(models.Model):
    """Individual messages in AI conversations"""
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'AI Assistant'),
        ('system', 'System'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name='messages')
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    
    # Context tracking
    context_data = models.JSONField(null=True, blank=True)  # Store relevant user data snapshot
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.get_role_display()}: {self.content[:50]}..."


class AIAction(models.Model):
    """Actions taken by AI (workout logs, habit updates, etc.)"""
    
    ACTION_TYPE_CHOICES = [
        ('workout_log', 'Logged Workout'),
        ('workout_create', 'Created Workout Plan'),
        ('habit_update', 'Updated Habit'),
        ('goal_set', 'Set Goal'),
        ('recommendation', 'Made Recommendation'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_actions')
    message = models.ForeignKey(AIMessage, on_delete=models.SET_NULL, null=True, blank=True)
    
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES)
    action_data = models.JSONField()  # Store action details
    
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_actions'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_type_display()}"


# ═══════════════════════════════════════════════════════════════
# ANALYTICS & INSIGHTS
# ═══════════════════════════════════════════════════════════════

class ProgressSnapshot(models.Model):
    """Weekly/Monthly progress summaries"""
    
    PERIOD_TYPE_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_snapshots')
    
    period_type = models.CharField(max_length=10, choices=PERIOD_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Aggregated Metrics
    total_workouts = models.IntegerField(default=0)
    total_workout_minutes = models.IntegerField(default=0)
    total_volume_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    avg_sleep_hours = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    avg_daily_steps = models.IntegerField(null=True, blank=True)
    total_water_ml = models.IntegerField(null=True, blank=True)
    
    habit_completion_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # AI-Generated Insights
    ai_summary = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'progress_snapshots'
        ordering = ['-end_date']
        unique_together = ['user', 'period_type', 'start_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_period_type_display()} ({self.start_date} to {self.end_date})"


# ═══════════════════════════════════════════════════════════════
# REMINDERS & NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════

class Reminder(models.Model):
    """User reminders (water, workout, habits, etc.)"""
    
    TYPE_CHOICES = [
        ('water', 'Water Reminder'),
        ('workout', 'Workout Reminder'),
        ('habit', 'Habit Reminder'),
        ('sleep', 'Sleep Reminder'),
        ('custom', 'Custom Reminder'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    
    time = models.TimeField()
    days_of_week = models.JSONField(default=list)  # [0-6] for Mon-Sun
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reminders'
        ordering = ['time']
    
    def __str__(self):
        return f"{self.user.username} - {self.title} @ {self.time}"