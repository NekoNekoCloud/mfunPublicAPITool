# params/no_param_collector.py
from typing import Dict, Any
from params.collectors import BaseParamCollector

class NoParamCollector(BaseParamCollector):
    """无参数收集器"""
    
    def collect(self, api_name: str) -> Dict[str, Any]:
        return {}
    
    def needs_input(self) -> bool:
        return False