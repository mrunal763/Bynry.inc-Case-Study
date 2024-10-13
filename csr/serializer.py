from rest_framework.serializers import ModelSerializer
from .models import GasUtilServiceRequest


# Service request serializer
class GasUtilServiceRequestSerializer(ModelSerializer):
    class Meta:
        model = GasUtilServiceRequest
        fields = '__all__'