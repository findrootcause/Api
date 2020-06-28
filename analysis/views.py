from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from analysis.Datacleaning import *
from analysis.Sysanalysis import *
from analysis.Findrootnode import *
from analysis.Findrootcause import *

class DataCleanView(APIView):
    
    def get(self,request):
        datacleandata,dataclean_json = datacleaning('E:/软件杯2020/data_release/test/')
        sysanalysis_json = sysanalysis(datacleandata,dataclean_json)
        findrootnode_json = findrootnode(dataclean_json,sysanalysis_json)
        findcause_json = findcause(datacleandata,findrootnode_json)
        return Response(findcause_json)
