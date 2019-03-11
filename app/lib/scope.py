from app.lib.errors import ServerError
from flask import current_app


class Scope:
    allow_func = []
    allow_module = []
    forbidden_func = []
    forbidden_module = []
    type = 0

    def __init__(self):
        # 使用result来保存最终计算的权限结果，view_func的集合
        self.__result = []
        # 计算权限结果
        self.__cal()

    def append(self, other):
        if not isinstance(other, Scope):
            raise ServerError()
        self.allow_func.extend(other.allow_func)
        self.allow_module.extend(other.allow_module)
        self.forbidden_func.extend(other.forbidden_func)
        self.forbidden_module.extend(other.forbidden_module)
        self.__cal()
        return self

    @staticmethod
    def __clear_list_repeat(target_list):
        if not isinstance(target_list, list) or target_list is None:
            raise ServerError()
        return list(set(target_list))

    def __clear_repeat(self):
        self.__clear_list_repeat(self.allow_func)
        self.__clear_list_repeat(self.allow_module)
        self.__clear_list_repeat(self.forbidden_func)
        self.__clear_list_repeat(self.forbidden_module)

    def __cal(self):
        # 去重
        self.__clear_repeat()
        self.__result.clear()
        self.__process_module()
        self.__process_func()
        self.__clear_list_repeat(self.__result)

    def __process_func(self):
        self.__result.extend(self.allow_func)
        for func in self.forbidden_func:
            if func not in self.__result:
                continue
            self.__result.remove(func)

    def __process_module(self):

        """
        处理 allow_module和 forbidden_module
        :return:
        """
        for module in self.allow_module:
            add_func = self.__get_func_by_module(module)
            self.__result.extend(add_func)
        for module in self.forbidden_module:
            remove_func = self.__get_func_by_module(module)
            for func in remove_func:
                if func not in self.__result:
                    continue
                self.__result.remove(func)

    @staticmethod
    def __get_func_by_module(module):
        result = []
        for rule_obj in current_app.url_map.iter_rules():
            rule = rule_obj.rule
            endpoint = rule_obj.endpoint
            import re
            rule = re.sub('/', '.', rule)
            rule = re.sub('<.+', '', rule)
            rule = rule.rstrip('.').lstrip('.')
            rule = '.'.join(rule.split('.')[:2])

            if module == rule:
                result.append(endpoint)
        return result

    @property
    def result(self):
        return self.__result
