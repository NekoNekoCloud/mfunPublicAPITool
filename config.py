# config.py
import os
import logging
from pathlib import Path
from datetime import datetime

class Config:
    """MFuns API 配置类"""
    
    # 基础路径
    BASE_DIR = Path(__file__).parent.absolute()
    
    # 数据存储路径
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = DATA_DIR / "logs"
    TOKENS_DIR = DATA_DIR / "tokens"
    RESPONSES_DIR = DATA_DIR / "responses"
    
    # MFuns API基础配置
    MFUNS_BASE_URL = "https://api.mfuns.net/v1"
    MFUNS_AUTH_TYPE = "token_direct"  # 直接使用token，不加Bearer
    MFUNS_ACCEPT_ENCODING = "gzip, deflate"
    
    # MFuns API特定请求头
    MFUNS_HEADERS = {
        "DNT": "1",
        "Origin": "https://www.mfuns.net",
        "Referer": "https://www.mfuns.net/",
        "Sec-Ch-Ua": '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Sec-Gpc": "1",
        "Priority": "u=1, i"
    }
    
    # 请求配置
    DEFAULT_TIMEOUT = 30
    RETRY_TIMES = 3
    MAX_RETRIES = 3
    
    # 日志配置
    LOG_LEVEL = logging.DEBUG
    
    @classmethod
    def init_dirs(cls):
        """初始化目录结构"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.TOKENS_DIR.mkdir(exist_ok=True)
        cls.RESPONSES_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def setup_logging(cls):
        """设置日志"""
        # 清除现有的日志处理器
        logging.getLogger().handlers = []
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(cls.LOG_LEVEL)
        console_handler.setFormatter(formatter)
        
        # 文件处理器
        log_file = cls.LOGS_DIR / f"mfuns_api_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(cls.LOG_LEVEL)
        file_handler.setFormatter(formatter)
        
        # 设置根日志器
        root_logger = logging.getLogger()
        root_logger.setLevel(cls.LOG_LEVEL)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        
        return root_logger