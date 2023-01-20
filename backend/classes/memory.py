from bisect import bisect_left
from typing import OrderedDict, List
from collections import OrderedDict as odict
from pymem import Pymem
from pymem.memory import virtual_query
from pymem.ressources.structure import MEMORY_STATE, MEMORY_PROTECTION
from backend.utils.log import log
from backend.utils.utils import Singleton


@Singleton
class Memory:
    mem: Pymem  # Pymem对象
    _mem_map: OrderedDict[int, int] = odict()  # 内存地址map
    process_name: str = "Goose Goose Duck.exe"  # 游戏名称
    assembly_module_name: str = "GameAssembly.dll"  # 读写的dll
    assembly_base_address: int = 0  # dll基地址
    pid: int = 0  # pid不为0标志着memory初始化完成

    def __init__(self) -> None:
        # self.init()
        pass

    def init(self) -> None:
        if self.__init_process():
            self.read_all_memory()
            self.pid = self.mem.process_id
            return True
        return False

    def __init_process(self) -> bool:
        """初始化进程

        :return: 初始化是否成功
        :rtype: bool
        """
        try:
            self.mem = Pymem(self.process_name)
        except Exception as e:
            log(f"Failed to init memory. {e}", "error")
            return False

        self.assembly_base_address = self.__get_module_base_address(
            self.assembly_module_name
        )

        if self.assembly_base_address == 0:
            log("Failed to get base address!", "error")
            return False

        log("Success init game process!", "info")
        return True

    def __get_module_base_address(self, module_name: str) -> int:
        """获取dll基地址

        :param module_name: dll名称
        :type module_name: str
        :return: 基地址
        :rtype: int
        """
        for module in self.mem.list_modules():
            if module.name == module_name:
                log(f"Find module <{module_name}>")
                log(f"Find module base address <{module.lpBaseOfDll:#x}>")
                log(f"Find module SizeOfImage <{module.SizeOfImage:#x}>")
                return module.lpBaseOfDll
        log(f"Not find module <{module_name}>!", "error")
        return 0

    def read_all_memory(self) -> None:
        """读取可读的内存区间并放入map中"""
        _addr = 0
        try:
            while mbi := virtual_query(self.mem.process_handle, _addr):
                if mbi.State == MEMORY_STATE.MEM_COMMIT and mbi.Protect not in [
                    MEMORY_PROTECTION.PAGE_NOACCESS,
                    MEMORY_PROTECTION.PAGE_GUARD,
                ]:
                    # if mbi.BaseAddress not in tuple(self._mem_map.keys()):
                    # log(f"{mbi.BaseAddress:#x} ~ {mbi.BaseAddress+mbi.RegionSize:#x} 加入合法区间")
                    self._mem_map[mbi.BaseAddress] = mbi.RegionSize
                _addr += mbi.RegionSize
        except:
            pass

    def is_legal_address(self, address: int) -> bool:
        """判断地址是否合法

        :param address: 内存地址
        :type address: _type_
        :return: 是否合法
        :rtype: bool
        """
        # ? 也许不需要去检查地址的合法性? 直接读，如果报错就返回0
        if _keys := tuple(self._mem_map.keys()):
            _idx = bisect_left(_keys, address) - 1
            if _idx < 0 or _idx >= len(_keys):
                return False
            if address < self._mem_map[_keys[_idx]] + _keys[_idx]:
                return True
            return False
        return False

    def find_pointer(
        self, base_addr: int, offsets: List[float], debug: bool = False
    ) -> int:
        """寻找指针(多级偏移)

        :param base_addr: 基地址
        :type base_addr: int
        :param offsets: 偏移列表
        :type offsets: List[float]
        :return: 指针地址
        :rtype: int
        """

        #! 目前没有开启is_legal_address的检测，因为如果在游戏开启后立即开启本程序，读取的memory地址空间缺失，会导致之后判定地址为非法地址
        # TODO: 寻找热更新_mem_map的方式
        if len(offsets) <= 0:
            return 0
        try:
            addr = base_addr + offsets[0]
            # if not self.is_legal_address(addr):
            #     return 0
            addr = self.mem.read_longlong(addr)
            if debug:
                log(f"debug0: {addr:#x}")
            if len(offsets) <= 1:
                # if self.is_legal_address(addr):
                #     return addr
                # return 0
                return addr
            addr += offsets[1]
            if debug:
                log(f"debug1: {addr:#x}")
            for i in range(2, len(offsets)):
                addr = self.mem.read_longlong(addr)
                if debug:
                    log(f"debug{i}: {addr:#x}")
                if addr == 0:  # ? or not self.is_legal_address(addr)
                    if debug:
                        log(f"debug{i} {addr:#x} 不是合法地址")
                    return 0
                addr += offsets[i]
            return addr
        except:
            # 可能存在错误,原因是上述for循环中没有检测addr的合法性
            # 至于为啥不检查是因为无法确定进程是否加载完毕
            return 0
