# params/login_collector.py
from typing import Dict, Any
from params.collectors import BaseParamCollector

class LoginParamCollector(BaseParamCollector):
    """登录参数收集器"""
    
    def collect(self, api_name: str) -> Dict[str, Any]:
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