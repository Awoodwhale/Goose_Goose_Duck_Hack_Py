names = (
    "无",
    "鹅",
    "鸭",
    "呆呆鸟",
    "赏金",
    "Mechanic",
    "Technician",
    "通灵",
    "正义使者",
    "食鸟鸭",
    "变形者(鸭子)",
    "警长",
    "静语者(鸭子)",
    "加拿大鹅",
    "恋人(鸭子)",
    "恋人(鹅)",
    "秃鹫",
    "专业杀手(鸭子)",
    "间谍(鸭子)",
    "模仿者",
    "侦探",
    "鸽子",
    "观鸟者",
    "刺客(鸭子)",
    "猎鹰",
    "雇佣杀手(鸭子)",
    "保镖鹅",
    "告密者(鸭子)",
    "政治家",
    "锁匠",
    "殡仪员",
    "网红",
    "派对狂(鸭子)",
    "爆炸王(鸭子)",
    "决斗呆呆鸟",
    "【猎鹅】鹅",
    "【猎鹅】鸭子",
    "【猎鹅】赏金鹅",
    "【HNS】鹅",
    "【HNS】鸭子",
    "【HNS】赏金鹅",
    "【霸王餐】鸭子",
    "【霸王餐】猎鹰",
    "【霸王餐】秃鹫",
    "【霸王餐】变形鸭",
    "FPGoose",
    "ExploreGoose",
    "【TT】吸血鬼",
    "【TT】村民",
    "【TT】鬼奴",
    "旁观",
    "身份窃贼",
    "冒险家",
    "复仇者",
    "忍者(鸭子)",
    "丧葬者",
    "Snoop",
    "超能力者",
    "隐身者",
    "星界行者",
    "鹈鹕",
    "【TTE】鬼奴",
    "【TT】木乃伊",
    "连环杀手(鸭子)",
    "工程师",
    "术士(鸭子)",
    "流浪儿童",
    "追踪者",
)


def get_role_name(id: int) -> str:
    """更具角色id获取角色名称

    :param id: 角色id
    :type id: int
    :return: 角色名称
    :rtype: str
    """
    if id >= len(names):
        return names[0]
    return names[id]

def Singleton(cls):
    """装饰器单例模式

    :return: 单例对象
    :rtype: obj
    """
    _instance = {}

    def _singleton(*args, **kwagrs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwagrs)
        return _instance[cls]

    return _singleton