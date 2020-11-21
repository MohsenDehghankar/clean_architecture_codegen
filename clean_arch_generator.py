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
    # platform
    try:
        os.makedirs('lib/core/platform')
    except FileExistsError:
        print('\'core/platform\' dir exists!')
    os.system('touch lib/core/constants/strings.dart')
    os.system(
        'echo \"/// Define Your Constant Strings Here.\" > lib/core/constants/strings.dart')
    os.system('touch lib/core/constants/colors.dart')
    os.system(
        'echo \"/// Define Your Constant Color Values Here.\" > lib/core/constants/colors.dart')
    os.system('touch lib/core/constants/urls.dart')
    os.system(
        'echo \"/// Define Your Constant API URLs Here.\" > lib/core/constants/urls.dart')
    os.system('touch lib/core/constants/assets.dart')
    os.system(
        'echo \"/// Define Your Constant Asset Addresses Here.\" > lib/core/constants/assets.dart')


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
        """.format(name, name, "lib/" + path + "/" + name.lower() + "_repository.dart"))
    else:
        os.system("""
    sudo printf \"import 'package:project/{}';    \\n\\n/// Auto Generated Repository Implementation based on {} Entity \\nclass {}RepositoryImpl extends {}Repository {{ \\n   /// repository fields \\n\\n}}  \" > {}
        """.format(path2 + "/" + name.lower() + "_repository.dart", name, name, name, "lib/" + path + "/" + name.lower() + "_repository_impl.dart"))


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


def get_project_name():
    return subprocess.check_output("basename \"$PWD\"", shell=True).decode('utf-8').strip()


def write_state(module, page_name_class, page_name_file):
    tmp_file = open('lib/modules/{}/presentation/bloc/states/{}'.format(module,
                                                                        page_name_file + "_states.dart"), 'w')
    tmp_file.write(
        """
/// Auto Generated State
abstract class {0}State {{}}

class {1}StateStart extends {2}State {{}}
        """.format(page_name_class, page_name_class, page_name_class)
    )
    tmp_file.close()
    tmp_file = open('lib/modules/{}/presentation/bloc/events/{}'.format(module,
                                                                        page_name_file + "_events.dart"), 'w')
    tmp_file.write(
        """
/// Auto Generated Event
abstract class {0}Event {{}}
        """.format(page_name_class)
    )
    tmp_file.close()


def create_bloc(module, page_name_class, page_name_file):
    if os.system('touch lib/modules/{}/presentation/bloc/{}'.format(module, page_name_file + "_bloc.dart")) != 0:
        print('can not create bloc file!')
        return
    if os.system('touch lib/modules/{}/presentation/bloc/states/{}'.format(module, page_name_file + "_states.dart")) != 0:
        print('can not create states file!')
        return
    if os.system('touch lib/modules/{}/presentation/bloc/events/{}'.format(module, page_name_file + "_events.dart")) != 0:
        print('can not create events file!')
        return
    project_name = get_project_name()
    tmp_file = open(
        'lib/modules/{}/presentation/bloc/{}'.format(module, page_name_file + "_bloc.dart"), 'w')
    tmp_file.write(
        """
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{12}/modules/{8}/presentation/bloc/events/{10}_events.dart';
import 'package:{13}/modules/{9}/presentation/bloc/states/{11}_states.dart';

/// Auto Genrated Class for {0} page
class {1}Bloc extends Bloc<{2}Event, {3}State> {{

    // feel free to change first state
    {4}Bloc() : super({5}StateStart());

    @override
    Stream<{6}State> mapEventToState({7}Event event) async* {{
        // todo implement
        throw UnimplementedError();
    }}
}}
        """.format(page_name_class,
                   page_name_class,
                   page_name_class,
                   page_name_class,
                   page_name_class,
                   page_name_class,
                   page_name_class,
                   page_name_class,
                   module,
                   module,
                   page_name_file,
                   page_name_file,
                   project_name.strip(),
                   project_name.strip()
                   )
    )
    tmp_file.close()
    write_state(module, page_name_class, page_name_file)


def create_widget(module, page_name_class, page_name_file):
    if os.system('touch lib/modules/{}/presentation/widgets/{}'.format(module, page_name_file + "_widget.dart")) != 0:
        print('can not create widget file!')
        return
    tmp_file = open('lib/modules/{}/presentation/widgets/{}'.format(module,
                                                                    page_name_file + "_widget.dart"), 'w')
    tmp_file.write(
        """
import 'package:flutter/material.dart';

/// Auto Generated Widget Class For Page {0}
class {1}Widget extends StatelessWidget {{
    @override
    Widget build(BuildContext context){{
        // todo implement
        throw UnimplementedError();
    }}
}}
        """.format(page_name_class, page_name_class)
    )
    tmp_file.close()


def create_page():
    module = input('module name: ')
    # check name of module
    if os.system('cd lib/modules/' + module) != 0:
        print('invalid module name!')
        return
    # create page class file
    page_name_file = input('the page file name(with no .dart)? ')
    page_name_class = input('the page class name? ')
    if os.system('touch lib/modules/' + module + '/presentation/pages/' + page_name_file + '.dart') != 0:
        print('Can\'t create the page in presentation/pages dir!')
        return
    # create the class inside the page class file
    project_name = get_project_name()
    content = """
import 'package:{11}/modules/{8}/presentation/bloc/{13}_bloc.dart';
import 'package:{12}/modules/{9}/presentation/widgets/{14}_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

/// This is Page is created automatically feel free to make changes
class {0} extends StatefulWidget {{
  @override
  {2}State createState() => {1}State();
}}

class {3}State extends State<{4}> {{
  @override
  Widget build(BuildContext context) {{
    return BlocProvider(
      create: (context) => {5}Bloc(),
      child: Scaffold(
        resizeToAvoidBottomInset: false,
        body: {6}Widget(),
      ),
    );
  }}
}}

    """.format(page_name_class,
               page_name_class,
               page_name_class,
               page_name_class,
               page_name_class,
               page_name_class,
               page_name_class,
               module,
               module,
               module,
               project_name.strip(),
               project_name.strip(),
               project_name.strip(),
               page_name_file,
               page_name_file)

    # put content to the page.dart
    page_file = open(
        'lib/modules/{0}/presentation/pages/{1}.dart'.format(module, page_name_file), 'w')
    page_file.write(content)
    page_file.close()

    create_bloc(module, page_name_class, page_name_file)
    create_widget(module, page_name_class, page_name_file)


if __name__ == "__main__":

    while True:
        print("""
\nEnter a number:
    1)  initialize clean architecture packaging here
    2)  add a new module (feature)
    3)  create \'repositories\' according to \'entities\' of a module
    4)  create a new page in a module
    5)  exit\n
        """)
        cmd = int(input())
        if (cmd == 1):
            init_arch()
        if (cmd == 5):
            exit()
        if (cmd == 2):
            add_module()
        if (cmd == 3):
            create_repos()
        if (cmd == 4):
            create_page()
            print('Don\'t forget to add dependencies to pubspec.yaml.')
