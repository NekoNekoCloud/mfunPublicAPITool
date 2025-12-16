# apis/auth.py
import time
import logging
from typing import Dict
from services.token_service import TokenService
from utils.request_handler import RequestHandler

logger = logging.getLogger(__name__)

class AuthAPI:
    """认证相关API"""
    
    def __init__(self, request_handler: RequestHandler, token_manager: TokenService):
        self.request_handler = request_handler
        self.token_manager = token_manager
    
    def login(self, account: str, password: str) -> bool:
        """用户登录"""
        endpoint = "/auth/login"
        data = {
            "account": account,
            "password": password
        }
        
        logger.info(f"登录: {account}")
        
        # 移除认证token（登录请求不需要）
        original_auth = self.request_handler.session.headers.get("Authorization")
        self.request_handler.remove_auth_token()
        
        try:
            result = self.request_handler.post(endpoint, data)
            
            if result["success"]:
                response_data = result["data"]
                
                if response_data.get("code") == 1:
                    token = response_data["data"]["access_token"]
                    
                    # 保存token
                    self.token_manager.save_token("mfuns", {
                        "access_token": token,
                        "account": account,
                        "login_time": int(time.time())
                    })
                    
                    # 设置认证token
                    self.request_handler.set_auth_token(token)
                    
                    logger.info("登录成功")
                    return True
                else:
                    logger.error(f"登录失败: {response_data.get('msg')}")
            else:
                logger.error(f"请求失败: {result.get('error')}")
            
            return False
        finally:
            # 恢复原来的认证token
            if original_auth:
                self.request_handler.session.headers["Authorization"] = original_auth