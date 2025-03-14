import pandas as pd

# Read the Excel file
df = pd.read_excel(r'C:\JYN\unique_files.xlsx')

# Define the list of keywords to filter out
keywords = ["图", "计划表", "技术方案", "标准", "报告", "合同", "协议", "规程", 
            "规范", "规则", "书", "手册", "说明", "指南",
             "上海数腾", "产品手册", "社保", "资格证", "原理", "技巧"]

# Filter out rows where 'file_name' contains any of the keywords
filtered_df = df[~df['file_name'].str.contains('|'.join(keywords), na=False)]

# Output the filtered dataframe to a new Excel file
filtered_df.to_excel(r'c:\JYN\filtered_files.xlsx', index=False)