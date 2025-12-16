# ui/manager.py
import sys
from typing import List, Tuple, Dict, Any, Callable

class UIManager:
    """用户界面管理器"""
    
    def __init__(self):
        pass
    
    def display_header(self, title: str):
        """显示标题"""
        print("\n" + "=" * 60)
        print(f" {title}")
        print("=" * 60)
    
    def display_menu(self, title: str, items: List[Tuple[str, str]], show_back: bool = True) -> int:
        """显示菜单并获取选择"""
        self.display_header(title)
        
        for i, (name, description) in enumerate(items, 1):
            print(f"  {i}. {name} - {description}")
        
        if show_back:
            print(f"  0. 返回")
        
        return self.get_choice(0, len(items))
    
    def get_choice(self, min_val: int, max_val: int) -> int:
        """获取用户选择"""
        while True:
            try:
                choice = input(f"\n请选择 ({min_val}-{max_val}): ").strip()
                value = int(choice)
                
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"请输入 {min_val} 到 {max_val} 之间的数字")
            except ValueError:
                print("请输入有效的数字")
    
    def confirm(self, message: str) -> bool:
        """确认对话框"""
        response = input(f"{message} (y/N): ").strip().lower()
        return response == 'y'
    
    def display_result(self, result: Dict[str, Any]):
        """显示API执行结果"""
        print("\n" + "=" * 40)
        print("API执行结果:")
        print("=" * 40)
        
        if result.get("success"):
            print(f" {result.get('api_name', 'API')} 执行成功")
            print(f"描述: {result.get('description', '')}")
            
            api_result = result.get("result", {})
            if api_result:
                print("\n返回数据:")
                for key, value in api_result.items():
                    if isinstance(value, dict):
                        print(f"  {key}:")
                        for k, v in value.items():
                            print(f"    {k}: {v}")
                    else:
                        print(f"  {key}: {value}")
        else:
            print(f"执行失败: {result.get('message', '未知错误')}")
    
    def wait_for_continue(self):
        """等待用户继续"""
        input("\n按Enter键继续...")