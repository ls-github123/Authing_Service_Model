from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .authin_utils import verify_jwt_token

class ProtectedView(APIView):
    # 受保护的视图,用户必须携带 JWT 令牌访问
    permission_classes = [IsAuthenticated] # 确保用户必须通过JWT认证
    
    def get(self, request):
        # 从请求头中提取 Authorization: Bearer <access_token>
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error':'未提供令牌'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = auth_header.split(' ')[1] # 从请求头中提取 Bearer 令牌
        
        # 验证JWT令牌
        claims = verify_jwt_token(token)
        if not claims:
            return Response({'error':'令牌无效'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 验证通过，返回对应用户数据或其他信息
        return Response({'message': 'Token is valid', 'claims': claims}, status=status.HTTP_200_OK)