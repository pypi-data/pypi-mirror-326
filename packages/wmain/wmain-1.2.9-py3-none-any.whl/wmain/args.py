import sys
from typing import List, Dict, Union

class Arg:
    
    def __init__(self, default_value: Union[str, None] = None, help_text: Union[str, None] = None):
        self.default_value: Union[str, None] = default_value
        self.help_text: Union[str, None] = help_text
        self.value: Union[str, None] = None
    
class Args:

    def __init__(self):
        self.__args_dic: Dict[str, Arg] = {}

    def add_arg(self, name: str, required: bool = False, default_value: Union[str, None] = None, help_text: Union[str, None] = None):
        self.__args_dic[name] = Arg(default_value, help_text)
    
    def parse(self, in_str: str):
        if in_str.find("=") == -1:
            raise ValueError("Invalid argument format(not contain '='): " + in_str)
        name, value = in_str.split("=", 1)
        if name not in self.__args_dic:
            raise ValueError("Invalid argument name: " + name)
        self.__args_dic[name].value = value
        
    def __getitem__(self, name: str) -> Union[str, None]:
        if name not in self.__args_dic:
            raise ValueError("Invalid argument name: " + name)
        arg = self.__args_dic[name]
        if arg.value is None:
            if arg.default_value is None:
                raise ValueError("Argument " + name + " is required but not provided")
            return arg.default_value
        return self.__args_dic[name].value
    
    def init_from_argv(self, argv: List[str] = sys.argv[1:]):
        if len(argv) == 1:
            arg = argv[0].strip().strip("-").strip()
            if arg == "help" or arg == "h":
                for arg_name, arg_obj in self.__args_dic.items():
                    if arg_obj.help_text is None:
                        continue
                    print(arg_name + ":", arg_obj.help_text)
                sys.exit(0)
        for arg in argv:
            self.parse(arg)