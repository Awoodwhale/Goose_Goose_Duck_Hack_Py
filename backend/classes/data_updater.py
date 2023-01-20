from typing import List
from backend.utils.log import log
from backend.classes.client import Client
from backend.data.offsets import GameAssembly, Offsets
from backend.classes.local_player import LocalPlayer
from backend.classes.player_controller import PlayerController
from backend.utils.utils import Singleton

@Singleton
class DataUpdater:
    client: Client  # client
    valid_players_num: int = 0  # 有效玩家数量
    b_isPlayerRoleSet: bool = False  # 是否开始游戏

    def __init__(self, client: Client) -> None:
        self.client = client
        self.memory = client.memory

    def player_controller_updater(self):
        if self.update_localPlayer(self.client.local_player):
            # 本地玩家有了再去更新16个玩家
            self.update_player_controllers(
                self.client.player_controllers, self.client.players_num
            )

    def update_localPlayer(self, local_player: LocalPlayer) -> None:
        offsets = GameAssembly.localPlayer()
        local_player_addr = self.memory.find_pointer(
            self.memory.assembly_base_address, offsets
        )

        if local_player_addr == 0:
            # log(f"读取不到local_player的信息 --> {local_player_addr}")
            return False

        local_player.update_addr(local_player_addr)  # 设置本地玩家的指针
        local_player_controller_addr = self.memory.mem.read_longlong(
            local_player_addr + Offsets.LocalPlayer.ptr_playerController
        )

        res = self.update_player_controller_addr(
            local_player.player_controller, local_player_controller_addr
        )

        if not res:
            return False

        # log(f"local_player info:\n{local_player.player_controller}")
        if local_player.player_controller.b_isPlayerRoleSet:
            # log("游戏已经开始了")
            if not self.b_isPlayerRoleSet:
                self.client.on_game_started()
                self.b_isPlayerRoleSet = True
        else:
            # log("游戏还没开始")
            if self.b_isPlayerRoleSet:
                self.client.on_game_ended()
                self.b_isPlayerRoleSet = False

        return True

    def update_player_controller_addr(
        self, player_controller: PlayerController, addr: int
    ) -> bool:
        if addr <= 0:
            return False
        return player_controller.update_addr(addr)

    def update_player_controllers(
        self, player_controllers: List[PlayerController], player_num: int
    ) -> None:
        valid_players_num = 0
        for i in range(player_num):
            cur_player_controler_addr = self.memory.find_pointer(
                self.memory.assembly_base_address,
                GameAssembly.playerControllerByIndex(i),
            )
            if cur_player_controler_addr == 0:
                # if i < 5:
                #     log(f"读取不到玩家[{i}]的信息 --> {cur_player_controler_addr}")
                continue

            if self.update_player_controller_addr(
                player_controllers[i], cur_player_controler_addr
            ):
                valid_players_num += 1
                # log(f"玩家[{i}] info:\n{player_controllers[i]}")
        self.valid_players_num = valid_players_num
