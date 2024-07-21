from parse import parse
import json
from datetime import datetime
import pandas as pd
import io
import os
from akrs_log.parse.log_base import LOG_TEMPLATES
import streamlit as st
import re


# 解析日志条目
def parse_log_entry(entry):
    for template_name, template in LOG_TEMPLATES:
        result = parse(template, entry)
        if result:
            parsed_result = result.named
            parsed_result["template_name"] = template_name
            return parsed_result
    return None


# 解析日志段
def parse_log_segment(log_segment):
    parsed_entries = []
    for entry in log_segment:
        parsed_entry = parse_log_entry(entry["content"])
        if parsed_entry:
            parsed_entries.append(parsed_entry)
    return parsed_entries


def load_log_file(uploaded_file):
    log_entries = []
    for line_num, line in enumerate(uploaded_file, start=1):
        # 解码每行日志内容
        decoded_line = line.decode("utf-8").strip()
        log_entries.append({"line_num": line_num, "content": decoded_line})
    return log_entries


def extract_log_segments(log_entries):
    start_pattern = re.compile(r"精度校正:Bottom开始校正")
    middle_pattern = re.compile(r"去工作台校正开始时间")
    end_pattern = re.compile(r"校正结束时间")

    segments = []
    i = 0
    while i < len(log_entries):
        if middle_pattern.search(log_entries[i]["content"]):
            middle_index = i

            # 向上查找开始标记，最多查找50行
            start_index = -1
            upper_limit = max(middle_index - 50, 0)
            for j in range(middle_index, upper_limit - 1, -1):
                if start_pattern.search(log_entries[j]["content"]):
                    start_index = j
                    break

            # 如果找不到行列信息， 就向上取两行， 然后使用None作为位置信息了
            if start_index == -1:
                if middle_index > 1:
                    start_index = middle_index - 1
                else:
                    i += 1
                    continue

            # 向下查找结束标记
            end_index = -1
            for k in range(middle_index, len(log_entries)):
                if end_pattern.search(log_entries[k]["content"]):
                    end_index = k
                    break

            if end_index == -1:
                i += 1
                continue

            # 提取日志段
            log_segment = log_entries[start_index : end_index + 1]
            segments.append(log_segment)

            # 更新索引
            i = end_index + 1
        else:
            i += 1

    return segments


def save_log_segment(log_segment, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = generate_file_name(log_segment, output_dir)
    with open(file_path, "w", encoding="utf-8") as f:
        for entry in log_segment:
            f.write(entry["content"] + "\n")
    return file_path

last_map_position = "Unknown"

def generate_file_name(log_segment, output_dir):
    global last_map_position  # 声明使用全局变量

    timestamp_str = (
        log_segment[0]["content"].split()[0]
        + " "
        + log_segment[0]["content"].split()[1]
    )
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    match = re.search(r"Die位置 row:(\d+) col:(\d+)", log_segment[0]["content"])
    if match:
        map_position = match.group(1) + "_" + match.group(2)
        last_map_position = map_position + "_guess"  # 更新全局变量
    else:
        map_position = last_map_position

    file_name = (
        f"simulate_log_segment_{timestamp.strftime('%Y%m%d_%H%M%S')}_{map_position}.txt"
    )
    return os.path.join(output_dir, file_name)


def save_to_excel(data):
    output = io.BytesIO()
    df = pd.DataFrame(data)
    df.to_excel(output, index=False)
    return output.getvalue()


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


def parse_log(uploaded_file):
    parsed_logs = parse_log_file(uploaded_file)

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


def display_log(log_entries):
    # 显示日志内容
    if log_entries:
        st.write("日志文件内容:")
        log_content = "\n".join(
            [
                f"行号: {entry['line_num']}, 内容: {entry['content']}"
                for entry in log_entries
            ]
        )
        st.text_area("日志内容", log_content, height=400)


def parse_log_entries(log_entries):
    pass
