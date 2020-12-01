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
        print('Httpd Commands:')
        print('  bin/toolbox httpd:create <domain> [<domain aliases ...>]')
        print('    Creates a new virtual host configuration and hosting directory with TLS certificate')
        print('')
        print('  bin/toolbox httpd:refresh-tls <domain>')
        print('    Refreshes the TLS certificate')
        print('')
        print()

        return 0
