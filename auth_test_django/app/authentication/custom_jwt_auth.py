# 自定义JWT认证类
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.contrib.auth.models import User

class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        """
        Override the validation to bypass 'typ' checking and validate the token using UntypedToken.
        """
        try:
            # Use UntypedToken to skip type validation and get a valid token
            token = UntypedToken(raw_token)
            return token
        except jwt.PyJWTError as e:
            raise InvalidToken(f'Invalid token: {str(e)}')
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')

    def get_user(self, validated_token):
        """
        Custom method to extract the user information from the token's payload.
        """
        try:
            # Extract the user identifier from the token payload
            # Authing may use 'sub' as the user identifier instead of 'user_id'
            user_id = validated_token.get('user_id') or validated_token.get('sub')
            
            if user_id is None:
                raise InvalidToken('令牌未包含用户标识符')

            # Try to retrieve the user from the database
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('用户不存在')

            return user

        except KeyError:
            raise InvalidToken('无法从令牌中提取用户标识符')