from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from analysis.Datacleaning import *
from analysis.Sysanalysis import *
from analysis.Findrootnode import *
from analysis.Findrootcause import *

#数据清理
class DataCleanView(APIView):

    def get(self, request):
        path = os.path.join(os.getcwd(), ".")+'/upload/now/'
        datacleandata, dataclean_json,csv_name = datacleaning(os.path.abspath(path))
        node_json = {"datacleandata":datacleandata,
                     "dataclean_json":dataclean_json,
                     "csv_name":csv_name
                     }
        shutil.rmtree(path)
        os.mkdir(path)
        return Response(node_json)

#系统关系分析
class SysanalysisView(APIView):

    def post(self, request):
        #datacleandata, dataclean_json = datacleaning('E:/软件杯2020/data_release/test/')
        datacleandata = request.data.get("datacleandata")
        dataclean_json = request.data.get("dataclean_json")
        sysanalysis_json = sysanalysis(datacleandata, dataclean_json)
        return Response(sysanalysis_json)

#找到根因结点
class FindrootnodeView(APIView):

    def post(self, request):
        #sysanalysis_json = sysanalysis(datacleandata, dataclean_json)
        dataclean_json = request.data.get("dataclean_json")
        sysanalysis_json = request.data.get("sysanalysis_json")
        findrootnode_json = findrootnode(dataclean_json, sysanalysis_json)
        return Response(findrootnode_json)

#找到根因
class FindrootcauseView(APIView):

    def post(self, request):
        datacleandata = request.data.get("datacleandata")
        findrootnode_json = request.data.get("findrootnode_json")
        findcause_json = findcause(datacleandata, findrootnode_json)
        return Response(findcause_json)

#批量分析
class MoreanalysisView(APIView):

    def get(self, request):
        path = os.path.join(os.getcwd(), ".")+'/upload/now/'
        datacleandata, dataclean_json,csv_name = datacleaning(os.path.abspath(path))
        sysanalysis_json = sysanalysis(datacleandata, dataclean_json)
        findrootnode_json = findrootnode(dataclean_json, sysanalysis_json)
        findcause_json = findcause(datacleandata, findrootnode_json)
        shutil.rmtree(path)
        os.mkdir(path)
        json = {"findrootnode_json":findrootnode_json,
                "findcause_json":findcause_json,
                "csv_name":csv_name
                }
        return Response(json)

