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
]
