# authin_views 包含登录和回调视图
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from .authin_utils import get_authing_login_url, get_access_token, get_user_info
import requests

# 登录/注册重定向视图
class AuthingLoginRedirectView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        login_url = get_authing_login_url()
        if not login_url:
            return Response({"error":"无法生成登录URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return redirect(login_url)

# 登录回调视图
class AuthingCallbackView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # 获取授权码
        auth_code = request.GET.get('code')
        if not auth_code:
            return Response({"error":"未获取到授权码"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取访问令牌
        # 讲获取的auth_code传参到get_access_token()函数
        token_data = get_access_token(auth_code)
        if not token_data:
            return Response({"error":"无法获取到访问令牌"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 提取令牌(access\id)
        access_token = token_data.get('access_token')
        id_token = token_data.get('id_token')
        if not access_token or not id_token:
            return Response({"error":"未检索到令牌信息"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 获取用户信息
        user_info = get_user_info(access_token)
        if not user_info:
            return Response({"error":"无法获取用户信息"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 返回登录成功获取到的令牌信息及用户信息
        return Response({
            "message":"登录成功",
            "access_token": access_token,
            "id_token": id_token
        })