# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 0005 10:14
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: common.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
from django.db import models

class BaseModel(models.Model):
	"""为模型类补充字段"""
	add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

	class Meta:
		abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
