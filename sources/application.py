from .handler.help import HelpHandler


def main(argc: int, argv: list) -> int:
    command = None
    if argc > 1:
        command = argv[1]

    if command == 'help' and argc == 2:
        return HelpHandler.show(argc, argv)

    HelpHandler.show(argc, argv)
    return 1
