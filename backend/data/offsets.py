class Offsets:
    class Rigidbody2D:
        class UnknownClass0:
            class UnknownFields:
                v2_position_readonly: int = 0x24
                v2_position: int = 0x2C

            ptr_UnknownFields: int = 0x78

        ptr_UnknownClass0: int = 0x10

    class PlayerController:
        class Class:
            class StaticField:
                playersList: int = 0x10
                playersListWithAgoraIDs: int = 0x20

            ptr_staticFields: int = 0xB8

        ptr_Class: int = 0x0
        ptr_Rigidbody2D: int = 0x58
        # Rigidbody2D
        ptr_bodyCollider: int = 0xA8
        # CapsuleCollider2D
        b_isSilenced: int = 0xC1
        # Boolean
        b_isInfected: int = 0xC3
        # Boolean
        killedBy: int = 0xC8
        # point64_ter, [instance+killedBy] +  0x14, length: [instance+killedBy] + 0x10
        fl_playerRoleId: int = 0xE8
        # point64_ter, [instance+playerRoleId] + 0x10, int64_t
        b_isPlayerRoleSet: int = 0xF0
        # Boolean
        b_inVent: int = 0xF1
        # Boolean
        b_facingRight: int = 0x130
        # Boolean, can make "Moon walk".
        b_hasBomb: int = 0x134
        # Boolean
        b_isGhost: int = 0x188
        # Boolean
        i_timeOfDeath: int = 0x18C
        # int
        b_isLocal: int = 0x1C0
        # Boolean
        fl_nickname: int = 0x1D0
        # point64_ter, [instance+nickname] +  0x14, length: [instance+nickname] + 0x10
        v3_position: int = 0x2C8
        # Value name is randomized. x, y. Float, Float
        f_idleTime: int = 0x2E4
        # float
        b_hasKilledThisRound: int = 0x2EC
        # Boolean
        fl_invisibilityDistance: int = 0x32C
        # int64_t, need this?
        b_fogOfWarEnabled: int = 0x379
        b_isSpectator: int = 0x37A
        # Boolean
        b_isRemoteSpectating: int = 0x37B
        # Boolean

    class LocalPlayer:
        class Class:
            class StaticField:
                ptr_localPlayer: int = 0x0
                f_movementSpeed: int = 0x10
                f_baseMovementSpeed: int = 0xC
                # Read only

            ptr_staticFields: int = 0xB8

        ptr_Class: int = 0x0
        staticField: int = 0x10
        ptr_playerController: int = 0x18
        # PlayerController of localplayer
        ptr_fogOfWarHandler: int = 0x20
        # FogOfWarHandler

    class FogOfWarHandler:
        i_layerMask: int = 0x18
        # Bit
        f_baseViewDistance: int = 0x2C
        f_viewDistanceMultiplier: int = 0x38
        b_targetPlayerSet: int = 0x50

    class CapsuleCollider2D:
        class UnknownClass0:
            b_enableCollider: int = 0x39

        ptr_unknownClass0: int = 0x30

    class UICooldownButton:
        f_cooldownTime = 0x70


# Const
GameAssembly_Method_UICooldownButton_Update = 0xF2D770
GameAssembly_Class_ptr_PlayerControllerClass = 0x3CA6AC0
GameAssembly_Class_ptr_LocalPlayerClass = 0x3C79808


class GameAssembly:
    class Method:
        class UICooldownButton:
            Update = GameAssembly_Method_UICooldownButton_Update

    class Class:
        ptr_PlayerControllerClass = GameAssembly_Class_ptr_PlayerControllerClass
        ptr_LocalPlayerClass = GameAssembly_Class_ptr_LocalPlayerClass

    class BytesPatch:
        class CooldownTime:
            # address = GameAssembly_Method_UICooldownButton_Update + 0xB7
            # raw = b"\x0F\x82"
            # removeCooldownTime = b"\xEB\x0E"
            # TODO: 验证上述patch代码
            address = GameAssembly_Method_UICooldownButton_Update + 0xA8
            raw = b"\x73"
            removeCooldownTime = b"\x53"

    @staticmethod
    def playerControllerByIndex(idx: int) -> list:
        specialOffset = 0x30
        specialOffset += idx * 0x18
        offset = [
            GameAssembly.Class.ptr_PlayerControllerClass,
            Offsets.PlayerController.Class.ptr_staticFields,
            Offsets.PlayerController.Class.StaticField.playersListWithAgoraIDs,
            0x18,
            specialOffset,
            0,
        ]
        return offset

    @staticmethod
    def localPlayer() -> list:
        return [
            GameAssembly.Class.ptr_LocalPlayerClass,
            Offsets.LocalPlayer.Class.ptr_staticFields,
            Offsets.LocalPlayer.Class.StaticField.ptr_localPlayer,
            0,
        ]
