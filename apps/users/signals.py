# -*- coding: utf-8 -*-
# @Time    : 2019/12/6 0006 14:45
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: signals.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


# post_save:接收信号的方式
# sender：接收信号的model
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
	# 是否新建，因为update的时候也会进行post_save
	if created:
		password = instance.password
		# instance相当于user
		instance.set_password(password)
		instance.save()
