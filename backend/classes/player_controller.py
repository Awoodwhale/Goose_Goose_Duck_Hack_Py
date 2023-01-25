from json import dumps
from typing import List
from backend.classes.memory import Memory
from backend.data.offsets import Offsets
from backend.utils.log import log
from backend.utils.utils import get_role_name


class PlayerController:
    """玩家控制器"""

    memory: Memory
    address: int = 0

    b_isSilenced: bool = False  # 是否被静音
    b_isInfected: bool = False  # 是否被感染
    b_isPlayerRoleSet: bool = False  # 是否被赋予了游戏角色,可以用来判断游戏是否开始
    b_inVent: bool = False  # 是否钻管道
    b_hasBomb: bool = False  # 是否携带炸弹
    b_isGhost: bool = False  # 是否是幽灵
    b_isLocal: bool = False  # 是否是本地
    b_isSpectator: bool = False  # 是否是观战
    b_isRemoteSpectating: bool = False  # 远程观战?
    b_hasKilledThisRound: bool = False  # 本轮是否杀过人
    i_playerRoleId: int = 0  # 角色id
    invisibilityDistance: int = 0  # 可见距离?好像没用?
    i_timeOfDeath: int = 0  # 死亡时间

    nickname: str = ""  # 游戏名称
    rolename: str = ""  # 角色名称

    v3_position: List[float] = [0.0, 0.0, 0.0]  # 当前玩家三维坐标x, y, z

    def __init__(self, memory: Memory) -> None:
        self.memory = memory

    def update_addr(self, addr: int) -> bool:
        """更新address

        :param addr: address
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
        """更新当前角色的信息"""
        if self.address == 0:
            return False
        try:
            if self.nickname == "":
                self.update_nickname()

            self.b_isPlayerRoleSet = self.memory.mem.read_bool(
                self.address + Offsets.PlayerController.b_isPlayerRoleSet
            )  # 是否已经设置了角色

            self.b_isLocal = self.memory.mem.read_bool(
                self.address + Offsets.PlayerController.b_isLocal
            )  # 是否是本地角色

            if self.b_isPlayerRoleSet:
                self.update_position()
                self.b_inVent = self.memory.mem.read_bool(
                    self.address + Offsets.PlayerController.b_inVent
                )
                self.b_hasBomb = self.memory.mem.read_bool(
                    self.address + Offsets.PlayerController.b_hasBomb
                )
                self.b_isGhost = self.memory.mem.read_bool(
                    self.address + Offsets.PlayerController.b_isGhost
                )
                self.b_isSpectator = self.memory.mem.read_bool(
                    self.address + Offsets.PlayerController.b_isSpectator
                )
                self.invisibilityDistance = self.memory.mem.read_int(
                    self.address + Offsets.PlayerController.fl_invisibilityDistance
                )
                self.b_isRemoteSpectating = self.memory.mem.read_bool(
                    self.address + Offsets.PlayerController.b_isRemoteSpectating
                )
                self.b_hasKilledThisRound = self.memory.mem.read_bool(
                    self.address + Offsets.PlayerController.b_hasKilledThisRound
                )  # 本轮是否杀过人

                self.i_timeOfDeath = self.memory.mem.read_int(
                    self.address + Offsets.PlayerController.i_timeOfDeath
                )  # 死亡时间
                i_playerRoleId_addr = self.memory.mem.read_ulonglong(
                    self.address + Offsets.PlayerController.ptr_playerRole
                )
                self.i_playerRoleId = self.memory.mem.read_int(
                    i_playerRoleId_addr + 0x10
                )   # 角色id
                self.rolename = get_role_name(self.i_playerRoleId)  # 角色名称

            return True
        except Exception as e:
            log(f"Failed to update player_controller info. {e}", "error")
            return False

    def update_nickname(self) -> bool:
        """更新当前角色的名称

        :return: 是否更新成功
        :rtype: bool
        """
        if self.address == 0:
            return False
        try:
            nickname = self.memory.mem.read_longlong(
                self.address + Offsets.PlayerController.ptr_nickname
            )
            first_char = nickname + 0x14
            length = self.memory.mem.read_int(nickname + 0x10)
            if length <= 0:
                return False
            # 读取玩家名称
            self.nickname = "".join(
                [
                    chr(self.memory.mem.read_ushort(first_char + i * 2))
                    for i in range(length)
                ]
            )
            return True
        except Exception as e:
            log(f"Failed to update nickname. {e}", "error")
            return False

    def update_position(self) -> bool:
        """更新当前角色的位置

        :return: 是否更新成功
        :rtype: bool
        """
        if self.address == 0:
            return False
        try:
            self.v3_position[0] = self.memory.mem.read_float(
                self.address + Offsets.PlayerController.v3_position
            )
            self.v3_position[1] = self.memory.mem.read_float(
                self.address + Offsets.PlayerController.v3_position + 4
            )
            self.v3_position[2] = self.memory.mem.read_float(
                self.address + Offsets.PlayerController.v3_position + 8
            )
            return True
        except Exception as e:
            log(f"Failed to update position. {e}", "error")
            return False

    def reset(self) -> None:
        """重制"""
        self.address = 0
        self.reset_fields()

    def reset_fields(self) -> None:
        """重制fields属性"""
        self.b_isSilenced: bool = False
        self.b_isInfected: bool = False
        self.b_isPlayerRoleSet: bool = False
        self.b_inVent: bool = False
        self.b_hasBomb: bool = False
        self.b_isGhost: bool = False
        self.b_isLocal: bool = False
        self.b_isSpectator: bool = False
        self.b_isRemoteSpectating: bool = False
        # 本轮是否杀过人
        self.b_hasKilledThisRound: bool = False

        self.i_playerRoleId: int = 0
        self.invisibilityDistance: int = 0
        self.i_timeOfDeath: int = 0

        self.nickname: str = ""
        self.rolename: str = ""

        self.v3_position: List[float] = [0.0, 0.0, 0.0]

    def tp2_xy(self, v2_pos: List[float]) -> bool:
        """传送到一个二维坐标

        :param v2_pos: 坐标
        :type v2_pos: List[float]
        :return: 是否传送成功
        :rtype: bool
        """
        if self.address == 0:
            return

        if not self.b_isLocal:
            return

        offsets = [
            Offsets.PlayerController.ptr_Rigidbody2D,
            Offsets.Rigidbody2D.ptr_UnknownClass0,
            Offsets.Rigidbody2D.UnknownClass0.ptr_UnknownFields,
            Offsets.Rigidbody2D.UnknownClass0.UnknownFields.v2_position,
        ]
        position = self.memory.find_pointer(self.address, offsets)
        if not position:
            return False

        try:
            self.memory.mem.write_float(position, float(v2_pos[0]))
            self.memory.mem.write_float(position + 4, float(v2_pos[1]))
        except:
            return False

        return True

    def __str__(self):
        dic = {k: v for k, v in self.__dict__.items()}
        if "memory" in dic.keys():
            dic.pop("memory")
        return dumps(dic, ensure_ascii=False)
