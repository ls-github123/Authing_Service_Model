from rest_framework import serializers
from . import models

# 用户信息及权限系统序列化
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['id', 'username', 'email', 'mobile', 'nickname', 'photo', 'gender', 'last_login', 'logins_count']

# 三方登录信息序列化
class ThirdPartyLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ThirdPartyLogin
        fields = ['id', 'uid', 'provider', 'login_time']


# 订单信息及详情序列化
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDetail
        fields = ['id', 'gid', 'gname', 'comment_status']
        
class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True, read_only=True)
    class Meta:
        model = models.Order
        fields = ['id', 'user', 'money', 'pay_status', 'addtime', 'order_details']


# 评价信息序列化
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'user', 'message', 'level', 'gid']