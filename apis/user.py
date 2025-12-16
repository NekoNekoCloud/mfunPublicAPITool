# apis/user.py
import logging
from typing import Dict
from utils.request_handler import RequestHandler

logger = logging.getLogger(__name__)

class UserAPI:
    """用户相关API"""
    
    def __init__(self, request_handler: RequestHandler):
        self.request_handler = request_handler
    
    def get_user_info(self) -> Dict:
        """获取用户信息"""
        endpoint = "/user/info"
        
        logger.info("获取用户信息")
        return self.request_handler.get(endpoint)