# apis/contentAccess.py
import logging
from typing import Dict
from utils.request_handler import RequestHandler

logger = logging.getLogger(__name__)

class ContentAccessAPI:
    """内容访问相关API"""
    
    def __init__(self, request_handler: RequestHandler):
        self.request_handler = request_handler
    
    def like(self, target_id: int, like_type: int = 0) -> Dict:
        """点赞"""
        endpoint = "/like/like"
        data = {
            "id": target_id,
            "type": like_type
        }
        
        logger.info(f"点赞: ID={target_id}, Type={like_type}")
        return self.request_handler.post(endpoint, data)