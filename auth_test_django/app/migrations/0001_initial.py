# Generated by Django 5.1.1 on 2024-09-24 12:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='订单ID')),
                ('money', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='订单金额')),
                ('addtime', models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')),
                ('pay_status', models.CharField(max_length=50, verbose_name='支付状态')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
                'db_table': 'order_info',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='AUTHING_ID')),
                ('arn', models.CharField(blank=True, max_length=255, null=True, verbose_name='ARN_ID')),
                ('user_pool_id', models.CharField(max_length=64, verbose_name='AUTHING_用户池ID')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='用户名')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='邮箱')),
                ('email_verified', models.BooleanField(default=False, verbose_name='是否验证邮箱')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='手机号')),
                ('phone_verified', models.BooleanField(default=False, verbose_name='是否验证手机')),
                ('unionid', models.CharField(blank=True, max_length=100, null=True, verbose_name='union_id')),
                ('openid', models.CharField(blank=True, max_length=100, null=True, verbose_name='open_id')),
                ('nickname', models.CharField(blank=True, max_length=100, null=True, verbose_name='昵称')),
                ('register_source', models.JSONField(blank=True, null=True, verbose_name='注册来源')),
                ('photo', models.URLField(blank=True, null=True, verbose_name='头像URL')),
                ('logins_count', models.IntegerField(default=0, verbose_name='登录次数')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='最后登录时间')),
                ('last_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='最后登录IP')),
                ('signed_up', models.DateTimeField(blank=True, null=True, verbose_name='注册时间')),
                ('blocked', models.BooleanField(default=False, verbose_name='是否禁用')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('gender', models.CharField(choices=[('M', '男'), ('F', '女'), ('U', '未知')], default='U', max_length=1, verbose_name='性别')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='出生日期')),
                ('address', models.JSONField(blank=True, null=True, verbose_name='地址信息')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'db_table': 'user_profile',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gid', models.CharField(max_length=255, verbose_name='商品ID')),
                ('gname', models.CharField(max_length=100, verbose_name='商品名称')),
                ('comment_status', models.BooleanField(default=False, verbose_name='是否评价')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='app.order', verbose_name='关联订单')),
            ],
            options={
                'verbose_name': '订单详情',
                'verbose_name_plural': '订单详情',
                'db_table': 'order_detail',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ThirdPartyLogin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=100, verbose_name='三方用户ID')),
                ('provider', models.CharField(max_length=50, verbose_name='登录类型')),
                ('unionid', models.CharField(blank=True, max_length=100, null=True, verbose_name='UNION_ID')),
                ('openid', models.CharField(blank=True, max_length=100, null=True, verbose_name='OPEN_ID')),
                ('login_time', models.DateTimeField(auto_now_add=True, verbose_name='登录时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='third_party_logins', to='app.userprofile', verbose_name='关联本地用户')),
            ],
            options={
                'verbose_name': '三方登录信息',
                'verbose_name_plural': '三方登录信息',
                'db_table': 'thirdpartylogin',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField(verbose_name='评价详情')),
                ('level', models.CharField(choices=[(1, '差'), (2, '一般'), (3, '优')], max_length=1, verbose_name='评价等级')),
                ('gid', models.CharField(max_length=255, verbose_name='商品ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app.userprofile', verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '评价信息',
                'verbose_name_plural': '评价信息',
                'db_table': 'review',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='app.userprofile', verbose_name='订单用户'),
        ),
    ]
