import streamlit as st
import pandas as pd
import io
from datetime import datetime

# 过滤并解析日志文件，按小时统计包含关键词的日志条目
def parse_custom_log_file(file, keyword):
    log_data = {}
    for line in file:
        line = line.decode('utf-8')  # 解码为字符串
        if keyword in line:
            time_part = line.split(" [INF] ")[0].strip()
            log_time = datetime.strptime(time_part, "%Y-%m-%d %H:%M:%S.%f +08:00")
            hour_str = log_time.strftime("%Y-%m-%d %H:00")
            if hour_str not in log_data:
                log_data[hour_str] = 0
            log_data[hour_str] += 1
    return log_data

# 保存数据到Excel文件并返回文件内容
def save_to_excel(data, columns):
    output = io.BytesIO()
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(output, index=False)
    return output.getvalue()

def other_analysis_page():
    st.title("自定义分析工具")

    uploaded_file = st.file_uploader("上传另一组日志文件", type=["txt", "log"])
    
    if uploaded_file is not None:
        keyword = "当前力控值"
        
        uploaded_file.seek(0)  # 重置文件指针
        log_data = parse_custom_log_file(uploaded_file, keyword)
        
        # 转换为DataFrame并排序
        log_df = pd.DataFrame(list(log_data.items()), columns=["时间", "次数"]).sort_values(by="时间")
        
        # 显示统计信息
        st.write(f"日志中包含关键词 '{keyword}' 的每小时统计信息:")
        st.table(log_df)

        # 保存到Excel
        excel_data = save_to_excel(log_df, ["时间", "次数"])
        st.download_button(
            label="下载每小时统计信息",
            data=excel_data,
            file_name="hourly_log_statistics.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# 调用函数显示页面内容
other_analysis_page()