# services/token_service.py
import json
from pathlib import Path
from typing import Dict, Optional, Any
from config import Config
import logging

logger = logging.getLogger(__name__)

class TokenService:
    """Token服务"""
    
    def __init__(self):
        Config.init_dirs()
        self.tokens: Dict[str, Dict] = {}
        self.load_tokens()
    
    def get_token_path(self, api_name: str) -> Path:
        """获取token文件路径"""
        return Config.TOKENS_DIR / f"{api_name}_token.json"
    
    def load_tokens(self):
        """加载所有保存的token"""
        token_dir = Config.TOKENS_DIR
        
        for token_file in token_dir.glob("*_token.json"):
            api_name = token_file.stem.replace("_token", "")
            try:
                with open(token_file, 'r', encoding='utf-8') as f:
                    self.tokens[api_name] = json.load(f)
                logger.info(f"加载 {api_name} 的token")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logger.error(f"加载 {api_name} 的token失败: {e}")
    
    def save_token(self, api_name: str, token_data: Dict[str, Any]) -> bool:
        """保存token"""
        try:
            token_file = self.get_token_path(api_name)
            
            with open(token_file, 'w', encoding='utf-8') as f:
                json.dump(token_data, f, ensure_ascii=False, indent=2)
            
            self.tokens[api_name] = token_data
            logger.info(f"{api_name} 的token已保存")
            return True
        except Exception as e:
            logger.error(f"保存token失败: {e}")
            return False
    
    def get_token(self, api_name: str, key: str = "access_token") -> Optional[str]:
        """获取指定API的token"""
        if api_name in self.tokens:
            return self.tokens[api_name].get(key)
        return None
    
    def clear_token(self, api_name: str) -> bool:
        """清除token"""
        try:
            token_file = self.get_token_path(api_name)
            if token_file.exists():
                token_file.unlink()
            if api_name in self.tokens:
                del self.tokens[api_name]
            logger.info(f"已清除 {api_name} 的token")
            return True
        except Exception as e:
            logger.error(f"清除token失败: {e}")
            return False
    
    def has_valid_token(self, api_name: str, min_length: int = 10) -> bool:
        """检查是否有有效的token"""
        token = self.get_token(api_name)
        return token is not None and len(token) >= min_length