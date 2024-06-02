import os

def generate_directory_structure(root_dir, prefix=''):
    structure = ''
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = '|' + '    ' * level
        sub_indent = '|' + '    ' * (level + 1)
        
        if level == 0:
            structure += f'{os.path.basename(root)}/\n'
        else:
            structure += f'{prefix}{indent}--{os.path.basename(root)}/\n'
        
        for f in files:
            structure += f'{prefix}{sub_indent}--{f}\n'
    return structure

# 设置根目录
root_directory = '/Users/xiaodi/Postgraduate/MDA/Maps/github_version/MDA_Project2024_AED_Optimization'

# 生成目录结构
directory_structure = generate_directory_structure(root_directory)

# 将目录结构写入文件
with open('deploy/directory_structure.txt', 'w') as f:
    f.write(directory_structure)
