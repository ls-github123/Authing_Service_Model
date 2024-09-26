from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# 测试访问视图
class TestUseView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({"messgae":"测试通过"}, status=status.HTTP_200_OK)