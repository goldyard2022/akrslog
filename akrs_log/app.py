import streamlit as st
import json
import numpy as np
import pandas as pd
from math import sqrt
import io

# 计算两点之间的欧几里得距离
def calculate_distance(p1, p2):
    return sqrt((p1["X"] - p2["X"])**2 + (p1["Y"] - p2["Y"])**2)

# 计算指定点对之间的距离
def calculate_custom_distances(log_data):
    distances = [[] for _ in range(20)]  # 20组距离
    point_pairs = [
        (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),   # 第一排和第二排
        (5, 10), (6, 11), (7, 12), (8, 13), (9, 14),  # 第二排和第三排
        (10, 15), (11, 16), (12, 17), (13, 18), (14, 19),  # 第三排和第四排
        (15, 20), (16, 21), (17, 22), (18, 23), (19, 24)  # 第四排和第五排
    ]
    for entry in log_data:
        points = entry["匹配点"]
        if len(points) == 25:
            for i, (p1_idx, p2_idx) in enumerate(point_pairs):
                distances[i].append(calculate_distance(points[p1_idx], points[p2_idx]))
    return distances

# 计算三西格玛值
def calculate_three_sigma(values):
    mean = np.mean(values)
    std_dev = np.std(values)
    return 3 * std_dev

# 过滤并解析日志文件
def parse_log_file(file, keyword):
    log_data = []
    for line in file:
        line = line.decode('utf-8')  # 解码为字符串
        if keyword in line:
            json_str = line.split('PR执行结果：')[-1].strip()
            log_entry = json.loads(json_str)
            if len(log_entry["匹配点"]) == 25:
                log_data.append(log_entry)
    return log_data

# 保存数据到Excel文件并返回文件内容
def save_to_excel(data):
    output = io.BytesIO()
    df = pd.DataFrame(data)
    df.to_excel(output, index=False)
    return output.getvalue()

# Streamlit应用主函数
def main():
    st.title("日志分析工具")

    uploaded_file = st.file_uploader("上传日志文件", type=["txt", "log"])
    
    if uploaded_file is not None:
        keywords = [
            "左侧右下视标定片阵列Mark定位 PR执行结果",
            "左侧左下视标定片阵列Mark定位 PR执行结果"
        ]
        
        for keyword in keywords:
            st.header(f"{keyword} 的统计结果")
            
            uploaded_file.seek(0)  # 重置文件指针
            log_data = parse_log_file(uploaded_file, keyword)
            distances = calculate_custom_distances(log_data)
            
            # 构建横向数据表
            three_sigma_values = [calculate_three_sigma(group_distances) for group_distances in distances]
            
            df_sigma = pd.DataFrame([three_sigma_values], columns=[f"{i+1}" for i in range(20)])
            
            st.table(df_sigma)

            # 保存原始点坐标数据，每行对应日志中的一行
            original_points = []
            for entry in log_data:
                row = {}
                for i, point in enumerate(entry["匹配点"]):
                    row[f"X{i+1}"] = point["X"]
                    row[f"Y{i+1}"] = point["Y"]
                original_points.append(row)

            excel_data = save_to_excel(original_points)
            st.download_button(
                label="下载原始点坐标数据",
                data=excel_data,
                file_name=f"{keyword}_points.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            

if __name__ == "__main__":
    main()