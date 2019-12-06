# Create your models here.
# get_user_model方法会去setting中找AUTH_USER_MODEL
from django.contrib.auth import get_user_model

from goods.models import Goods
from utils.common import *

User = get_user_model()


class ShoppingCart(BaseModel):
	"""
	购物车
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
	goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
	nums = models.IntegerField("购买数量", default=0)

	class Meta:
		verbose_name = '购物车'
		verbose_name_plural = verbose_name
		unique_together = ("user", "goods")

	def __str__(self):
		return "%s(%d)".format(self.goods.name, self.nums)


class OrderInfo(BaseModel):
	"""
	订单信息
	"""
	ORDER_STATUS = (
		("TRADE_SUCCESS", "成功"),
		("TRADE_CLOSED", "超时关闭"),
		("WAIT_BUYER_PAY", "交易创建"),
		("TRADE_FINISHED", "交易结束"),
		("paying", "待支付"),
	)
	PAY_TYPE = (
		("alipay", "支付宝"),
		("wechat", "微信"),
	)
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
	# 订单号唯一
	order_sn = models.CharField("订单编号", max_length=30, null=True, blank=True, unique=True)
	# 微信支付
	nonce_str = models.CharField("随机加密串", max_length=50, null=True, blank=True, unique=True)
	# 支付宝支付
	trade_no = models.CharField("交易号", max_length=100, null=True, blank=True, unique=True)
	# 支付状态
	pay_status = models.CharField("订单状态", max_length=30, choices=ORDER_STATUS, default="paying")
	# 订单支付类型
	pay_type = models.CharField("支付类型", max_length=10, choices=PAY_TYPE, default="alipay")
	post_script = models.CharField("订单留言", max_length=200)
	order_mount = models.DecimalField("订单金额", max_digits=11, decimal_places=2, default=0.00)
	pay_time = models.DateTimeField("支付时间", null=True, blank=True)

	# 用户信息
	address = models.CharField("收货地址", max_length=100, default="")
	signer_name = models.CharField("签收人", max_length=20, default="")
	signer_mobile = models.CharField("联系电话", max_length=11)

	class Meta:
		verbose_name = "订单信息"
		verbose_name_plural = verbose_name

	def __str__(self):
		return str(self.order_sn)


class OrderGoods(BaseModel):
	"""
	订单内的商品详情
	"""
	# 一个订单对应多个商品
	order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单信息", related_name="goods")
	# 两个外键形成一张关联表
	goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
	goods_num = models.IntegerField("商品数量", default=0)

	class Meta:
		verbose_name = "订单商品"
		verbose_name_plural = verbose_name

	def __str__(self):
		return str(self.order.order_sn)
