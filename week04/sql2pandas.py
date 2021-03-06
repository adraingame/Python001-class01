'''
作业背景：在数据处理的步骤中，可以使用 SQL 语句或者 pandas 加 Python 库、函数等方式进行数据的清洗和处理工作。

因此需要你能够掌握基本的 SQL 语句和 pandas 等价的语句，利用 Python 的函数高效地做聚合等操作。

作业要求：请将以下的 SQL 语句翻译成 pandas 语句：
'''
import pandas as pd
import numpy as np

	
# 1. SELECT * FROM data;
import pymysql

con = pymysql.connect('id', 'order_id', 'name', 'age')
df = pd.read_sql('selcect * from data', con)
 
# 2. SELECT * FROM data LIMIT 10;
df.head(10) 

# 3. SELECT id FROM data;  //id 是 data 表的特定一列
df['id']

# 4. SELECT COUNT(id) FROM data;
df['id'].value_counts()
 
# 5. SELECT * FROM data WHERE id<1000 AND age>30;
df(df['id']<1000) & (df['age']>30)]

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
con_table1 = pymysql.connect('id', 'order_id', 'name', 'age')
table1_data = pd.read_sql('selcect * from table1', con_table1)
dfs = table1_data.groupby('id').groups
for df in dfs:
    df[df['id'] & df['order_id'].unique()]

 
# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(df1, df2, on = 'id', how = 'inner')
 
# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([df1, df2], ignore_index = True).drop_duplicates()
 
# 9. DELETE FROM table1 WHERE id=10;
df.drop([df['id']=10], axis = 0)

# 10. ALTER TABLE table1 DROP COLUMN column_name;
df.drop(['column_name'], axis = 1)
