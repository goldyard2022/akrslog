import parse
import json
from datetime import datetime
import pandas as pd
import io
from akrs_log.parse.log_base import AKRS_LOG
import streamlit as st


def parse_log_file(file, log_format):
    log_data = []
    for line in file:
        line = line.decode("utf-8")  # 解码为字符串
        result = parse.parse(log_format, line)
        if result:
            log_entry = result.named
            log_entry["datetime"] = datetime.strptime(
                f"{log_entry['date']} {log_entry['time']}", "%Y-%m-%d %H:%M:%S.%f"
            )
            if "force" in log_entry:
                log_entry["force"] = float(log_entry["force"])
            if "height" in log_entry:
                log_entry["height"] = float(log_entry["height"])
            if "current_position" in log_entry:
                log_entry["current_position"] = float(log_entry["current_position"])
            if "displacement" in log_entry:
                log_entry["displacement"] = float(log_entry["displacement"])
            if "brightness" in log_entry:
                log_entry["brightness"] = int(log_entry["brightness"])
            if "residual" in log_entry:
                log_entry["residual"] = float(log_entry["residual"])
            if "angle" in log_entry:
                log_entry["angle"] = float(log_entry["angle"])
            if "json_data" in log_entry:
                try:
                    json_data = json.loads(log_entry["json_data"])
                    log_entry["json_data"] = json_data
                except json.JSONDecodeError:
                    log_entry["json_data"] = None
            del log_entry["date"]
            del log_entry["time"]
            log_data.append(log_entry)
    return pd.DataFrame(log_data)


def save_to_excel(data):
    output = io.BytesIO()
    df = pd.DataFrame(data)
    df.to_excel(output, index=False)
    return output.getvalue()


def bonding_log_analysis():
    st.title("玻璃片模拟贴片日志分析工具")

    log_type = st.selectbox("选择日志操作类型", options=list(AKRS_LOG.keys()))
    log_format = AKRS_LOG[log_type]

    uploaded_file = st.file_uploader("上传模拟贴片日志文件", type=["txt", "log"])

    if uploaded_file is not None:
        uploaded_file.seek(0)  # 重置文件指针
        parsed_logs = parse_log_file(uploaded_file, log_format)

        # 显示解析结果
        st.write("解析结果:")
        st.table(parsed_logs)

        # 保存到Excel
        excel_data = save_to_excel(parsed_logs)
        st.download_button(
            label="下载解析结果",
            data=excel_data,
            file_name="parsed_bonding_logs.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


# 调用函数显示页面内容
bonding_log_analysis()
