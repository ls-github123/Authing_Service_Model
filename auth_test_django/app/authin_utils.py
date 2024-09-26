# authing_utils 处理 Authing 的登录和用户信息获取逻辑
from decouple import config
import requests
from authing import AuthenticationClient
from cachetools import cached, TTLCache
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from jwt import ExpiredSignatureError, InvalidTokenError
import base64

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
cache = TTLCache(maxsize=1, ttl=3600*24*7)

# 从 Authing 的 JWKS 端点获取公钥
@cached(cache) # cached装饰器-将公钥缓存到内存中 避免重复请求 Authing 的 JWKS 端点
def get_authing_jwks():
    try:
        # 请求Authing Jwks端点
        response = requests.get(config("AUTHING_APP_JWKS"))
        response.raise_for_status() # 检查请求结果
        jwks_data = response.json()
        print(f"打印JWKS公钥信息以调试:{jwks_data}")
        
        # 检查是否存在'keys'键,并返回第一个密钥
        if 'keys' in jwks_data and len(jwks_data['keys']) > 0:
            return jwks_data['keys'][0]
        else:
            print("JWKS数据中未检索到密钥")
            return None
    except requests.exceptions.RequestException as e:
        print(f"从 Authing 获取 JWKS 时出错:{e}")
        return None

# 将 JWKS 中的公钥数据转换为 PEM 格式
def get_pem_from_jwks(jwks_key):
    """
    将 JWKS 中的公钥数据转换为 PEM 格式。
    :param jwks_key: 从 JWKS 获取的包含 'n' 和 'e' 的 RSA 公钥数据。
    :return: PEM 格式的公钥字符串。
    """
    try:
        # Base64 URL 解码 'n' 和 'e' decode 转换为字节串
        n = int.from_bytes(base64.urlsafe_b64decode(jwks_key['n'] + '=='), 'big')
        e = int.from_bytes(base64.urlsafe_b64decode(jwks_key['e'] + '=='), 'big')
        
        # 使用 cryptography 生成 RSA 公钥
        public_key = rsa.RSAPublicNumbers(e, n).public_key()
        
        # 将公钥导出为 PEM 格式
        pem_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # 解码为 UTF-8 字符串
        pem_key_str = pem_key.decode('utf-8') # 将字节串解码为字符串
        print(f"PEM 公钥: {pem_key_str}")
        return pem_key_str
    except Exception as e:
        print(f'从JWKS数据生成PEM公钥时出错: {e}')
        return None

# 获取并缓存 PEM 格式公钥
def get_cached_authing_public_key():
    """
    获取并缓存的 Authing 公钥，转换为 PEM 格式
    return: PEM 格式的公钥字符串
    """
    jwks_key = get_authing_jwks() # 从缓存或请求获取jwks数据
    if jwks_key: # 如果jwks数据存在, 则执行PEM公钥转换
        return get_pem_from_jwks(jwks_key) # 转换并返回 PEM 公钥
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