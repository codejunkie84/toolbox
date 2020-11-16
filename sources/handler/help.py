class HelpHandler:
    @staticmethod
    def show(argc: int, argv: list) -> int:
        print('toolbox')
        print('-------------------------------------------------------')
        print("")
        print()
        print('Dummy Commands:')
        print('  bin/toolbox dummy:action <dummy file>')
        print('    Dummy command description')
        print()

        return 0
