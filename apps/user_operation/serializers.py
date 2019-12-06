# -*- coding: utf-8 -*-
# @Time    : 2019/12/6 0006 15:27
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: serializers.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from user_operation.models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
	# 获取当前登录的用户
	user = serializers.HiddenField(
		default=serializers.CurrentUserDefault()
	)

	class Meta:
		# validate实现唯一联合，一个商品只能收藏一次
		validators = [
			UniqueTogetherValidator(
				queryset=UserFav.objects.all(),
				fields=('user', 'goods'),
				# message的信息可以自定义
				message="已经收藏"
			)
		]
		model = UserFav
		# 收藏的时候需要返回商品的id，因为取消收藏的时候必须知道商品的id是多少
		fields = ("user", "goods", "id")
