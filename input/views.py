from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from  input.serializers import *


class FileRecordsView(APIView):
    
    def get(self,request):
        filerecord = FileRecord.objects.all()
        serializer = FileRecordSerializer(filerecord, many=True)
        return Response(serializer.data)
