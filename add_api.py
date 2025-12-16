#!/usr/bin/env python3
"""
快速添加新API的脚本
"""

import os
import re

def create_api_template(api_name: str, base_url: str, auth_type: str = "bearer"):
    """创建新API的模板文件"""
    
    # 1. 创建API类文件
    api_class_content = f'''"""
{api_name.title()} API客户端
"""

from typing import Dict, Optional
from api_client import BaseAPIClient

class {api_name.title()}API(BaseAPIClient):
    """{api_name.title()} API客户端"""
    
    def __init__(self):
        super().__init__("{api_name}")
    
    # 示例方法1: 登录
    def login(self, username: str, password: str) -> Dict:
        """登录"""
        endpoint = "/auth/login"
        data = {{
            "username": username,
            "password": password
        }}
        return self.post(endpoint, data)
    
    # 示例方法2: 获取数据
    def get_data(self, page: int = 1, limit: int = 10) -> Dict:
        """获取数据"""
        endpoint = "/data"
        params = {{
            "page": page,
            "limit": limit
        }}
        return self.get(endpoint, params=params)
    
    # 添加更多方法...
'''

    # 2. 更新__init__.py
    init_file = "apis/__init__.py"
    with open(init_file, 'r', encoding='utf-8') as f:
        init_content = f.read()
    
    # 添加import
    new_import = f"from .{api_name}_api import {api_name.title()}API"
    if new_import not in init_content:
        # 找到import部分，在最后添加
        lines = init_content.split('\n')
        import_end = 0
        for i, line in enumerate(lines):
            if line.startswith("from .") or line.startswith("import "):
                import_end = i
            elif import_end > 0 and not line.startswith("from .") and not line.startswith("import "):
                break
        
        lines.insert(import_end + 1, new_import)
        init_content = '\n'.join(lines)
    
    # 添加API_CLIENTS
    if f'"{api_name}": {api_name.title()}API' not in init_content:
        # 找到API_CLIENTS字典
        pattern = r'API_CLIENTS = \{([^}]+)\}'
        match = re.search(pattern, init_content, re.DOTALL)
        if match:
            clients_content = match.group(1)
            new_clients = clients_content.rstrip() + f'\n    "{api_name}": {api_name.title()}API,'
            init_content = init_content.replace(clients_content, new_clients)
    
    # 3. 保存文件
    api_file_path = f"apis/{api_name}_api.py"
    with open(api_file_path, 'w', encoding='utf-8') as f:
        f.write(api_class_content)
    
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    # 4. 更新配置文件示例
    print("\n" + "="*60)
    print(f"API模板创建完成！")
    print("="*60)
    print(f"\n1. API类文件已创建: {api_file_path}")
    print(f"\n2. 请在 config.py 中添加配置:")
    print(f"""
    APIS = {{
        "{api_name}": {{
            "base_url": "{base_url}",
            "auth_type": "{auth_type}",
            "accept_encoding": "gzip, deflate"
        }}
    }}
    """)
    print(f"\n3. 使用方法:")
    print(f"    from apis import get_api_client")
    print(f"    api = get_api_client('{api_name}')")
    print(f"    result = api.login('username', 'password')")
    print("\n4. 请根据实际API文档修改模板中的方法")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="快速创建新API模板")
    parser.add_argument("name", help="API名称（英文，如: github, twitter）")
    parser.add_argument("url", help="API基础URL")
    parser.add_argument("--auth", default="bearer", 
                       choices=["bearer", "token_direct", "basic"],
                       help="认证类型")
    
    args = parser.parse_args()
    
    create_api_template(args.name, args.url, args.auth)