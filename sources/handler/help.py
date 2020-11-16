class HelpHandler:
    @staticmethod
    def show(argc: int, argv: list) -> int:
        print('toolbox')
        print('-------------------------------------------------------')
        print("Simple tool in which my common work steps are automated and collected")
        print()
        print('Project Commands:')
        print('  bin/toolbox project:create <language> <project name> [<project description>]')
        print('    Creates a new private GitHub repository for <project name> with a <language> template')
        print('    Supported languages: python')
        print()

        return 0
