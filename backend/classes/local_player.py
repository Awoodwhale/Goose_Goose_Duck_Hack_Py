from typing import Union
from backend.classes.memory import Memory
from backend.settings.setting import HackSettings
from backend.data.offsets import GameAssembly, Offsets
from backend.classes.player_controller import PlayerController
from backend.utils.log import log
from backend.utils.utils import Singleton

@Singleton  # 只有一个本地玩家
class LocalPlayer:
    """本地玩家"""

    memory: Memory
    address: int = 0
    player_controller: PlayerController

    def __init__(self, memory: Memory) -> None:
        self.memory = memory
        self.player_controller = PlayerController(self.memory)

    def update_addr(self, addr: int) -> bool:
        """更新地址

        :param addr: 地址
        :type addr: int
        :return: 是否更新成功
        :rtype: bool
        """
        if addr <= 0:
            return False

        if self.address != addr:
            self.reset()
            self.address = addr

        return self.update()

    def update(self) -> bool:
        """更新

        :return: 是否更新成功
        :rtype: bool
        """
        if self.address == 0:
            return False
        try:
            ptr = self.memory.mem.read_longlong(
                self.address + Offsets.LocalPlayer.ptr_playerController
            )
            return self.player_controller.update_addr(ptr)
        except Exception as e:
            log(f"Failed to read local_player's player_controller ptr. {e}", "error")
            return False

    def reset(self) -> None:
        """重制"""
        self.address = 0

    def get_movement_speed(self) -> float:
        """获取当前移动速度

        :return: 移动速度
        :rtype: float
        """
        if self.address == 0:
            return HackSettings.init_movement_speed

        offsets = [
            Offsets.LocalPlayer.ptr_Class,
            Offsets.LocalPlayer.Class.ptr_staticFields,
            Offsets.LocalPlayer.Class.StaticField.f_movementSpeed,
        ]
        try:  # 防止内存读取报错
            addr = self.memory.find_pointer(self.address, offsets)

            if not addr:
                return HackSettings.init_movement_speed

            res = self.memory.mem.read_float(addr)
            if res <= 0:
                return HackSettings.init_movement_speed

            return res
        except:
            return HackSettings.init_movement_speed

    def get_base_movement_speed(self) -> float:
        """获取当前基础移动速度

        :return: 基础移动速度
        :rtype: float
        """
        if self.address == 0:
            return HackSettings.init_base_movement_speed

        offsets = [
            Offsets.LocalPlayer.ptr_Class,
            Offsets.LocalPlayer.Class.ptr_staticFields,
            Offsets.LocalPlayer.Class.StaticField.f_baseMovementSpeed,
        ]

        try:  # 防止内存读取报错
            addr = self.memory.find_pointer(self.address, offsets)

            if not addr:
                return HackSettings.init_base_movement_speed

            res = self.memory.mem.read_float(addr)
            if res <= 0:
                return HackSettings.init_base_movement_speed

            return res
        except:
            return HackSettings.init_base_movement_speed

    def get_fog_distance(self) -> float:
        """获取当前战争迷雾距离

        :return: 迷雾距离
        :rtype: float
        """
        if self.address == 0:
            return HackSettings.init_fog_distance

        fog_of_war_handler_addr = (
            self.memory.find_pointer(
                self.memory.assembly_base_address, GameAssembly.localPlayer()
            )
            + Offsets.LocalPlayer.ptr_fogOfWarHandler
        )
        if fog_of_war_handler_addr == 0:
            return HackSettings.init_fog_distance

        try:  # 防止内存读取报错
            fog_of_war_handler = self.memory.mem.read_longlong(fog_of_war_handler_addr)
            if fog_of_war_handler == 0:
                return HackSettings.init_fog_distance
            if self.memory.mem.read_bool(
                fog_of_war_handler + Offsets.FogOfWarHandler.b_targetPlayerSet
            ):
                # 当前的清晰度
                res = self.memory.mem.read_float(
                    fog_of_war_handler + Offsets.FogOfWarHandler.f_baseViewDistance
                )
                return res
        except:
            return HackSettings.init_fog_distance

        return HackSettings.init_fog_distance

    def get_enable_xray(self) -> bool:
        if self.address == 0:
            return HackSettings.init_enable_xray
        
        try:
            return self.get_fog_distance() == HackSettings.hacked_fog_distance
        except:
            return HackSettings.init_enable_xray

    def get_enable_wall(self) -> bool:
        """判断当前是否可以穿墙

        :return: 是否可以穿墙
        :rtype: bool
        """
        if self.address == 0:
            return HackSettings.init_enable_wall

        offsets = [
            Offsets.PlayerController.ptr_bodyCollider,
            Offsets.CapsuleCollider2D.ptr_unknownClass0,
            Offsets.CapsuleCollider2D.UnknownClass0.b_enableCollider,
        ]

        b_enableCollider_addr = self.memory.find_pointer(
            self.player_controller.address, offsets
        )
        if b_enableCollider_addr == 0:
            return HackSettings.init_enable_wall

        try:
            return not self.memory.mem.read_bool(b_enableCollider_addr)
        except Exception as e:
            log(f"get_enable_wall error. {e}", "error")
            return HackSettings.init_enable_wall

    def get_enable_cd(self) -> bool:
        """判断当前是否开启了无cd

        :return: 是否开启了无cd
        :rtype: bool
        """
        if not self.player_controller.b_isLocal:
            return HackSettings.init_enable_cd

        memory = self.memory

        addr = (
            memory.assembly_base_address + GameAssembly.BytesPatch.CooldownTime.address
        )
        if addr == 0:
            log("get_enable_cd addr == 0")
            return False

        patch = GameAssembly.BytesPatch.CooldownTime.removeCooldownTime

        try:
            res = memory.mem.read_bytes(addr,1)
            if res == patch:
                return True
        except Exception as e:
            log(f"get_enable_cd error. {e}", "error")
            return False

        return False
