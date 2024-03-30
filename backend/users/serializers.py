from rest_framework.serializers import ModelSerializer
from .models import UserComplaint


class UserComplaintSerializer(ModelSerializer):
    class Meta:
        model = UserComplaint
        fields = ('text',)