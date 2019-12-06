# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 0005 13:39
# @Author  : 没有蜡笔的小新
# @E-mail  : sqw123az@sina.com
# @FileName: xadmin.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/Asunqingwen
# @GitHub  ：https://github.com/Asunqingwen
# @WebSite : labixiaoxin.me
import xadmin

from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartAdmin(object):
	list_display = ['user', 'goods', 'nums', ]


class OrderInfoAdmin(object):
	list_display = ['user', 'order_sn', 'trade_no', 'pay_status', 'post_script', 'order_mount',
	                'order_mount', 'pay_time', 'add_time']

	class OrderGoodsInline(object):
		model = OrderGoods
		exclude = ['add_time', ]
		extra = 1
		style = 'tab'

	inlines = [OrderGoodsInline, ]


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
