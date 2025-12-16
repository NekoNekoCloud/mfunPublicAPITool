# utils/logger.py
import logging
import sys
from pathlib import Path
from config import Config

def setup_logger(name: str = "api_tester"):
    """设置日志"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # 文件处理器
        file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger

# 创建全局日志实例
logger = setup_logger()