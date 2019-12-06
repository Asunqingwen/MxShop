# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 0005 14:09
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: import_category_data.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
import os
import sys

# 获取当前文件的路径（运行脚本）
pwd = os.path.dirname(os.path.realpath(__file__))
# 获取项目根目录
sys.path.append(pwd + "../")
# 要想单独使用django的model，必须指定一个环境变量，会去settings配置找
# 参照manage.py里面就知道为什么这样设置了
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")

import django

django.setup()

from goods.models import GoodsCategory
from db_tools.data.category_data import row_data

# 一级类
for lev1_cat in row_data:
	lev1_instance = GoodsCategory()
	lev1_instance.code = lev1_cat['code']
	lev1_instance.name = lev1_cat['name']
	lev1_instance.category_type = 1
	# 保存到数据库
	lev1_instance.save()

	# 二级类
	for lev2_cat in lev1_cat['sub_categorys']:
		lev2_instance = GoodsCategory()
		lev2_instance.code = lev2_cat['code']
		lev2_instance.name = lev2_cat['name']
		lev2_instance.category_type = 2
		lev2_instance.parent_category = lev1_instance
		lev2_instance.save()

		# 三级类
		for lev3_cat in lev2_cat['sub_categorys']:
			lev3_instance = GoodsCategory()
			lev3_instance.code = lev3_cat["code"]
			lev3_instance.name = lev3_cat["name"]
			lev3_instance.category_type = 3
			lev3_instance.parent_category = lev2_instance
			lev3_instance.save()
