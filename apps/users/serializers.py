# -*- coding: utf-8 -*-
# @Time    : 2019/12/6 0006 13:29
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: serializers.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from MxShop.settings import REGEX_MOBILE
from users.models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
	mobile = serializers.CharField(max_length=11)

	# 函数名必须：validate+验证字段名
	def validate_mobile(self, mobile):
		"""
		手机号码验证
		"""
		# 是否注册
		if User.objects.filter(mobile=mobile).count():
			raise serializers.ValidationError("用户已经存在")

		# 是否合法
		if not re.match(REGEX_MOBILE, mobile):
			raise serializers.ValidationError("手机号码非法")

		# 验证码发送频率
		# 60s只能发送一次
		one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
		if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
			raise serializers.ValidationError("距离上一次发送未超过60s")

		return mobile


class UserRegSerializer(serializers.ModelSerializer):
	"""
	用户注册
	"""
	# UserProfile中没有code字段，这里需要自定义一个code序列化字段
	code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,
	                             error_messages={
		                             "blank": "请输入验证码",
		                             "required": "请输入验证码",
		                             "max_length": "验证码格式错误",
		                             "min_length": "验证码格式错误",
	                             },
	                             help_text="验证码")
	# 验证用户名是否存在
	username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
	                                 validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

	password = serializers.CharField(style={'input_type': 'password'},
	                                 help_text='密码', label='密码',
	                                 write_only=True)

	# 调用父类的create方法，该方法会返回当前model的实例化对象即user
	# 前面是将父类原有的create进行执行，后面是加入自己的逻辑
	def create(self, validated_data):
		user = super(UserRegSerializer, self).create(validated_data=validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user

	# 验证code
	def validate_code(self, code):
		# 用户注册，用post方式提交注册信息，post的数据保存在initial_data里面
		# username就是用户注册的手机号，验证码按添加时间倒序排序，为了后面验证过期，错误等
		verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")

		if verify_records:
			# 最近的一个验证码
			last_record = verify_records[0]
			# 有效期为五分钟
			five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
			if five_minutes_ago > last_record.add_time:
				raise serializers.ValidationError("验证码过期")

			if last_record.code != code:
				raise serializers.ValidationError("验证码错误")

		else:
			raise serializers.ValidationError("验证码错误")

	# 所有字段，attrs是字段验证合法之后返回的总的dict
	def validate(self, attrs):
		# 前端没有传mobile值到后端，这里添加起来
		attrs['mobile'] = attrs['username']
		# code是自己添加的，数据库并没有这个字段，验证完就删除掉
		del attrs["code"]

	class Meta:
		model = User
		fields = ('username', 'code', 'mobile', 'password')
