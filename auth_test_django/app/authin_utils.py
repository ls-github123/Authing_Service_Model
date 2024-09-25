# authing_utils 处理 Authing 的登录和用户信息获取逻辑
from decouple import config
import requests
from authing import AuthenticationClient
from jwcrypto import jwt, jwk
from cachetools import cached, TTLCache

# 重定向到 Authing 托管登录页
# 生成用于登录的一次性地址链接

# 初始化 AuthenticationClient
authentication_client = AuthenticationClient(
    # Authing 应用 ID
    app_id = config('AUTHING_APP_ID'),
    # Authing应用密钥
    app_secret = config('AUTHING_APP_SECRET'),
    # Authing 应用地址
    app_host = config('AUTHING_APP_HOST'),
    # Authing 应用配置的登录回调地址
    redirect_uri = config('AUTHING_APP_REDIRECT_URI'),
)

# 缓存公钥, 配置过期时间
# maxsize 缓存中允许存储的最大条目数量
# ttl-time to live 生存时间(秒)
cache = TTLCache(maxsize=1, ttl=3600)

# 从 Authing 的 JWKS 端点获取公钥
@cached(cache)
def get_authing_jwks():
    try:
        # 请求Authing Jwks端点
        response = requests.get(config("AUTHING_APP_JWKS"))
        response.raise_for_status() # 检查请求结果
        jwks_data = response.json()
        print(f"打印JWKS公钥信息以调试:{jwks_data}")
        return jwks_data['keys'][0] # 获取 JWKS 数据中的第一个密钥
    except requests.exceptions.RequestException as e:
        print(f"从 Authing 获取 JWKS 时出错:{e}")
        return None
    
# 验证 JWT 令牌
def verify_jwt_token(token):
    """
    使用 Authing 的公钥验证 JWT 令牌。
    :param token: 前端传递的 JWT 令牌
    :return: 验证成功返回解码后的 claims,失败返回 None
    """
    try:
        # 获取Authing公钥
        jwks_key = get_authing_jwks()
        if not jwks_key:
            return None
        
        # 使用公钥验证 JWT 签名
        key = jwk.JWK(**jwks_key)
        token_obj = jwt.JWT(key=key, jwt=token)
        
        # 返回解码后的 claims 数据
        claims = token_obj.claims
        return claims
    except Exception as e:
        print(f"JWT 验证失败: {e}")
        return None


# 获取 Authing 托管登录页的授权URL
def get_authing_login_url():
    try:
        login_url = authentication_client.build_authorize_url()
        return login_url
    except Exception as e:
        print(f"生成 Authing 登录URL时出错:{e}")
        return None

# 使用授权码请求访问令牌
def get_access_token(auth_code):
    try:
        token_data = authentication_client.get_access_token_by_code(auth_code)
        return token_data
    except requests.exceptions.RequestException as e:
        print(f"请求访问令牌时出错:{e}")
        return None
    except Exception as e:
        print(f"请求访问令牌时出现意外错误:{e}")
        return None


# 获取用户信息
# 使用访问令牌手动通过(用户信息端点 /me 路径)获取
def get_user_info(access_token):
    try:
        headers = {
            'Authorization':f'Bearer {access_token}',
        }
        response = requests.get(config("AUTHING_APP_USERINFO"), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user info from Authing: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching user info: {e}")
        return None