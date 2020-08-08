import json
import os
import pprint
import re
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_NAME_DFLT = 'config.json'
CONFIG_PATH_DFLT = os.path.join(HERE, CONFIG_FILE_NAME_DFLT)
CWD = os.getcwd()

SUBSTITUTIONS = {
    'CWD': CWD,
    'HERE': HERE,
}



def get_config_path():
    try:
        path = sys.argv[1]
    except IndexError:
        path = CONFIG_PATH_DFLT
    if not os.path.isfile(path):
        raise ValueError(f'No DativeTop config file at {path}.')
    return path


def parse_config_from_json(path):
    try:
        with open(path, 'rb') as f:
            return json.load(f)
    except Exception:
        raise ValueError(f'Failed to parse correct JSON from {path}.')


class Nil:
    pass


nil = Nil()


def override_with_env_var(k, v):
    env_var_v = os.environ.get(k.upper(), nil)
    if env_var_v is nil:
        return v
    return env_var_v


def override_with_env_vars(config_json):
    return {k: override_with_env_var(k, v) for k, v in config_json.items()}


VAR_PATT = re.compile('<(\w+)>')


def sub_vars(v, config_json):
    def sub_var(match):
        act_match = match.group(1)
        try:
            return SUBSTITUTIONS[act_match]
        except KeyError:
            try:
                return config_json[act_match]
            except KeyError:
                raise ValueError(
                    f'No match for {match.group(0)} in global substitutions or'
                    f' in config itself.')
    return VAR_PATT.sub(sub_var, v)


def contains_vars(config_json):
    return any([v for v in config_json.values() if VAR_PATT.search(v)])


def sub_all_vars(config_json):
    if contains_vars(config_json):
        return sub_all_vars(
            {k: sub_vars(v, config_json)
             for k, v in config_json.items()})
    return config_json


def threadf(initial, *funcs):
    for func in funcs:
        initial = func(initial)
    return initial


def get_settings(config_path=None):
    config_path = config_path or get_config_path()
    return threadf(
        config_path,
        parse_config_from_json,
        override_with_env_vars,
        sub_all_vars,
    )


def main():
    pprint.pprint(get_settings())


if __name__ == '__main__':
    main()
