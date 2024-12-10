import os
import shutil

def create_directory_structure():
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 删除现有的static和uploads目录（如果存在）
    for dir_name in ['static', 'uploads']:
        dir_path = os.path.join(current_dir, dir_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"Removed existing directory: {dir_path}")

    # 需要创建的目录结构
    directories = [
        'app/api/endpoints',
        'app/core',
        'app/db',
        'app/models',
        'app/utils',
        'static',
        'uploads/covers',
        'uploads/chapters'
    ]

    # 创建目录和__init__.py文件
    for directory in directories:
        dir_path = os.path.join(current_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")
        
        # 在Python包目录中创建__init__.py
        if 'app' in dir_path:
            init_file = os.path.join(dir_path, '__init__.py')
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('# This is a Python package\n')
            print(f"Created: {init_file}")

    return current_dir

def create_html_files(current_dir):
    # HTML文件内容
    html_files = {
        'static/login.html': '''<!DOCTYPE html>
<html lang="zh">
... login.html的完整内容 ...
</html>''',
        'static/comics.html': '''<!DOCTYPE html>
<html lang="zh">
... comics.html的完整内容 ...
</html>''',
        'static/chapters.html': '''<!DOCTYPE html>
<html lang="zh">
... chapters.html的完整内容 ...
</html>''',
        'static/reader.html': '''<!DOCTYPE html>
<html lang="zh">
... reader.html的完整内容 ...
</html>'''
    }

    # 创建HTML文件
    for file_path, content in html_files.items():
        full_path = os.path.join(current_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created file: {full_path}")

def verify_structure(current_dir):
    # 验证目录结构
    required_dirs = [
        'static',
        'uploads/covers',
        'uploads/chapters',
        'app/api/endpoints',
        'app/core',
        'app/db',
        'app/models',
        'app/utils'
    ]
    
    required_files = [
        'static/login.html',
        'static/comics.html',
        'static/chapters.html',
        'static/reader.html',
        'app/api/endpoints/__init__.py',
        'app/core/__init__.py',
        'app/db/__init__.py',
        'app/models/__init__.py',
        'app/utils/__init__.py'
    ]
    
    all_ok = True
    
    for dir_path in required_dirs:
        full_path = os.path.join(current_dir, dir_path)
        if not os.path.exists(full_path):
            print(f"ERROR: Directory not found: {dir_path}")
            all_ok = False
    
    for file_path in required_files:
        full_path = os.path.join(current_dir, file_path)
        if not os.path.exists(full_path):
            print(f"ERROR: File not found: {file_path}")
            all_ok = False
    
    return all_ok

def main():
    print("Starting project setup...")
    current_dir = create_directory_structure()
    create_html_files(current_dir)
    
    if verify_structure(current_dir):
        print("\nProject structure setup completed successfully!")
    else:
        print("\nProject structure setup completed with errors!")

if __name__ == "__main__":
    main() 