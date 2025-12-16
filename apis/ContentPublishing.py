# apis/ContentPublishing.py
import logging
from typing import Dict, Optional
from utils.request_handler import RequestHandler

logger = logging.getLogger(__name__)

class ContentPublishingAPI:
    """内容发布相关API"""
    
    def __init__(self, request_handler: RequestHandler):
        self.request_handler = request_handler

    def update_article(
        self, 
        title: str, 
        cid: int, 
        content: str, 
        cover: str = "", 
        tags: str = "", 
        copyright: int = 2, 
        draft: bool = False, 
        contribute_id: Optional[int] = None
    ) -> Dict:
        """
        更新文章
        
        参数:
            title: 文章标题
            cid: 频道ID
            content: 文章内容（JSON格式）
            cover: 封面图片URL
            tags: 标签，多个用逗号分隔
            copyright: 版权类型 (1=原创, 2=转载, 3=未定义)
            draft: 是否为草稿
            contribute_id: 内容ID（更新已有文章时使用）
        """
        endpoint = "/contribute/article/update"
        
        data = {
            "title": title,
            "cid": cid,
            "content": content,
            "cover": cover,
            "tags": tags,
            "copyright": copyright,
            "draft": draft,
        }
        
        # 如果有内容ID，添加到数据中
        if contribute_id:
            data["contribute_id"] = contribute_id
        
        logger.info(f"更新文章: {title}, 频道ID: {cid}")
        return self.request_handler.post(endpoint, data)
    
    # def get_article(self, contribute_id: int) -> Dict:
    #     """获取文章信息"""
    #     endpoint = f"/article/{contribute_id}"
    #     logger.info(f"获取文章信息: ID={contribute_id}")
    #     return self.request_handler.get(endpoint)
    
    # def list_articles(self, page: int = 1, limit: int = 10) -> Dict:
    #     """获取文章列表"""
    #     endpoint = "/article/list"
    #     params = {
    #         "page": page,
    #         "limit": limit
    #     }
    #     logger.info(f"获取文章列表: 第{page}页, 每页{limit}条")
    #     return self.request_handler.get(endpoint, params=params)



# 负载示例
# {
#     "title": "喵御宅网站",
#     "cid": 44,    频道id
#     "content": "{\"ops\":[{\"attributes\":{\"link\":\"https://www.mfuns.net/\"},\"insert\":\"喵御宅官网，兴趣至上的ACGN社区(。゜ω゜)ノ\\\"!\"},{\"insert\":\"\\n\\n\"}]}",
#     "cover": "https://resource.mfuns.net/image/default/default_cover.jpg",
#     "tags": "喵御宅",
#     "copyright": 2,版权：原创、转载、未定义
#     "draft": false,非草稿
#     "contribute_id": 170079   内容
# }