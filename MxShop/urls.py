"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from MxShop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet
from trade.views import ShoppingCartViewset, OrderViewset
from user_operation.views import LeavingMessageViewset, AddressViewset
from users.views import SmsCodeViewset, UserViewset

router = DefaultRouter()
# 配置goods的url
router.register('goods', GoodsListViewSet)
# 配置category的url
router.register('categorys', CategoryViewSet, base_name='categorys')
# 配置codes的url
router.register('code', SmsCodeViewset, base_name='code')
# 配置users的url
router.register('users', UserViewset, base_name='users')
# 配置用户收藏的url
router.register('userfavs', UserViewset, base_name="userfavs")
# 配置用户留言的url
router.register('messages', LeavingMessageViewset, base_name='messages')
# 配置收货地址url
router.register('address', AddressViewset, base_name='address')
# 配置购物车的url
router.register('shopcarts', ShoppingCartViewset, base_name='shopcarts')
# 配置订单的url
router.register('orders', OrderViewset, base_name='orders')

urlpatterns = [
	path('xadmin/', xadmin.site.urls),
	path('ueditor/', include('DjangoUeditor.urls')),
	# 文件
	path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
	# drf文档，title自定义
	path('docs', include_docs_urls(title='旺达的鱼')),
	path('api-auth/', include('rest_framework.urls')),
	# 商品列表页
	re_path('^', include(router.urls)),
	# jwt
	path('login/', obtain_jwt_token),
]
