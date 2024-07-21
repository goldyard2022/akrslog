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


# 生成文件信息列表
def generate_file_info_list(
    log_segments: List[List[Dict[str, Any]]], output_dir: str
) -> List[Dict[str, Any]]:
    file_info_list = []
    for segment in log_segments:
        file_path = save_log_segment(segment, output_dir)
        file_info = {
            "file_name": os.path.basename(file_path),
            "file_size": format_file_size(os.path.getsize(file_path)),
            "file_path": file_path,
        }
        file_info_list.append(file_info)
    return file_info_list


# 生成下载链接
def generate_download_link(file_path: str) -> str:
    return f'<a href="{file_path}" download="{os.path.basename(file_path)}">下载</a>'


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

            # 添加下载链接
            for file_info in file_info_list:
                file_info["download_link"] = generate_download_link(
                    file_info["file_path"]
                )

            # 创建一个DataFrame来存储文件信息，并删除file_path列
            file_info_df = pd.DataFrame(file_info_list).drop(columns=["file_path"])

            # 显示文件信息表格
            st.write("生成的日志文件信息:")
            st.write(
                file_info_df.to_html(escape=False, index=False), unsafe_allow_html=True
            )


# 调用函数显示页面内容
bonding_log_analysis()
