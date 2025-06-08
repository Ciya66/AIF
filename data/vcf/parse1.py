import os,sys
from bs4 import BeautifulSoup
import pandas as pd

def parse_tables_from_local_html(file_path, table_index=0, encoding='utf-8'):
    """
    解析本地HTML文件中的表格
    
    参数:
        file_path (str): 本地HTML文件路径
        table_index (int): 要解析的表格索引(默认为0，即第一个表格)
        encoding (str): 文件编码格式(默认为utf-8)
        
    返回:
        pandas.DataFrame: 包含表格数据的DataFrame
        或
        list: 如果return_all=True，返回所有表格的DataFrame列表
    """
    try:
        # 读取本地HTML文件
        with open(file_path, 'r', encoding=encoding) as file:
            html_content = file.read()
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找所有表格元素
        tables = soup.find_all('table')
        
        if not tables:
            print("HTML文件中没有找到表格")
            return None
            
        if table_index >= len(tables):
            print(f"表格索引超出范围，文件中只有{len(tables)}个表格")
            return None
            
        table = tables[table_index]
        
        # 提取表头
        table_headers = []
        for th in table.find_all('th'):
            table_headers.append(th.get_text(strip=True))
        
        # 提取表格数据
        table_data = []
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all(['td', 'th']):
                row_data.append(cell.get_text(' ', strip=True))  # 使用空格连接多行文本
            if row_data:  # 忽略空行
                table_data.append(row_data)
        
        # 如果没有表头，使用第一行作为表头
        if not table_headers and table_data:
            table_headers = table_data[0]
            table_data = table_data[1:]
        
        # 转换为DataFrame
        df = pd.DataFrame(table_data, columns=table_headers)
        
        return df
        
    except Exception as e:
        print(f"解析表格时出错: {e}")
        return None

# 示例用法
if __name__ == "__main__":
    # 替换为你的本地HTML文件路径
    html_file = sys.argv[1]
    
    # 解析HTML文件中的第一个表格
    df = parse_tables_from_local_html(html_file, table_index=0)
    
    if df is not None:
        # 显示前5行数据
        print("\n解析到的表格数据(前5行):")
        print(df.head())
        
        # 保存到CSV文件（可选）
        output_file = f'{sys.argv[2]}.csv'
        df.to_csv(output_file, index=False)
        print(f"\n表格已保存到 {output_file}")
