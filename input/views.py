from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

import os
from  input.serializers import *

def handle_uploaded_file(f):
    with open(os.path.abspath(os.path.join(os.getcwd(), "."))+'/upload/now/'+f.name, 'wb+') as fp:
        for chunk in f.chunks():
            fp.write(chunk)

class FileRecordsView(APIView):
    
    def get(self,request):
        filerecord = FileRecord.objects.all()
        serializer = FileRecordSerializer(filerecord, many=True)
        return Response(serializer.data)

    def post(self,request):
        csv_file = request.FILES.get('csv')
        handle_uploaded_file(csv_file)
        if (csv_file) is None:
            return Response({'detail': '文件为空'}, status=status.HTTP_400_BAD_REQUEST)
        name = csv_file.name.split('.')[0]
        ext = csv_file.name.split('.')[-1].lower()
        if ext != "csv":
            return Response({'detail': '只能上传csv格式的文件'}, status=status.HTTP_400_BAD_REQUEST)
        csv = FileRecord.objects.create(name=csv_file.name, upload=csv_file)
        return Response()
