# serializers.py
from rest_framework import serializers
from .models import Status,Task,Priority,Team,User,CustomUser,Chat

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()    
    password = serializers.CharField()


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Status
        fields=['task_status']

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model=Priority
        fields=['priority_status']
    
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['content','timestamp','team']

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field = 'name', queryset = CustomUser.objects.all())
    status = serializers.SlugRelatedField(slug_field = 'task_status', queryset = Status.objects.all())
    priority = serializers.SlugRelatedField(slug_field = 'priority_status', queryset = Priority.objects.all())
    class Meta:
        model=Task
        fields=['id','team','task','owner','status','priority','notes','files']

class CustomUserSerializer:
    class Meta:
        model = CustomUser
        fields='__all__'

class CustomStringRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        # Convert the related object to its string representation
        return str(value)

    def to_internal_value(self, data):
        # This method converts the string representation back to the related object
        try:
            # Perform a lookup to retrieve the CustomUser object based on the string representation
            user = CustomUser.objects.get(name=data) # Assuming 'username' is unique
            return user
        except CustomUser.DoesNotExist:
            # Handle the case where the CustomUser object does not exist
            raise serializers.ValidationError(f"CustomUser with username '{data}' does not exist")
        
class TeamSerializer(serializers.ModelSerializer):
    members = CustomStringRelatedField(many=True,queryset = CustomUser.objects.all())
    class Meta:
        model = Team
        fields = ['members']

# class OwnerSerializer(serializers.ModelSerializer):
#     team = TeamSerializer()
#     user = CustomUserSerializer()
#     class Meta:
#         model=Owner
#         fields=['user','team']