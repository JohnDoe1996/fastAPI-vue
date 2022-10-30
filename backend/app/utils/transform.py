import re


def camel_case_2_underscore(name: str, /, *, symbol: str = '_') -> str:
    """
    驼峰命名转下划线命名MallUser, mailName 替换成 mall_user
    :param name:
    :param symbol:  链接符号， 默认是下划线
    :return:
    """
    name_list = re.findall(r"[A-Z][a-z\d]*", name[0].upper() + name[1:])
    return symbol.join(name_list).lower()


def list_2_tree(list_data: list, parent_key: str = "parent_id") -> list:
    """
    列表转树状结构的列表
    :param list_data:
    :param parent_key: 父节点的key
    :return:
    """

