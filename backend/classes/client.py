from typing import List
from backend.classes.memory import Memory
from backend.settings.setting import HackSettings
from backend.classes.local_player import LocalPlayer
from backend.classes.player_controller import PlayerController
from backend.utils.utils import Singleton

@Singleton
class Client:  # TODO: 是否需要把dateupdater进行内嵌
    memory: Memory
    local_player: LocalPlayer
    player_controllers: List[PlayerController]
    players_num: int = 16  # 最多游玩的玩家数量

    def __init__(self, memory: Memory) -> None:
        self.memory = memory
        self.init_players()
    
    def init_players(self):
        # 本地玩家
        self.local_player = LocalPlayer(self.memory)
        # 默认16个游戏玩家
        self.player_controllers = [
            PlayerController(self.memory) for _ in range(self.players_num)
        ]

    def on_game_started(self):
        """游戏开始触发的函数"""
        self.update_game_original_data()

    def on_game_ended(self):
        """游戏结束触发的函数"""
        self.recovery_game_original_data()
        # TODO: 游戏结束还原配置

    def update_game_original_data(self):
        """更新游戏的原始数据"""
        HackSettings.init_base_movement_speed = (
            # read_only属性, 无法修改, 只能读取
            self.local_player.get_base_movement_speed()
        )
        # HackSettings.init_movement_speed = self.local_player.get_movement_speed()
        # HackSettings.init_fog_distance = self.local_player.get_fog_distance()
        # HackSettings.init_enable_wall = self.local_player.get_enable_wall()
        # HackSettings.init_enable_xray = self.local_player.get_enable_xray()
        # print("更新初始配置",
        #     [
        #         HackSettings.init_movement_speed,
        #         HackSettings.init_fog_distance,
        #         HackSettings.init_enable_wall,
        #         HackSettings.init_enable_xray,
        #     ]
        # )

    def recovery_game_original_data(self):
        from backend.classes.hack import Hack

        hack = Hack(self)  # 获取单例
        # * 还原游戏开始前的初始属性
        hack.speed_hack(HackSettings.init_movement_speed)
        hack.fog_hack(HackSettings.init_enable_xray)  # 关闭透视
        hack.wall_hack(HackSettings.init_enable_wall)   # 关闭穿墙
        print("恢复初始配置",
            [
                HackSettings.init_movement_speed,
                HackSettings.init_fog_distance,
                HackSettings.init_enable_wall,
                HackSettings.init_enable_xray,
            ]
        )
