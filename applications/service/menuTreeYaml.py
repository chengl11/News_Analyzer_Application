import yaml
import glob


def read_yaml(yaml_file_path):
    try:
        with open(yaml_file_path, 'rb') as f:
            cf = f.read()
    except FileNotFoundError:
        print('not fount config')
    c = yaml.safe_load(cf)
    return c


def read_all_yaml(menu_yaml_path):
    lista = []
    lst = glob.glob(menu_yaml_path)
    for l in lst:
        a = read_yaml(l)
        lista.append(a)
    return lista

def make_tree(menu_yaml_path):
    a = read_all_yaml(menu_yaml_path)
    auth_tree = []

    for i in a:
        i_date = i.get('data')
        auth_tree.append(i_date)

    print(auth_tree)

    auth_tree.sort(key=lambda y:y['id'])
    return auth_tree
