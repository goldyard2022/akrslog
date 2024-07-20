from parse import parse
from typing import *

# 定义日志模板
LOG_TEMPLATES = [
    (
        "MOVE_MAP_POSITION",
        "{date} {time} +08:00 [INF] LeftBondModule - 移动到Map指定位置[{row:d},{col:d}] [{x:d},{y:d}]完成",
    ),
    ("PR_RESULT", "{date} {time} +08:00 [INF] {module}定位 PR执行结果：{json_data}"),
    (
        "ANGLE_CORRECTION",
        "{date} {time} +08:00 [INF] LeftBondModule第{correction_num:d}次角度校正，DD旋转角度：{angle}°",
    ),
    (
        "PRECISION_ADJUSTMENT",
        "{date} {time} +08:00 [INF] LeftBondModule精度校正{status}，Die位置 row:{row:d} col:{col:d}",
    ),
    ("CORRECTION_START", "{date} {time} +08:00 [INF] {module}开始校正"),
    (
        "CORRECTION_END",
        "{date} {time} +08:00 [INF] 校正结束时间={end_time} 耗时={duration}ms",
    ),
    (
        "FORCE_CONTROL",
        "{date} {time} +08:00 [INF] LeftBondModule - 当前力控值：{force}g, 高度：{height}",
    ),
    (
        "AXIS_MOVEMENT_ABSOLUTE",
        "{date} {time} +08:00 [INF] 轴[{axis}]绝对运动，开始位置：[{start_pos}],目标位置:[{end_pos}]",
    ),
]


# 定义一个函数来检查日志条目是否匹配任意模板
def check_log_match(
    log_entry: Any, templates: Any
) -> tuple[Any, dict | Any] | tuple[None, None]:
    for name, template in templates:
        result = parse(template, log_entry)
        if result:
            return name, result.named
    return None, None


# 示例日志条目
log_entries = [
    "2024-07-16 00:57:28.083 +08:00 [INF] LeftBondModule - 移动到Map指定位置[5,6] [323219,64056]完成",
    "2024-07-16 00:57:28.095 +08:00 [INF] 轴[BAZL]绝对运动，开始位置：[850.018827285819],目标位置:[-2660.0026]",
]

# 检查每个日志条目是否匹配任意模板
for entry in log_entries:
    name, data = check_log_match(entry, LOG_TEMPLATES)
    if name is not None:
        print(f"Matched template: {name}")
        print(f"Extracted data: {data}")
    else:
        print("No match found")
