import os
import subprocess


def init_arch():
    ls = os.listdir('.')
    # check if dir is valid
    if 'lib' not in ls:
        print('No \'lib\' found here!')
        return
    # create 'core' directory
    try:
        os.makedirs('lib/core')
    except FileExistsError:
        print('\'core\' dir exists!')
    # create 'modules' directory
    try:
        os.makedirs('lib/modules')
    except FileExistsError:
        print('\'modules\' dir exists!')
    # create constants directory with classes
    try:
        os.makedirs('lib/core/constants')
    except FileExistsError:
        print('\'core/constants\' dir exists!')
    os.system('touch lib/core/constants/strings.dart')
    os.system('touch lib/core/constants/colors.dart')
    os.system('touch lib/core/constants/urls.dart')


# path with no ending '/'
def init_module(path):
    if os.system('cd ' + path) != 0:
        print('invalid path to module')
    # first layer
    os.makedirs(path + "/data")
    os.makedirs(path + "/domain")
    os.makedirs(path + "/presentation")
    # second layer
    os.makedirs(path + "/data/datasource")
    os.makedirs(path + "/data/repository")
    os.makedirs(path + "/data/models")
    # second layer
    os.makedirs(path + "/domain/entities")
    os.makedirs(path + "/domain/repository")
    os.makedirs(path + "/domain/usecases")
    # seconds layer
    os.makedirs(path + "/presentation/bloc")
    os.makedirs(path + "/presentation/pages")
    os.makedirs(path + "/presentation/widgets")
    # third layer
    os.makedirs(path + "/presentation/bloc/states")
    os.makedirs(path + "/presentation/bloc/events")


def add_module():

    if os.system('cd lib/modules') != 0:
        print('No modules found, try 1) ')
        return

    name = input("Name of module: ")

    try:
        os.mkdir('lib/modules/' + name)
    except Exception:
        print('Invalid name')
        return
    init_module('lib/modules/' + name)

# exact path for repo, without ending '/'


def create_a_repo(path, name, data, path2):
    if os.system("cd " + 'lib/' + path) != 0:
        print('invalid path for creating a repository')
        return

    if data:
        if os.system('touch ' + 'lib/' + path + "/" + name.lower() + "_repository.dart") != 0:
            print('can\'t create ' + 'lib/' + path +
                  "/" + name.lower() + "_repository.dart")
            return
    else:
        if os.system('touch ' + "lib/" + path + "/" + name.lower() + "_repository_impl.dart") != 0:
            print('can\'t create ' + "lib/" + path + "/" +
                  name.lower() + "_repository_impl.dart")
            return

    # if file exists, return
    if data:
        file_path = "lib/" + path + "/" + name.lower() + "_repository.dart"
        output = subprocess.check_output(
            "cat " + file_path, shell=True
        )
        if (not (output is None or len(output) == 0)):
            return
    else:
        file_path = "lib/" + path + "/" + name.lower() + "_repository_impl.dart"
        output = subprocess.check_output(
            "cat " + file_path, shell=True
        )
        if (not (output is None or len(output) == 0)):
            return

    if data:
        os.system("""
    sudo printf \"/// Auto Generated Repository based on {} Entity \\nabstract class {}Repository {{ \\n   /// repository fields \\n\\n}}  \" > {}
        """.format(name, name, "lib/" + path + "/" + name.lower() + "_repository.dart" ))
    else:
         os.system("""
    sudo printf \"import 'package:project/{}';    \\n\\n/// Auto Generated Repository Implementation based on {} Entity \\nclass {}RepositoryImpl extends {}Repository {{ \\n   /// repository fields \\n\\n}}  \" > {}
        """.format(path2 + "/" + name.lower() + "_repository.dart", name, name,name, "lib/" + path + "/" + name.lower() + "_repository_impl.dart" ))


def create_repos():
    module = input('module name: ')

    if os.system('cd lib/modules/' + module) != 0:
        print('invalid module name, first create it!')
        return

    try:
        entities = os.listdir('lib/modules/' + module + "/domain/entities")
    except Exception:
        print('project not initialized correctly!')
        return

    entity_names = []

    for entity in entities:
        output = subprocess.check_output(
            "cat lib/modules/" + module + "/domain/entities/" + entity, shell=True)
        output = output.decode('utf-8')
        ind = (output.find('class'))
        ind3 = output.find('{')
        entity_names.append(output[ind + 6: ind3].strip())

    for entity_name in entity_names:
        create_a_repo('modules/' + module + '/domain/repository',
                      entity_name, True, 'modules/' + module + '/data/repository')
        create_a_repo('modules/' + module + '/data/repository',
                      entity_name, False, 'modules/' + module + '/domain/repository')


if __name__ == "__main__":

    while True:
        print("""
\nEnter a number:
    1)  initialize clean architecture packaging here
    2)  add a new module (feature)
    3)  create \'repositories\' according to \'entities\' of a module
    4)  exit\n
        """)
        cmd = int(input())
        if (cmd == 1):
            init_arch()
        if (cmd == 4):
            exit()
        if (cmd == 2):
            add_module()
        if (cmd == 3):
            create_repos()
