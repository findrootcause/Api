from django.db import models
from django.utils import timezone

from findcause.settings import *

class FileRecord(models.Model):
    name = models.CharField(max_length=255) #本次事件名称
    upload = models.FileField(upload_to='uploads/') #上传路径
    created_at = models.DateTimeField(default=timezone.now)#创建时间
    
