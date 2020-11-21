# clean_architecture_codegen
Python Code Generator For Flutter Projects based on Clean Architecture

Usage
  - run this command in your project directory (where lib/ exists)
  - python ./clean_arch_generator.py
 
 Features
  - initialize clean architecture packaging here
    - Creates core/ and modules/ directories
  - add a new module (feature)
    - Creates a new module in modules/ and initilaizes important directories
  - create 'repositories' according to 'entities' of a module (classes that you have defined in 'lib/modules/module_name/domain/entities')
    - After creating entities in 'modules/module_name/domain/entities', creates respository classes in 
      - lib/modules/module_name/data/repository
      - lib/modules/module_name/domain/repository
  - New features will be added soon :)
      
 Example
 
 After running following commands:
  - cd path/to/project_dir
  - python ./path/to/clean_arch_generator.py
  - 1 (first option)
  - 2
    - my_first_module (input)
  - create a class named 'User' in lib/modules/my_first_module/domain/entities/user.dart
  - 3
    - my_first_module
 
 The project will look like this
  - lib/
    - core/
      - constants/
        - strings.dart
        - urls.dart
        - colors.dart
    - modules/
      - my_first_module/
        - data/
          - datasource/
          - models/
          - repository/
            - user_repository_impl.dart
        - domain/
          - entities/
            - user.dart
          - usecases/
          - repository/
            - user_repository.dart
        - presentation/
          - bloc/
            - evets/
            - states/
          - widgets/
          - pages/
          
