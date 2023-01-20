from typing import List
from backend.settings.setting import HackSettings
from backend.utils.log import log
from backend.classes.client import Client
from backend.data.offsets import GameAssembly, Offsets
from backend.utils.utils import Singleton


@Singleton
class Hack:
    """修改功能"""

    client: Client

    def __init__(self, client: Client) -> None:
        self.client = client

    def speed_hack(self, target_speed: float = 5.0) -> bool:
        """修改local_player的移动速度

        :param target_speed: 目标速度
        :type target_speed: float
        """
        if type(target_speed) is not float:
            target_speed = float(target_speed)
        local_player = self.client.local_player
        if not (
            local_player
            and local_player.player_controller
            and local_player.player_controller.b_isLocal
        ):
            log(f"Failed to hack speed. You are not local player!", "error")
            return False

        if target_speed <= 0:
            log(f"Failed to hack speed. Target speed can't samll than 0!", "error")
            return False

        memory = self.client.memory
        offsets = [
            Offsets.LocalPlayer.ptr_Class,
            Offsets.LocalPlayer.Class.ptr_staticFields,
            Offsets.LocalPlayer.Class.StaticField.f_movementSpeed,
        ]

        base_movement_speed_addr = memory.find_pointer(local_player.address, offsets)
        if base_movement_speed_addr == 0:
            log(f"Failed to find [speed] pointer!", "error")
            return False

        try:
            cur_speed = memory.mem.read_float(base_movement_speed_addr)
            if cur_speed == target_speed:
                log(f"Same as before speed: {cur_speed}")
                return True
            # 速度不一样再去写内存
            memory.mem.write_float(base_movement_speed_addr, target_speed)
        except Exception as e:
            log(f"Failed to hack speed. {e}", "error")
            return False

        return True

    def wall_hack(self, target_state: bool = True) -> bool:
        """修改本地玩家能否穿墙

        :param target_state: 是否能穿墙的状态, defaults to True
        :type target_state: bool, optional
        """
        local_player = self.client.local_player
        if not (
            local_player
            and local_player.player_controller
            and local_player.player_controller.b_isLocal
        ):
            log(f"Failed to hack wall. You are not local player!", "error")
            return False

        memory = self.client.memory
        offsets = [
            Offsets.PlayerController.ptr_bodyCollider,
            Offsets.CapsuleCollider2D.ptr_unknownClass0,
            Offsets.CapsuleCollider2D.UnknownClass0.b_enableCollider,
        ]

        b_enableCollider_addr = memory.find_pointer(
            local_player.player_controller.address, offsets
        )
        if b_enableCollider_addr == 0:
            log(f"Failed to find [wall] pointer!", "error")
            return False

        try:
            cur_state = memory.mem.read_bool(b_enableCollider_addr)
            if cur_state == (not target_state):
                log(f"Same as before wall state: {target_state}")
                return True
            # 状态不一样再去更新内存
            memory.mem.write_bool(b_enableCollider_addr, not target_state)
        except Exception as e:
            log(f"Fail to hack wall. {e}", "error")
            return False

        return True

    def fog_hack(self, target_state: bool = True) -> bool:
        """移除战争迷雾

        :param target_state: 是否移除
        :type target_state: bool
        :return: 是否移除成功
        :rtype: bool
        """
        local_player = self.client.local_player
        if not (
            local_player
            and local_player.player_controller
            and local_player.player_controller.b_isLocal
        ):
            log(f"Failed to hack fog. You are not local player!", "error")
            return False
        try:
            memory = self.client.memory
            fog_of_war_handler_addr = (
                memory.find_pointer(
                    memory.assembly_base_address, GameAssembly.localPlayer()
                )
                + Offsets.LocalPlayer.ptr_fogOfWarHandler
            )
            if fog_of_war_handler_addr == 0:
                log(f"Failed to hack fog. fog_of_war_handler_addr is 0!", "error")
                return False
            fog_of_war_handler = memory.mem.read_longlong(fog_of_war_handler_addr)
            if fog_of_war_handler == 0:
                log(f"Failed to hack fog. fog_of_war_handler is 0!", "error")
                return False
            if memory.mem.read_bool(
                fog_of_war_handler + Offsets.FogOfWarHandler.b_targetPlayerSet
            ):  # 游戏已经开始
                try:
                    memory.mem.write_int(
                        fog_of_war_handler + Offsets.FogOfWarHandler.i_layerMask,
                        0 if target_state else HackSettings.init_layer_mask,
                    )
                    f_viewDistanceMultiplier = memory.mem.read_float(
                        fog_of_war_handler
                        + Offsets.FogOfWarHandler.f_viewDistanceMultiplier
                    )
                    # # 当前的清晰度
                    # cur = memory.mem.read_float(
                    #     fog_of_war_handler + Offsets.FogOfWarHandler.f_baseViewDistance
                    # )
                    # log(f"fog_of_war_handler: {cur}")
                    # log(f"target : {7.5 / f_viewDistanceMultiplier}")
                    if f_viewDistanceMultiplier != 0:
                        memory.mem.write_float(
                            fog_of_war_handler
                            + Offsets.FogOfWarHandler.f_baseViewDistance,
                            7.5 / f_viewDistanceMultiplier,
                        )
                        return True
                except Exception as e:
                    log(f"Failed to hack fog. {e}", "error")
                    return False
            log(f"Fail to hack fog. Game not start!", "error")
            return False
        except:
            return False

    def skill_cooldown_hack(self, target_state: bool = True) -> bool:
        """修改技能冷却时间(部分技能型鸭子的冷却存在问题, 星界也存在无法回神的问题)

        :param target_state: 是否开启无冷却, defaults to True
        :type target_state: bool, optional
        :return: 是否修改成功
        :rtype: bool
        """
        local_player = self.client.local_player
        if not (
            local_player
            and local_player.player_controller
            and local_player.player_controller.b_isLocal
        ):
            log(f"Failed to hack kill_cooldown. You are not local player!", "error")
            return False
        log(
            f"local_player.player_controller.b_isLocal {local_player.player_controller.b_isLocal}"
        )
        memory = self.client.memory

        addr = (
            memory.assembly_base_address + GameAssembly.BytesPatch.CooldownTime.address
        )
        if addr == 0:
            log(
                f"Failed to hack kill_cooldown. Can't find cooldown pointer base address!",
                "error",
            )
            return False

        patch = (
            GameAssembly.BytesPatch.CooldownTime.removeCooldownTime
            if target_state
            else GameAssembly.BytesPatch.CooldownTime.raw
        )

        try:
            for i in range(len(patch)):
                memory.mem.write_uchar(addr + i, patch[i])
            memory.mem.write_bytes(addr, patch, len(patch))
        except Exception as e:
            log(f"Failed to hack kill_cooldown. Patch error. {e}")
            return False
        log("hack success")
        return True

    def tp_hack(self, v2_pos: List[float]) -> bool:
        local_player = self.client.local_player
        if not (
            local_player
            and local_player.player_controller
            and local_player.player_controller.b_isLocal
        ):
            log(f"Failed to hack tp. You are not local player!", "error")
            return False

        return local_player.player_controller.tp2_xy(v2_pos)
