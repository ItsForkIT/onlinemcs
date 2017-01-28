from rest_framework import serializers

from mcs.models import *


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Health
        fields = ('Type', 'Quantity', 'File')