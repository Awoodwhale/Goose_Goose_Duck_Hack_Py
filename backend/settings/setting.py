class HackSettings:
    """修改的设置"""

    init_base_movement_speed: float = 5.0
    init_movement_speed: float = 5.0  # 初始速度
    init_fog_distance: float = 100.0  # 初始迷雾距离(目前似乎没用)
    hacked_fog_distance: float = 7.5    # hack之后的迷雾距离
    init_layer_mask: int = 131090  # 初始迷雾蒙版
    init_enable_xray: bool = False  # 初始是否能透视
    init_enable_wall: bool = False  # 初始是否能穿墙的状态
    init_enable_cd: bool = False    # 初始是否开启了无cd
    cur_movement_speed: float = 5.0  # 当前速度
