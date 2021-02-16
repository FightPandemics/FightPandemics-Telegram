class BaseCall:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if len(self._args) != len(other._args):
            return False
        if len(self._kwargs) != len(other._kwargs):
            return False
        for self_arg, other_arg in zip(self._args, other._args):
            if self_arg != other_arg:
                return False
        for self_key, self_value in self._kwargs.items():
            if self_key not in other._kwargs:
                return False
            other_value = other._kwargs[self_key]
            if self_value == ANY or other_value == ANY:
                continue
            if self_value != other_value:
                return False
        return True

    def __str__(self):
        return repr(self)

    def __repr__(self):
        args_str = ', '.join(repr(arg) for arg in self._args)
        kwargs_str = ', '.join(f"{key}={repr(value)}" for key, value in self._kwargs.items())
        return f"{self.__class__.__name__}({args_str}, {kwargs_str})"


class PostCall(BaseCall):
    pass


class GetCall(BaseCall):
    pass


class ANY:
    pass
