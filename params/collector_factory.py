# params/collector_factory.py
from typing import Dict
from params.collectors import BaseParamCollector
from params.no_param_collector import NoParamCollector
from params.login_collector import LoginParamCollector
from params.like_collector import LikeParamCollector
from params.article_params import (
    UpdateArticleParamCollector, 
    GetArticleParamCollector, 
    ListArticlesParamCollector
)

class ParamCollectorFactory:
    """参数收集器工厂"""
    
    # 默认收集器映射
    _collector_mapping = {
        # 认证模块
        "登录": LoginParamCollector(),
        "登出": NoParamCollector(),
        "检查登录状态": NoParamCollector(),
        
        # 内容模块
        "点赞": LikeParamCollector(),
        "取消点赞": LikeParamCollector(),
        "获取点赞状态": LikeParamCollector(),
        
        # 用户模块
        "获取用户信息": NoParamCollector(),
        
        # 文章模块
        "更新文章": UpdateArticleParamCollector(),
        "获取文章信息": GetArticleParamCollector(),
        "获取文章列表": ListArticlesParamCollector(),
    }
    
    @classmethod
    def get_collector(cls, api_name: str) -> BaseParamCollector:
        """获取参数收集器"""
        return cls._collector_mapping.get(api_name, NoParamCollector())
    
    @classmethod
    def register_collector(cls, api_name: str, collector: BaseParamCollector):
        """注册新的参数收集器"""
        cls._collector_mapping[api_name] = collector
    
    @classmethod
    def list_collectors(cls) -> Dict[str, str]:
        """列出所有收集器"""
        return {
            api_name: type(collector).__name__
            for api_name, collector in cls._collector_mapping.items()
        }