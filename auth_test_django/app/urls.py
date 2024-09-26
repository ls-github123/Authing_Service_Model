from django.urls import path
from . import authin_views
from .views import TestUseView
urlpatterns = [
    path('authing_login/', authin_views.AuthingLoginRedirectView.as_view(), name='authing_login_redirect'), # 用户登录接口
    path('authing_callback/', authin_views.AuthingCallbackView.as_view(), name='authing_callback'), # 登录回调接口
    path('test/', TestUseView.as_view()),
]