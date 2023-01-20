from typing import List
from pymem.process import process_from_id
from backend.classes.hack import Hack
from backend.classes.memory import Memory
from backend.classes.client import Client
from backend.classes.data_updater import DataUpdater
from backend.utils.utils import Singleton

@Singleton
class Api:
    ready: bool = False

    def __init__(self) -> None:
        self.ready = self.init_memory()  # api准备就绪

    def init_memory(self) -> bool:
        """初始化memory

        :return: 是否初始化成功
        :rtype: bool
        """
        memory = Memory()  # 初始化游戏内存
        if memory.init():
            self.memory = memory
            self.client = Client(self.memory)
            self.hack = Hack(self.client)
            self.data_updater = DataUpdater(self.client)
            self.ready = True
            return True
        return False

    def is_game_process_open(self) -> bool:
        """判断游戏进程是否开启

        :return: 是否开启游戏进程
        :rtype: bool
        """
        if self.ready:
            if process_from_id(self.memory.pid):
                return True
            self.ready = False
            return False
        return self.init_memory()

    def is_game_start(self) -> bool:
        """判断局内游戏是否开始

        :return: 局内游戏是否开始
        :rtype: bool
        """
        if self.is_game_process_open():
            return self.client.local_player.player_controller.b_isPlayerRoleSet
        return False

    def update_players(self):
        """
        更新玩家信息
        前端开启一个线程, 不断地执行这个函数
        """
        if not self.is_game_process_open():
            raise   # 没开启游戏就产生异常
        self.data_updater.player_controller_updater()

    def hack_speed(self, target_speed: float) -> bool:
        """调用hack对象的函数去修改本地玩家的速度

        :param target_speed: 目标速度
        :type target_speed: float
        :return: 是否修改成功
        :rtype: bool
        """
        return self.hack.speed_hack(target_speed)

    def hack_wall(self, target_state: bool) -> bool:
        """调用hack对象的函数去修改本地玩家穿墙的能力

        :param target_state: 是否开启穿墙
        :type target_state: bool
        :return: 是否修改成功
        :rtype: bool
        """
        return self.hack.wall_hack(target_state)

    def hack_fog(self, target_state: bool) -> bool:
        """调用hack对象的函数去修改本地玩家超远视距, 移除迷雾

        :param target_state: 是否开启
        :type target_state: bool
        :return: 是否修改成功
        :rtype: bool
        """
        return self.hack.fog_hack(target_state)

    def hack_cooldown(self, target_state: bool) -> bool:
        """调用hack对象的函数将本地玩家的cd清零

        :param target_state: 是否开启无cd
        :type target_state: bool
        :return: 是否修改成功
        :rtype: bool
        """
        return self.hack.skill_cooldown_hack(target_state)

    def hack_position(self, v2_pos: List[float]) -> bool:
        """调用hack对象的函数将本地玩家传送到一个二维坐标

        :param v2_pos: 二维坐标
        :type v2_pos: List[float]
        :return: 是否修改成功
        :rtype: bool
        """
        return self.hack.tp_hack(v2_pos)

    def get_cur_speed(self) -> float:
        """获取当前本地用户的速度

        :return: 速度
        :rtype: float
        """
        return self.client.local_player.get_movement_speed()

    def get_cur_fog_distance(self) -> float:
        """获取当前本地用户的迷雾视距

        :return: 迷雾视距
        :rtype: float
        """
        return self.client.local_player.get_fog_distance()

    def get_cur_enable_xray(self) -> bool:
        """获取当前是否开启了透视

        :return: 是否开启了透视
        :rtype: bool
        """
        return self.client.local_player.get_enable_xray()

    def get_cur_enable_wall(self) -> bool:
        """获取当前是否开启了穿墙

        :return: 是否开启了穿墙
        :rtype: bool
        """
        return self.client.local_player.get_enable_wall()

    def get_cur_enable_cd(self) -> bool:
        """获取当前是否开启了无cd

        :return: 是否开启了无cd
        :rtype: bool
        """
        return self.client.local_player.get_enable_cd()

    def get_players_info(self) -> list:
        """返回16个玩家信息

        :return: 16个玩家信息
        :rtype: list
        """
        return [str(x) for x in self.client.player_controllers]
