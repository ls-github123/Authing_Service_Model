# authing_utils 处理 Authing 的登录和用户信息获取逻辑
from decouple import config
import requests
from authing import AuthenticationClient

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