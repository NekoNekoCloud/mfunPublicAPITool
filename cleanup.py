# cleanup.py
import shutil
import os

# 清理data目录
data_dir = "data"
if os.path.exists(data_dir):
    shutil.rmtree(data_dir)
    print(f"已清理 {data_dir} 目录")

# 清理旧的token文件
token_files = ["mfuns_token.txt", "token.txt"]
for token_file in token_files:
    if os.path.exists(token_file):
        os.remove(token_file)
        print(f"已删除 {token_file}")

print("清理完成，现在可以重新运行程序")