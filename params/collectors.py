# params/collectors.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from config import Config

class BaseParamCollector(ABC):
    """参数收集器基类"""
    
    @abstractmethod
    def collect(self, api_name: str, **kwargs) -> Dict[str, Any]:
        """收集参数"""
        pass
    
    @abstractmethod
    def needs_input(self) -> bool:
        """是否需要用户输入"""
        pass

class NoParamCollector(BaseParamCollector):
    """无参数收集器"""
    
    def collect(self, api_name: str, **kwargs) -> Dict[str, Any]:
        return {}
    
    def needs_input(self) -> bool:
        return False

class LoginParamCollector(BaseParamCollector):
    """登录参数收集器"""
    
    def collect(self, api_name: str, **kwargs) -> Dict[str, Any]:
        print(f"\n{api_name} 参数设置:")
        print("-" * 30)
        
        use_default = input("是否使用默认测试账号? (y/N): ").strip().lower()
        
        if use_default == 'y':
            return {}
        else:
            account = input("账号: ").strip()
            password = input("密码: ").strip()
            return {"account": account, "password": password}
    
    def needs_input(self) -> bool:
        return True

class LikeParamCollector(BaseParamCollector):
    """点赞参数收集器"""
    
    def collect(self, api_name: str, **kwargs) -> Dict[str, Any]:
        print(f"\n{api_name} 参数设置:")
        print("-" * 30)
        
        params = {}
        target_id = input(f"目标ID (默认: 113180): ").strip()
        like_type = input("类型 (0=文章, 1=视频, ...) (默认: 0): ").strip()
        
        if target_id:
            params["target_id"] = int(target_id)
        if like_type:
            params["like_type"] = int(like_type)
        
        return params
    
    def needs_input(self) -> bool:
        return True

class ParamCollectorFactory:
    """参数收集器工厂"""
    
    _collectors = {
        "登录": LoginParamCollector(),
        "点赞": LikeParamCollector(),
        "取消点赞": LikeParamCollector(),
        "获取点赞状态": LikeParamCollector(),
    }
    
    @classmethod
    def get_collector(cls, api_name: str) -> BaseParamCollector:
        """获取参数收集器"""
        return cls._collectors.get(api_name, NoParamCollector())
    
    @classmethod
    def register_collector(cls, api_name: str, collector: BaseParamCollector):
        """注册参数收集器"""
        cls._collectors[api_name] = collector