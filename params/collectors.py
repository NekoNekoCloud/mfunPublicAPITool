from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseParamCollector(ABC):
    """参数收集器基类"""
    
    @abstractmethod
    def collect(self, api_name: str) -> Dict[str, Any]:
        """收集参数"""
        pass
    
    @abstractmethod
    def needs_input(self) -> bool:
        """是否需要用户输入"""
        pass