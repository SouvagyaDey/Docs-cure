from rest_framework import serializers
from .models import CustomUser, Profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(required=False, write_only=True)
    phone = serializers.CharField(required=False, write_only=True)
    role = serializers.ChoiceField(choices=['patient', 'doctor'], required=False, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone', 'role']

    def create(self, validated_data):
        # Extract profile fields
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        phone = validated_data.pop('phone', '')
        role = validated_data.pop('role', 'patient')

        user = CustomUser(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        # create a related profile for the new user with extra fields
        Profile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
        )
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']



class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'role',
            'profile_picture',
            'first_name',
            'last_name',
            'bio',
            'phone',
            'address',
            'date_of_birth',
            'created_at',
            'updated_at',
            'get_full_name'
        ]