from typing import Dict, Any
from params.collectors import BaseParamCollector

class UpdateArticleParamCollector(BaseParamCollector):
    """更新文章参数收集器"""
    
    def collect(self, api_name: str) -> Dict[str, Any]:
        print(f"\n{api_name} 参数设置:")
        print("-" * 30)
        
        params = {}
        
        # 收集必填参数
        title = input("文章标题 (必填): ").strip()
        while not title:
            print("标题不能为空!")
            title = input("文章标题 (必填): ").strip()
        params["title"] = title
        
        cid = input("频道ID (必填，默认: 44): ").strip()
        if not cid:
            cid = "44"
        params["cid"] = int(cid)
        
        content = input("文章内容 (JSON格式，按Enter使用默认): ").strip()
        if content:
            params["content"] = content
        else:
            params["content"] = '{"ops":[{"attributes":{"link":"https://www.mfuns.net/"},"insert":"喵御宅官网，兴趣至上的ACGN社区(。゜ω゜)ノ!"},{"insert":"\\n\\n"}]}'
        
        # 收集可选参数
        cover = input("封面图片URL (按Enter跳过): ").strip()
        if cover:
            params["cover"] = cover
        
        tags = input("标签 (多个用逗号分隔，按Enter使用默认): ").strip()
        if tags:
            params["tags"] = tags
        else:
            params["tags"] = "喵御宅"
        
        copyright_choice = input("版权类型 (1=原创, 2=转载, 3=未定义，默认: 2): ").strip()
        if copyright_choice in ["1", "2", "3"]:
            params["copyright"] = int(copyright_choice)
        else:
            params["copyright"] = 2
        
        draft = input("是否为草稿? (y/N): ").strip().lower()
        params["draft"] = draft == 'y'
        
        contribute_id = input("内容ID (更新已有文章时填写，创建新文章留空): ").strip()
        if contribute_id:
            params["contribute_id"] = int(contribute_id)
        
        return params
    
    def needs_input(self) -> bool:
        return True

class GetArticleParamCollector(BaseParamCollector):
    """获取文章参数收集器"""
    
    def collect(self, api_name: str) -> Dict[str, Any]:
        print(f"\n{api_name} 参数设置:")
        print("-" * 30)
        
        contribute_id = input("内容ID (必填): ").strip()
        while not contribute_id:
            print("内容ID不能为空!")
            contribute_id = input("内容ID: ").strip()
        
        return {"contribute_id": int(contribute_id)}
    
    def needs_input(self) -> bool:
        return True

class ListArticlesParamCollector(BaseParamCollector):
    """文章列表参数收集器"""
    
    def collect(self, api_name: str) -> Dict[str, Any]:
        print(f"\n{api_name} 参数设置:")
        print("-" * 30)
        
        params = {}
        
        page = input("页码 (默认: 1): ").strip()
        if page:
            params["page"] = int(page)
        
        limit = input("每页数量 (默认: 10): ").strip()
        if limit:
            params["limit"] = int(limit)
        
        return params
    
    def needs_input(self) -> bool:
        return True