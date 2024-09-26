# 自定义配置 TokenBackend
from rest_framework_simplejwt.backends import TokenBackend

class CustomTokenBackend(TokenBackend):
    def decode(self, token, verify=True):
        # 解码 JWT 令牌，忽略对 `typ` 的严格检查
        decoded = super().decode(token, verify)

        # 如果没有 `typ` 字段，或者 `typ` 字段不为 'access'，手动设置
        if 'typ' not in decoded or decoded['typ'] != 'access':
            decoded['typ'] = 'access'  # 假设为访问令牌
        return decoded