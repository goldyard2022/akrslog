import streamlit as st
from akrs_log.base.log_analysis import (
    load_log_file,
    extract_log_segments,
    save_log_segment,
    parse_log_segment,
)


def bonding_log_analysis():
    st.title("正式片贴片日志切割工具")

    uploaded_file = st.file_uploader("上传模拟贴片日志文件", type=["txt", "log"])

    output_dir = st.text_input("输出目录", value="output_logs")

    if uploaded_file is not None and output_dir:
        uploaded_file.seek(0)  # 重置文件指针
        log_entries = load_log_file(uploaded_file)

        log_segments = extract_log_segments(log_entries)

        if not log_segments:
            st.error("未找到符合条件的日志段")
        else:
            for segment in log_segments:
                # 显示日志段内容
                log_content = "\n".join([entry["content"] for entry in segment])
                st.text_area(
                    f"提取的日志内容 (行号: {segment[0]['line_num']} 到 {segment[-1]['line_num']})",
                    log_content,
                    height=200,
                )

                # 保存日志段到文件
                file_path = save_log_segment(segment, output_dir)
                st.success(f"日志段已保存到文件：{file_path}")

                # 解析日志块内容
                # parsed_entries = parse_log_segment(segment)
                # st.json(parsed_entries)


# 调用函数显示页面内容
bonding_log_analysis()
