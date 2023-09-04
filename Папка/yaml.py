import yaml
from collections import OrderedDict
from typing import List, Dict


def yaml_to_env(config_file: str, pred = '', r = '') -> str:
    data = config_file
    data = yaml.load(data, Loader=yaml.SafeLoader)

    res = ''
    for key, values in data.items():
        if type(values) == dict:
            res += yaml_to_env(str(values), pred + r + key, r = '.')
        else:
            res += pred + r + key + '=' + str(values) + '\n'
    return res

def env_to_yaml(env_list: str) -> str:
    def parse_env(env: List[str]) -> Dict[str, str]:
        nested_dict = OrderedDict()
        for entry in env:
            key, value = entry.split('=')
            parts = key.split('.')
            current_dict = nested_dict
            for part in parts[:-1]:
                if part not in current_dict:
                    current_dict[part] = OrderedDict()
                current_dict = current_dict[part]
            current_dict[parts[-1]] = value
        return nested_dict
    
    def yaml_dump(d: Dict[str, str], indent: int = 0) -> str:
        result = ""
        indentation = ' ' * indent
        for key, value in d.items():
            if isinstance(value, dict):
                result += f"{indentation}{key}:\n{yaml_dump(value, indent + 2)}"
            else:
                result += f"{indentation}{key}: {value}\n"
        return result
    
    env = env_list.strip().split('\n')
    env_dict = parse_env(env)
    yaml_text = yaml_dump(env_dict)
    return yaml_text
            