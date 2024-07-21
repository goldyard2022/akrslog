import streamlit as st
from akrs_log.base.log_analysis2 import (
    load_log_file,
    extract_log_segments,
    save_log_segment,
    parse_log_segment,
)
from typing import Any, List, Tuple, Dict
import os
import pandas as pd
import base64


def generate_file_info_list(log_segments, output_dir):
    file_info_list = []

    for segment in log_segments:
        # 保存日志段到文件
        file_path = save_log_segment(segment, output_dir)

        # 获取文件大小
        file_size_kb = os.path.getsize(file_path) / 1024

        file_info_list.append(
            {
                "文件名": os.path.basename(file_path),
                "文件大小": f"{file_size_kb:.2f} KB",
                "下载链接": generate_download_link(file_path),
                "file_path": file_path
            }
        )

    return file_info_list


def generate_download_link(file_path: str) -> str:
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        b64 = base64.b64encode(file_bytes).decode()
        return f'<a href="data:text/plain;base64,{b64}" download="{os.path.basename(file_path)}">下载</a>'

# 格式化文件大小
def format_file_size(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def bonding_log_analysis():
    st.title("玻璃片模拟贴片校正对位日志切割工具")

    uploaded_file = st.file_uploader("上传模拟贴片日志文件", type=["txt", "log"])

    output_dir = st.text_input("输出目录", value="output_logs")

    if uploaded_file is not None and output_dir:
        uploaded_file.seek(0)  # 重置文件指针
        log_entries = load_log_file(uploaded_file)

        log_segments = extract_log_segments(log_entries)

        if not log_segments:
            st.error("未找到符合条件的日志段")
        else:
            file_info_list = generate_file_info_list(log_segments, output_dir)

            # 创建一个DataFrame来存储文件信息，并删除file_path列
            file_info_df = pd.DataFrame(file_info_list).drop(columns=["file_path"])

            # 显示文件信息表格
            st.write("生成的日志文件信息:")
            st.write(
                file_info_df.to_html(escape=False, index=False), unsafe_allow_html=True
            )


# 调用函数显示页面内容
bonding_log_analysis()
