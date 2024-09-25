from django.db import models

# 用户信息及权限系统模型
class UserProfile(models.Model):
    id = models.CharField('AUTHING_ID', primary_key=True, max_length=64) # # Authing 用户唯一ID
    arn = models.CharField('ARN_ID', max_length=255, null=True, blank=True) # 用户ARN(Authing中用户的唯一标识)
    user_pool_id = models.CharField('AUTHING_用户池ID', max_length=64)  # 用户池 ID(标识用户所属的 Authing 用户池)
    username = models.CharField('用户名', max_length=150, unique=True)  # 本地用户名
    email = models.EmailField('邮箱', unique=True, blank=True, null=True)  # 邮箱
    email_verified = models.BooleanField('是否验证邮箱', default=False)  # 是否验证邮箱
    phone = models.CharField('手机号', max_length=20, unique=True, null=True, blank=True)  # 手机号码
    phone_verified = models.BooleanField('是否验证手机', default=False)  # 是否验证手机
    unionid = models.CharField('union_id', max_length=100, null=True, blank=True)  # 三方登录 unionid
    openid = models.CharField('open_id', max_length=100, null=True, blank=True)  # 三方登录 openid
    nickname = models.CharField('昵称', max_length=100, null=True, blank=True)  # 昵称
    register_source = models.JSONField('注册来源', null=True, blank=True)  # 注册来源
    photo = models.URLField('头像URL', null=True, blank=True)  # 用户头像 URL
    logins_count = models.IntegerField('登录次数', default=0)  # 登录次数
    last_login = models.DateTimeField('最后登录时间', null=True, blank=True)  # 最后登录时间
    last_ip = models.GenericIPAddressField('最后登录IP', null=True, blank=True)  # 最后登录 IP
    signed_up = models.DateTimeField('注册时间', null=True, blank=True)  # 注册时间
    blocked = models.BooleanField('是否禁用', default=False)  # 是否被封禁
    is_deleted = models.BooleanField('是否删除', default=False)  # 是否被删除
    gender = models.CharField(max_length=1, choices=[('M', '男'), ('F', '女'), ('U', '未知')], default='U', verbose_name='性别')  # 性别
    birthdate = models.DateField('出生日期', null=True, blank=True)  # 出生日期
    address = models.JSONField('地址信息', null=True, blank=True)  # 地址信息，包含街道、城市、地区、邮编、国家等
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField('修改时间', auto_now=True)  # 更新时间

    class Meta:
        db_table = 'user_profile'
        managed = True
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
    
    def __str__(self):
        return self.username
    
# 三方登录表模型
class ThirdPartyLogin(models.Model):
    id = models.AutoField('ID', primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='third_party_logins', verbose_name='关联本地用户')
    uid = models.CharField('三方用户ID', max_length=100)  # 第三方平台用户ID
    provider = models.CharField('登录类型', max_length=50)  # 登录类型或平台（如微信、GitHub等）
    unionid = models.CharField('UNION_ID', max_length=100, null=True, blank=True)  # 三方登录 unionid
    openid = models.CharField('OPEN_ID', max_length=100, null=True, blank=True)  # 三方登录 openid
    login_time = models.DateTimeField('登录时间', auto_now_add=True)  # 登录时间
    
    class Meta:
        db_table = 'thirdpartylogin'
        managed = True
        verbose_name = '三方登录信息'
        verbose_name_plural = '三方登录信息'
        
    def __str__(self):
        # 返回用户昵称(nickname)和三方登录类型(provider)之间的组合
        return f'{self.user.nickname} - {self.provider}'
    

# 订单信息表
class Order(models.Model):
    # models.AutoField 用于自动生成并管理整数类型的主键（ID）
    id = models.AutoField('订单ID', primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders', verbose_name='订单用户') # 关联用户
    money = models.DecimalField('订单金额', max_digits=10, decimal_places=2) # 订单金额
    addtime = models.DateTimeField('订单创建时间', auto_now_add=True)
    pay_status = models.CharField('支付状态', max_length=50) # 支付状态（如已支付、未支付）
    
    class Meta:
        db_table = 'order_info'
        managed = True
        verbose_name = '订单信息'
        verbose_name_plural = '订单信息'
        
    def __str__(self):
        return f'Order {self.id} - User: {self.user.nickname}'
    
# 订单详情表
class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details', verbose_name='关联订单') # 关联订单
    gid = models.CharField('商品ID', max_length=255)
    gname = models.CharField('商品名称', max_length=100)
    comment_status = models.BooleanField('是否评价', default=False)  # 是否已评价
    
    class Meta:
        db_table = 'order_detail'
        managed = True
        verbose_name = '订单详情'
        verbose_name_plural = '订单详情'
        
    def __str__(self):
        return f'Order {self.order.id} - Product: {self.gname}'
    
# 评价信息表
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews', verbose_name='关联用户')
    message = models.TextField('评价详情')
    level = models.CharField(choices=[(1, '差'), (2, '一般'), (3, '优')], max_length=1, verbose_name='评价等级')
    gid = models.CharField('商品ID', max_length=255)
    
    class Meta:
        db_table = 'review'
        managed = True
        verbose_name = '评价信息'
        verbose_name_plural = '评价信息'
        
    def __str__(self):
        return f'Review by {self.user.nickname} for Product {self.gid}'