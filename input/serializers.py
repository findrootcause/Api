from rest_framework import serializers
from .models import *

from findcause.settings import *
class FileRecordSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FileRecord
        fields = ['name', 'upload', 'created_at']
