# apis/__init__.py
from .auth import AuthAPI

# 注册所有可用的API客户端
API_CLIENTS = {
    "auth": AuthAPI,
    # 在这里添加新的API客户端
}

def get_api_client(api_name: str):
    """获取API客户端实例"""
    if api_name in API_CLIENTS:
        return API_CLIENTS[api_name]()
    else:
        raise ValueError(f"未知的API: {api_name}")

def list_available_apis() -> list:
    """列出所有可用的API"""
    return list(API_CLIENTS.keys())