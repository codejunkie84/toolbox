from .handler.help import HelpHandler
from .handler.project import ProjectHandler
from .handler.httpd import HttpdHandler


def main(argc: int, argv: list) -> int:
    command = None
    if argc > 1:
        command = argv[1]

    if command == 'help' and argc == 2:
        return HelpHandler.show(argc, argv)

    if command == 'project:create' and argc in [4, 5]:
        return ProjectHandler.create(argc, argv)

    if command == 'vhost:create' and argc >= 3:
        return HttpdHandler.create(argc, argv)

    if command == 'vhost:refresh-tls' and argc == 3:
        return HttpdHandler.refresh_tls(argc, argv)

    HelpHandler.show(argc, argv)
    return 1
