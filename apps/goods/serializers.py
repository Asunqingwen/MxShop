# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 0005 14:42
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: serializers.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
	"""
	三级分类
	"""

	class Meta:
		model = GoodsCategory
		fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
	"""
	二级分类
	"""
	# 在parent_category字段中定义的related_name="sub_cat"
	sub_cat = CategorySerializer3(many=True)

	class Meta:
		model = GoodsCategory
		fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
	"""
	一级分类
	"""
	sub_cat = CategorySerializer2(many=True)

	class Meta:
		model = GoodsCategory
		fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
	"""
	商品列表序列化器
	"""
	category = CategorySerializer()

	class Meta:
		model = Goods
		fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
	"""
	轮播图
	"""

	class Meta:
		model = GoodsImage
		fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
	"""
	商品列表页
	"""
	# 覆盖外键字段
	category = CategorySerializer()
	# images是数据库中设置的related_name="images",把轮播图嵌套进来
	images = GoodsImageSerializer(many=True)

	class Meta:
		model = Goods
		fields = '__all__'
