# api_manager.py
import logging
from typing import Dict, List, Tuple, Any, Callable  # 添加 Any 和 Callable
from mfuns_client import MFunsClient

logger = logging.getLogger(__name__)

class APIManager:
    """API管理器 - 管理MFuns网站的所有API接口"""
    
    def __init__(self):
        self.client = MFunsClient()
        self.api_modules = self._init_api_modules()
    
    def _init_api_modules(self) -> Dict[str, Dict[str, Any]]:
        """初始化API模块列表"""
        return {
            "认证模块": {
                "description": "用户认证相关接口",
                "apis": [
                    ("登录", self._test_login, "测试用户登录"),
                    ("登出", self._test_logout, "测试用户登出"),
                    ("检查登录状态", self._test_login_status, "检查用户登录状态"),
                ]
            },
            "内容模块": {
                "description": "内容操作相关接口",
                "apis": [
                    ("点赞", self._test_like, "测试点赞功能"),
                    ("取消点赞", self._test_unlike, "测试取消点赞功能"),
                    ("获取点赞状态", self._test_get_like_status, "获取内容点赞状态"),
                ]
            },
            "用户模块": {
                "description": "用户信息相关接口",
                "apis": [
                    ("获取用户信息", self._test_get_user_info, "获取当前用户信息"),
                ]
            },
            "文章模块": {  # 新增文章模块
                "description": "文章管理相关接口",
                "apis": [
                    ("更新文章", self._test_update_article, "创建或更新文章"),
                ]
            }
            
        }
    
    def list_api_modules(self) -> List[str]:
        """列出所有API模块"""
        return list(self.api_modules.keys())
    
    def list_apis_in_module(self, module_name: str) -> List[Tuple[str, str]]:
        """列出指定模块中的所有API"""
        if module_name not in self.api_modules:
            return []
        
        module = self.api_modules[module_name]
        return [(api[0], api[2]) for api in module["apis"]]
    
    def get_module_description(self, module_name: str) -> str:
        """获取模块描述"""
        if module_name in self.api_modules:
            return self.api_modules[module_name]["description"]
        return ""
    
    def execute_api(self, module_name: str, api_index: int, **kwargs) -> Dict[str, Any]:
        """执行指定的API"""
        if module_name not in self.api_modules:
            return {"success": False, "message": f"模块 '{module_name}' 不存在"}
        
        module = self.api_modules[module_name]
        if api_index < 0 or api_index >= len(module["apis"]):
            return {"success": False, "message": f"API索引 {api_index} 无效"}
        
        api_name, api_func, api_desc = module["apis"][api_index]
        
        try:
            # 确保已登录（需要登录的API）
            if api_name not in ["登录"]:
                if not self.client.is_logged_in():
                    return {"success": False, "message": "请先登录"}
            
            result = api_func(**kwargs)
            return {
                "success": True,
                "api_name": api_name,
                "description": api_desc,
                "result": result
            }
        except Exception as e:
            logger.error(f"执行API失败: {e}")
            return {"success": False, "message": f"执行失败: {str(e)}"}
    
    # 以下是具体的API测试方法
    def _test_login(self, account: str = "", password: str = "") -> Dict[str, Any]:
        """测试登录"""
        if not account or not password:
            return {"success": False, "message": "需要账号和密码"}
        
        success = self.client.login(account, password)
        return {"success": success, "message": "登录成功" if success else "登录失败"}
    
    def _test_logout(self) -> Dict[str, Any]:
        """测试登出"""
        success = self.client.logout()
        return {"success": success, "message": "登出成功" if success else "登出失败"}
    
    def _test_login_status(self) -> Dict[str, Any]:
        """测试登录状态"""
        if self.client.is_logged_in():
            # 测试token是否有效
            token_valid = self.client.test_token_with_like()
            return {
                "success": True,
                "logged_in": True,
                "token_valid": token_valid,
                "message": "已登录" + ("，token有效" if token_valid else "，但token无效")
            }
        else:
            return {"success": True, "logged_in": False, "message": "未登录"}
    
    def _test_like(self, target_id: int = 113180, like_type: int = 0) -> Dict[str, Any]:
        """测试点赞"""
        result = self.client.content.like(target_id, like_type)
        return {
            "success": result["success"],
            "code": result["data"].get("code"),
            "message": result["data"].get("msg", ""),
            "data": result["data"].get("data", {})
        }
    
    def _test_unlike(self, target_id: int = 113180, like_type: int = 0) -> Dict[str, Any]:
        """测试取消点赞"""
        return {"success": False, "message": "取消点赞功能暂未实现"}
    
    def _test_get_like_status(self, target_id: int = 113180, like_type: int = 0) -> Dict[str, Any]:
        """测试获取点赞状态"""
        return {"success": False, "message": "获取点赞状态功能暂未实现"}
    
    def _test_get_user_info(self) -> Dict[str, Any]:
        """测试获取用户信息"""
        result = self.client.user.get_user_info()
        return {
            "success": result["success"],
            "code": result["data"].get("code"),
            "message": result["data"].get("msg", ""),
            "user_info": result["data"].get("data", {})
        }
    
    def add_custom_api(self, module_name: str, api_name: str, api_func: Callable, description: str = ""):
        """添加自定义API"""
        if module_name not in self.api_modules:
            self.api_modules[module_name] = {
                "description": "自定义模块",
                "apis": []
            }
        
        self.api_modules[module_name]["apis"].append((api_name, api_func, description))
        logger.info(f"已添加自定义API: {module_name}/{api_name}")

        # api_manager.py 中添加以下方法
    def _test_update_article(self, **kwargs) -> Dict[str, Any]:
        """测试更新文章"""        
        result = self.client.content_publishing.update_article(**kwargs)
        return {
            "success": result["success"],
            "code": result["data"].get("code"),
            "message": result["data"].get("msg", ""),
            "article_info": result["data"].get("data", {})
        }
