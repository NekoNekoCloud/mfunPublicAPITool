# main.py
import sys
import os
import logging

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from api_manager import APIManager
from ui.manager import UIManager
from params.collectors import ParamCollectorFactory

class MainApp:
    """主应用程序"""
    
    def __init__(self):
        self.ui = UIManager()
        self.api_manager = APIManager()
        self.logger = None
    
    def setup_environment(self):
        """设置环境"""
        Config.init_dirs()
        self.logger = Config.setup_logging()
        
        self.ui.display_header("MFuns API 测试管理器")
    
    def display_main_menu(self) -> int:
        """显示主菜单"""
        modules = self.api_manager.list_api_modules()
        menu_items = []
        
        for module in modules:
            description = self.api_manager.get_module_description(module)
            menu_items.append((module, description))
        
        # 添加测试所有API选项
        menu_items.append(("测试所有API", "批量测试所有API接口"))
        
        return self.ui.display_menu("请选择要测试的API模块", menu_items, show_back=False)
    
    def handle_module_selection(self, module_choice: int):
        """处理模块选择"""
        modules = self.api_manager.list_api_modules()
        
        if module_choice == len(modules) + 1:
            # 测试所有API
            self.test_all_apis()
            return
        
        module_name = modules[module_choice - 1]
        self.handle_module_apis(module_name)
    
    def handle_module_apis(self, module_name: str):
        """处理模块内的API"""
        while True:
            apis = self.api_manager.list_apis_in_module(module_name)
            menu_items = [(name, description) for name, description in apis]
            
            choice = self.ui.display_menu(f"{module_name} - 可用API", menu_items)
            
            if choice == 0:
                break
            
            self.execute_single_api(module_name, choice - 1)
            self.ui.wait_for_continue()
    
    def execute_single_api(self, module_name: str, api_index: int):
        """执行单个API"""
        apis = self.api_manager.list_apis_in_module(module_name)
        if api_index >= len(apis):
            print("无效的API选择")
            return
        
        api_name, api_desc = apis[api_index]
        
        # 收集参数
        param_collector = ParamCollectorFactory.get_collector(api_name)
        params = {}
        
        if param_collector.needs_input():
            params = param_collector.collect(api_name)
        
        # 执行API
        result = self.api_manager.execute_api(module_name, api_index, **params)
        
        # 显示结果
        self.ui.display_result(result)
    
    def test_all_apis(self):
        """测试所有API"""
        if not self.ui.confirm("确定要测试所有API吗？"):
            return
        
        self.ui.display_header("开始测试所有API")
        
        modules = self.api_manager.list_api_modules()
        
        for module_name in modules:
            print(f"\n测试模块: {module_name}")
            print("-" * 30)
            
            apis = self.api_manager.list_apis_in_module(module_name)
            for i, (api_name, api_desc) in enumerate(apis):
                print(f"  {i+1}. {api_name}...", end=" ")
                
                # 跳过需要用户输入的API
                param_collector = ParamCollectorFactory.get_collector(api_name)
                if param_collector.needs_input():
                    print("跳过（需要参数）")
                    continue
                
                result = self.api_manager.execute_api(module_name, i)
                if result["success"]:
                    print("成功")
                else:
                    print(f"失败: {result.get('message', '')}")
        
        print("\n所有API测试完成")
    
    def run(self):
        """运行应用程序"""
        try:
            self.setup_environment()
            
            while True:
                choice = self.display_main_menu()
                
                if choice == 0:
                    print("\n再见!")
                    break
                
                self.handle_module_selection(choice)
                
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
        except Exception as e:
            print(f"\n程序出错: {e}")
            logging.exception("程序出错")

if __name__ == "__main__":
    app = MainApp()
    app.run()