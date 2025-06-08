# import pandas as pd
# import mysql.connector

# # 读取 Excel 文件
# def read_excel(file_path):
#     # 使用 pandas 读取 Excel 文件
#     df = pd.read_excel(file_path)
#     df.columns = [col.strip() for col in df.columns]
#     return df

# # 创建 MySQL 数据库连接
# def create_mysql_connection(host, user, password, database):
#     connection = mysql.connector.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=database
#     )
#     return connection


# 创建 MySQL 表（根据 Excel 文件的列）
# def create_table(connection, table_name, columns):
#     cursor = connection.cursor()

#     # 假设所有列都是 VARCHAR(255)，根据实际情况可以调整
#     create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
#     for col in columns:
#         create_table_query += f"{col} VARCHAR(255),"
#     create_table_query = create_table_query.rstrip(',') + ");"
    
#     cursor.execute(create_table_query)
#     connection.commit()

# def create_table(connection, table_name, columns):
#     cursor = connection.cursor()

#     create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    
#     # 遍历所有列
#     for i, col in enumerate(columns):
#         # 如果列名是 'Species Properties'，增加字段长度
#         if 'Species Properties' in col:
#             create_table_query += f"`{col}` VARCHAR(10000)"
#         else:
#             create_table_query += f"`{col}` VARCHAR(255)"
        
#         # 确保不是最后一列才加逗号
#         if i < len(columns) - 1:
#             create_table_query += ", "
    
#     create_table_query += ");"  # 结束括号
    
#     print(create_table_query)  # 输出查询语句，帮助排查问题
#     cursor.execute(create_table_query)
#     connection.commit()


# # 插入 Excel 数据到 MySQL 表
# def insert_data_to_mysql(connection, table_name, df):
#     cursor = connection.cursor()

#     df = df.where(pd.notnull(df), None)
#     # 构建插入 SQL 语句
#     placeholders = ', '.join(['%s'] * len(df.columns))
#     columns = ', '.join([f"`{col}`" for col in df.columns])
#     insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

#     # 插入数据
#     for i, row in df.iterrows():
#         cursor.execute(insert_query, tuple(row))

#     connection.commit()


# # 主函数
# def main():
#     # Excel 文件路径
#     excel_file = "data.xlsx"

#     # MySQL 配置
#     mysql_config = {
#         "host": "localhost",
#         "user": "103_150_181_174",
#         "password": "MnF55fY2EhY6nQmY",
#         "database": "103_150_181_174"
#     }

#     # MySQL 表名
#     table_name = "AIFdata"

#     # 读取 Excel 文件
#     df = read_excel(excel_file)

#     # 创建数据库连接
#     connection = create_mysql_connection(**mysql_config)

#     # 创建表
#     create_table(connection, table_name, df.columns)

#     # 插入数据
#     insert_data_to_mysql(connection, table_name, df)

#     # 关闭连接
#     connection.close()

# if __name__ == "__main__":
#     main()





import pandas as pd
import mysql.connector
from mysql.connector import Error

# 读取 Excel 文件
def read_excel(file_path):
    df = pd.read_excel(file_path)
    df.columns = [col.strip() for col in df.columns]
    return df

# 创建 MySQL 数据库连接
def create_mysql_connection(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


# 创建表的函数
def create_table(connection, table_name, columns):
    cursor = connection.cursor()
    # 删除表，如果存在
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    
    # 创建表
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

    for col in columns:
        # 处理列名，去掉空格和特殊字符
        formatted_col = col.replace(' ', '_').replace('（', '(').replace('）', ')')
        
        # # 如果是 'Species_Properties' 列，将类型改为 TEXT
        # if formatted_col == 'Species_Properties':
        #     create_table_query += f"`{formatted_col}` TEXT,"
        # # 如果是 'Poultry_Species' 列，将类型改为 TEXT
        # elif formatted_col == 'Poultry_Species':
        #     create_table_query += f"`{formatted_col}` TEXT,"
        # # 如果是 'Data_sources' 列，将类型改为 TEXT
        # elif formatted_col == 'Data_sources':
        #     create_table_query += f"`{formatted_col}` TEXT,"
        # else:
        #     create_table_query += f"`{formatted_col}` VARCHAR(255),"
        create_table_query += f"`{formatted_col}` TEXT,"

    create_table_query = create_table_query.rstrip(',') + ");"
    
    print(create_table_query)  # 打印生成的 SQL 语句，检查是否正确
    cursor.execute(create_table_query)
    connection.commit()



# 插入数据
def insert_data_to_mysql(connection, table_name, df):
    try:
        cursor = connection.cursor()

        # 构建插入 SQL 语句，包括 'Species Properties' 列
        placeholders = ', '.join(['%s'] * len(df.columns))
        columns = ', '.join([f"`{col.replace(' ', '_').replace('（', '(').replace('）', ')')}`" for col in df.columns])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        print(insert_query)  # 打印生成的 SQL 语句

        # 插入数据
        rows_to_insert = [
            [None if pd.isna(row[col]) else row[col] for col in df.columns]
            for _, row in df.iterrows()
        ]
        cursor.executemany(insert_query, rows_to_insert)

        connection.commit()
    except Error as e:
        print(f"Error while inserting data: {e}")

# 主函数
def main():
    excel_file = "./data/鸡肉品质数据库.xlsx"
    mysql_config = {
        "host": "localhost",
        "user": "103_150_181_174",
        "password": "MnF55fY2EhY6nQmY",
        "database": "103_150_181_174"
    }

    table_name = "AIFdata"
    df = read_excel(excel_file)
    connection = create_mysql_connection(**mysql_config)

    if connection:
        create_table(connection, table_name, df.columns)
        insert_data_to_mysql(connection, table_name, df)
        connection.close()

if __name__ == "__main__":
    main()

