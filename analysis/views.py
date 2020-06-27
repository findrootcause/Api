from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from analysis.Datacleaning import *

class DataCleanView(APIView):
    
    def get(self,request):
        dataclean_json = datacleaning('E:/软件杯2020/data_release/train/')
        return Response(dataclean_json)
