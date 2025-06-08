# import pandas as pd
# import mysql.connector

# # 读取 Excel 文件中的所有 sheets
# def read_excel(file_path):
#     sheets = pd.read_excel(file_path, sheet_name=None)
#     for sheet_name, df in sheets.items():
#         df.columns = [col.strip() for col in df.columns]
#     return sheets

# # 创建 MySQL 数据库连接
# def create_mysql_connection(host, user, password, database):
#     connection = mysql.connector.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=database
#     )
#     return connection

# #创建 MySQL 表（将所有列设置为 TEXT 类型，使用 ROW_FORMAT=COMPRESSED），并返回截断后的列名映射
# def create_table(connection, table_name, columns):
#     cursor = connection.cursor()
#     cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
    
#     # 定义列映射和数据类型
#     column_mapping = {col: col[:64] for col in columns}  # 截断列名
#     create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ("
    
#     for col, truncated_col in column_mapping.items():
#         create_table_query += f"`{truncated_col}` LONGTEXT,"
    
#     # 设置 DYNAMIC 行格式
#     create_table_query = create_table_query.rstrip(',') + ") ROW_FORMAT=DYNAMIC;"
    
#     cursor.execute(create_table_query)
#     connection.commit()
#     return column_mapping

# #插入 Excel 数据到 MySQL 表，使用原始列名和截断列名的映射
# def insert_data_to_mysql(connection, table_name, df, column_mapping):
#     cursor = connection.cursor()
#     df = df.rename(columns=column_mapping)  # 使用截断列名作为DataFrame的列名
#     df = df.where(pd.notnull(df), None)  # 将NaN转换为None

#     placeholders = ', '.join(['%s'] * len(df.columns))
#     columns = ', '.join([f"`{col}`" for col in df.columns])
#     insert_query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"

#     for _, row in df.iterrows():
#         cursor.execute(insert_query, tuple(row))
#     connection.commit()

# # 主函数
# def main():
#     excel_file = "./data/VOC_chicken_202411.xlsx"
#     mysql_config = {
#         "host": "localhost",
#         "user": "103_150_181_174",
#         "password": "MnF55fY2EhY6nQmY",
#         "database": "103_150_181_174"
#     }

#     sheets = read_excel(excel_file)
#     connection = create_mysql_connection(**mysql_config)

#     for sheet_name, df in sheets.items():
#         table_name = f"AIFdata_VOC_{sheet_name}"  # 每个sheet创建一个独立的表
#         column_mapping = create_table(connection, table_name, df.columns)
#         insert_data_to_mysql(connection, table_name, df, column_mapping)
#     connection.close()

# if __name__ == "__main__":
#     main()






import pandas as pd
import mysql.connector
from mysql.connector import Error  # 导入 Error 用于异常处理

# 读取 Excel 文件中的所有 sheets
def read_excel(file_path):
    sheets = pd.read_excel(file_path, sheet_name=None)
    for sheet_name, df in sheets.items():
        df.columns = [col.strip() for col in df.columns]  # 去除列名中的多余空格
    return sheets

# 创建 MySQL 数据库连接
def create_mysql_connection(host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return connection

# 创建表
def create_table(connection, table_name, columns):
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")  # 删除表，如果存在
    
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for col in columns:
        formatted_col = col.replace(' ', '_').replace('（', '(').replace('）', ')')  # 去除空格和特殊字符
        
        # 判断列名长度是否超过50个字符，如果超过则设置为 BLOB 类型，否则为 TEXT
        if len(formatted_col) > 50:
            create_table_query += f"`{formatted_col}` BLOB,"
        else:
            create_table_query += f"`{formatted_col}` TEXT,"
    
    create_table_query = create_table_query.rstrip(',') + ") ROW_FORMAT=DYNAMIC;"
    
    print(create_table_query)  # 打印生成的 SQL 语句，检查是否正确
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()


# 插入数据
def insert_data_to_mysql(connection, table_name, df):
    try:
        cursor = connection.cursor()
        
        placeholders = ', '.join(['%s'] * len(df.columns))
        columns = ', '.join([f"`{col.replace(' ', '_').replace('（', '(').replace('）', ')')}`" for col in df.columns])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        print(insert_query)  # 打印生成的 SQL 语句
        
        rows_to_insert = [
            [None if pd.isna(row[col]) else row[col] for col in df.columns]
            for _, row in df.iterrows()
        ]
        cursor.executemany(insert_query, rows_to_insert)
        connection.commit()
        
    except Error as e:
        print(f"Error while inserting data: {e}")
        
    finally:
        cursor.close()

# 主函数
def main():
    excel_file = "./data/副本VOC_chicken_202411.xlsx"
    mysql_config = {
        "host": "localhost",
        "user": "103_150_181_174",
        "password": "MnF55fY2EhY6nQmY",
        "database": "103_150_181_174"
    }

    sheets = read_excel(excel_file)
    connection = create_mysql_connection(**mysql_config)

    for sheet_name, df in sheets.items():
        table_name = f"AIFdata_VOC_{sheet_name}"  # 每个sheet创建一个独立的表
        create_table(connection, table_name, df.columns)  # 创建表
        insert_data_to_mysql(connection, table_name, df)  # 插入数据

    if connection.is_connected():
        connection.close()

if __name__ == "__main__":
    main()



