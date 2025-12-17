from rest_framework import serializers
from .models import AppUsers

class RegisterSerializer(serializers.ModelSerializer):
    # 1. Security: Password must be write-only (never returned in API response)
    password = serializers.CharField(write_only=True)
    
    # 2. Validation: Ensure email is actually provided
    email = serializers.EmailField(required=True)

    class Meta:
        model = AppUsers
        fields = [
            # --- Standard Auth Fields (REQUIRED) ---
            'username', 'email', 'password',
            
            # --- Your Custom Profile Fields ---
            'firstName', 'lastName', 'role',
            'height', 'weight', 'age',
            'gender', 'country', 'activityLevel',
            'primaryGoal', 'protocol'
        ]

    def create(self, validated_data):
        # 3. Security: Extract password so we can hash it
        password = validated_data.pop('password')
        
        # 4. Use create_user() to handle password hashing and field assignment
        user = AppUsers.objects.create_user(
            password=password,
            **validated_data
        )
        return user