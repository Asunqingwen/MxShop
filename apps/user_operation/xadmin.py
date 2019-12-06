# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 0005 13:43
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: xadmin.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
import xadmin

from .models import UserFav, UserLeavingMessage, UserAddress


class UserFavAdmin(object):
	list_display = ['user', 'goods', 'add_time']


class UserLeavingMessageAdmin(object):
	list_display = ['user', 'message_type', 'message', 'add_time']


class UserAddressAdmin(object):
	list_display = ['signer_name', 'signer_mobile', 'district', 'address']


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
