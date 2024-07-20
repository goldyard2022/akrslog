# 定义日志格式

AKRS_LOG = {
    "LOG_CURRENT_FORCE": (
        "{date} {time} +08:00 [INF] LeftBondModule - 当前力控值：{force}g, 高度：{height}"
    ),
    "PR_EXECUTION_RESULT": (
        "{date} {time} +08:00 [INF] {module} PR执行结果：{json_data}"
    ),
    "MOTION_INFO": (
        "{date} {time} +08:00 [INF] 轴[{axis}]相对运动，当前位置：[{current_position}]，位移量：[{displacement}]"
    ),
    "BOND_LIGHT": (
        "{date} {time} +08:00 [INF] 左Bond{light}光源-设置光源亮[{brightness}]"
    ),
    "ANGLE_CORRECTION": (
        "{date} {time} +08:00 [INF] LeftBondModule角度校正{status}，剩余残差：{residual}° 当前T轴角度：{angle}"
    )
}

