# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination

from goods.serializers import GoodsSerializer, CategorySerializer
from .filter import GoodsFilter
from .models import Goods, GoodsCategory


class GoodsPagination(PageNumberPagination):
	"""
	商品列表自定义分页
	"""
	# 默认每页显示的个数
	page_size = 10
	# 可以动态改变每页显示的个数
	page_size_query_param = 'page_size'
	# 页码参数
	page_query_param = 'page'
	# 最多能显示多少页
	max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,viewsets.GenericViewSet):
	"""
	商品列表
	"""
	pagination_class = GoodsPagination
	# queryset = Goods.objects.all()  # 利用rest_framework默认分页功能会有警告
	queryset = Goods.objects.all().order_by('id')
	serializer_class = GoodsSerializer
	# 设置三大常用过滤器
	filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

	# 设置排序
	ordering_fields = ('sold_num', 'shop_price')

	# 设置filter的类为我们自定义的类
	filter_class = GoodsFilter

	# 搜索，=name表示精确搜索，也可以使用各种正则表达式
	search_fields = ('=name', 'goods_brief', 'goods_desc')

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	"""
	list:
		商品分类列表数据
	"""
	queryset = GoodsCategory.objects.filter(category_type=1)
	serializer_class = CategorySerializer
