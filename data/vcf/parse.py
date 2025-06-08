import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_html_tables(url, table_index=0, headers=None):
    """
    解析网页中的表格并返回DataFrame
    
    参数:
        url (str): 目标网页URL
        table_index (int): 要解析的表格索引(默认为0，即第一个表格)
        headers (dict): 可选的请求头
        
    返回:
        pandas.DataFrame: 包含表格数据的DataFrame
    """
    try:
        # 发送HTTP请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有表格元素
        tables = soup.find_all('table')
        
        if not tables:
            print("网页中没有找到表格")
            return None
            
        if table_index >= len(tables):
            print(f"表格索引超出范围，网页中只有{len(tables)}个表格")
            return None
            
        table = tables[table_index]
        
        # 提取表头
        table_headers = []
        for th in table.find_all('th'):
            table_headers.append(th.text.strip())
        
        # 提取表格数据
        table_data = []
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all(['td', 'th']):
                row_data.append(cell.text.strip())
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
    # 示例URL（维基百科的国家列表）
    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
    
    # 可以添加自定义请求头（有些网站需要）
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 解析网页中的第一个表格
    df = parse_html_tables(url, table_index=0, headers=custom_headers)
    
    if df is not None:
        # 显示前5行数据
        print(df.head())
        
        # 保存到CSV文件（可选）
        df.to_csv('extracted_table.csv', index=False)
        print("表格已保存到 extracted_table.csv")
