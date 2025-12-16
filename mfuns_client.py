# mfuns_client.py
import logging
from services.token_service import TokenService
from utils.request_handler import RequestHandler
from apis.auth import AuthAPI
from apis.contentAccess import ContentAccessAPI
from apis.user import UserAPI

logger = logging.getLogger(__name__)

class MFunsClient:
    """MFuns客户端"""
    
    def __init__(self):
        # 初始化组件
        self.token_manager = TokenService()
        self.request_handler = RequestHandler()
        
        # 初始化API模块
        self.auth = AuthAPI(self.request_handler, self.token_manager)
        self.content = ContentAccessAPI(self.request_handler)
        self.user = UserAPI(self.request_handler)
        
        # 如果有保存的token，自动设置
        self._load_saved_token()
    
    def _load_saved_token(self):
        """加载保存的token"""
        token = self.token_manager.get_token("mfuns")
        if token:
            self.request_handler.set_auth_token(token)
            logger.info("已自动加载保存的token")
    
    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        return self.token_manager.has_valid_token("mfuns")
    
    def login(self, account: str, password: str) -> bool:
        """登录"""
        return self.auth.login(account, password)
    
    def logout(self) -> bool:
        """登出"""
        # 清除token
        self.token_manager.clear_token("mfuns")
        self.request_handler.remove_auth_token()
        logger.info("已登出")
        return True
    
    def test_token_with_like(self, target_id: int = 113180) -> bool:
        """通过点赞测试token是否有效"""
        if not self.is_logged_in():
            return False
        
        result = self.content.like(target_id, 0)
        
        if result["success"] and result["data"].get("code") == 1:
            logger.info("Token有效，点赞成功")
            return True
        else:
            logger.warning("Token无效，点赞失败")
            return False