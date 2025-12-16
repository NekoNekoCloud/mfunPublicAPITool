# utils/request_handler.py
import requests
import json
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from config import Config

logger = logging.getLogger(__name__)

class RequestHandler:
    """基础请求处理器"""
    
    def __init__(self, base_url: str = Config.MFUNS_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """设置session基础配置"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
            "Accept": "application/json",
            "Accept-Encoding": Config.MFUNS_ACCEPT_ENCODING,
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Content-Type": "application/json",
        }
        
        # 添加MFuns特定的请求头
        headers.update(Config.MFUNS_HEADERS)
        self.session.headers.update(headers)
    
    def set_auth_token(self, token: str):
        """设置认证token"""
        # MFuns API使用直接token，不加Bearer前缀
        self.session.headers.update({"Authorization": token})
        logger.debug(f"已设置认证token: {token[:30]}...")
    
    def remove_auth_token(self):
        """移除认证token"""
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
            logger.debug("已移除认证token")
    
    def build_url(self, endpoint: str) -> str:
        """构建完整URL"""
        # 确保base_url以斜杠结尾，endpoint不以斜杠开头
        base = self.base_url.rstrip('/')
        endpoint = endpoint.lstrip('/')
        return f"{base}/{endpoint}"
    
    def _save_request_log(self, method: str, url: str, data: Any = None):
        """保存请求日志"""
        timestamp = int(time.time())
        filename = f"request_{method}_{datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M%S')}.json"
        filepath = Config.RESPONSES_DIR / filename
        
        log_data = {
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
            "method": method,
            "url": url,
            "headers": dict(self.session.headers),
            "data": data
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            logger.error(f"保存请求日志失败: {e}")
    
    def _save_response_log(self, method: str, url: str, response: requests.Response):
        """保存响应日志"""
        timestamp = int(time.time())
        filename = f"response_{method}_{datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M%S')}.json"
        filepath = Config.RESPONSES_DIR / filename
        
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            response_data = {"raw_text": response.text[:1000]}
        
        log_data = {
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
            "method": method,
            "url": url,
            "status_code": response.status_code,
            "response": response_data
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            logger.error(f"保存响应日志失败: {e}")
        
        return response_data
    
    def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送请求"""
        url = self.build_url(endpoint)
        
        logger.info(f"请求: {method} {url}")
        if 'json' in kwargs:
            logger.debug(f"请求数据: {kwargs['json']}")
        
        # 保存请求日志
        self._save_request_log(method, url, kwargs.get('json'))
        
        for attempt in range(Config.MAX_RETRIES):
            try:
                response = self.session.request(
                    method, url,
                    timeout=Config.DEFAULT_TIMEOUT,
                    **kwargs
                )
                
                logger.info(f"响应: {response.status_code}")
                
                # 保存响应日志
                response_data = self._save_response_log(method, url, response)
                
                return {
                    "success": response.status_code == 200,
                    "data": response_data,
                    "status_code": response.status_code,
                    "url": url
                }
                
            except requests.exceptions.RequestException as e:
                logger.error(f"请求失败 (尝试 {attempt + 1}/{Config.MAX_RETRIES}): {e}")
                if attempt == Config.MAX_RETRIES - 1:
                    return {
                        "success": False,
                        "error": str(e),
                        "url": url
                    }
                time.sleep(1)
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """GET请求"""
        return self.request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """POST请求"""
        return self.request("POST", endpoint, json=data)