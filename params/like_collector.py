# params/like_collector.py
from typing import Dict, Any
from params.collectors import BaseParamCollector

class LikeParamCollector(BaseParamCollector):
    """点赞参数收集器"""
    
    def collect(self, api_name: str) -> Dict[str, Any]:
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