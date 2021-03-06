from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

User = get_user_model()


# Create your models here.

class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name=u"商品", on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name=u"购买数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class OrderInfo(models.Model):
    """
    订单信息
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "交易成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付")
    )
    PAY_TYPE = (
        ("alipay", "成功"),
        ("wechat", "微信")
    )
    user = models.ForeignKey(User, verbose_name=u"用户", on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单编号")
    nonce_str = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name="随机加密串")
    trade_on = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name=u"交易号")
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=30, verbose_name="订单状态")
    pay_type = models.CharField(choices=PAY_TYPE, default='alipay', max_length=10, verbose_name="支付类型")
    pay_script = models.CharField(max_length=200, verbose_name="订单留言")
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    # 用户信息
    address = models.CharField(max_length=200, default="", verbose_name="收获地址")
    singer_name = models.CharField(max_length=100, default="", verbose_name="签收人")
    singer_mobile = models.CharField(max_length=11, verbose_name="联系电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    订单内的商品详情
    """
    # 一个订单对应多个商品，所以需要添加外键
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息", related_name="goods", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单内的商品项"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.order_sn
