# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 0005 16:09
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: filter.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Goods


class GoodsFilter(filters.FilterSet):
	"""
	商品过滤类
	"""
	# 两个参数，name是要过滤的字段，lookup是执行的行为，’小于等于本店价格‘
	price_min = filters.NumberFilter(field_name='shop_price', lookup_expr='gte', help_text='大于等于本店价格')
	price_max = filters.NumberFilter(field_name='shop_price', lookup_expr='lte', help_text='小于等于本店价格')
	# 行为: 名称中包含某字符，且字符不区分大小写
	# name = filters.CharFilter(field_name="name" ,lookup_expr="icontains")
	top_category = filters.NumberFilter(field_name="category", method='top_category_filter')

	def top_category_filter(self, queryset, name, value):
		# 不管当前点击的是一级目录二级目录还是三级目录。
		return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
			category__parent_category__parent_category_id=value))

	class Meta:
		model = Goods
		fields = ['price_min', 'price_max', 'name', 'is_hot', 'is_new']
