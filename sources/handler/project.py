from github import Github
from subprocess import DEVNULL, STDOUT, check_call
from pathlib import Path
from configparser import ConfigParser
import os


class ProjectHandler:
    @staticmethod
    def create(argc: int, argv: list) -> int:
        # check whether config exists is filled out
        # --------------------------------------------------------------------------------------------------------------
        path = Path('data/config.ini')
        if not path.is_file():
            print('ERROR: config.ini does not exists in data directory.')
            return -1

        config = ConfigParser()
        config.read(path.absolute())

        if not config.has_option('github', 'token') or not config['github']['token']:
            print('ERROR: config.ini does not provide github.username')
            return -1

        # create repository
        # --------------------------------------------------------------------------------------------------------------
        g = Github(config['github']['token'])
        user = g.get_user()
        repo_name = argv[3]
        repo_description = ""
        if argc > 4:
            repo_description = argv[4]

        if repo_name in [r.name for r in user.get_repos()]:
            print("ERROR: repository already exists")
            return -1

        repo = user.create_repo(repo_name, private=True)

        # create directories
        # --------------------------------------------------------------------------------------------------------------
        Path(repo_name + '/').mkdir(parents=True)
        Path(repo_name + '/bin/').mkdir(parents=True)
        Path(repo_name + '/sources/').mkdir(parents=True)
        Path(repo_name + '/documents/').mkdir(parents=True)
        Path(repo_name + '/README.md').write_text('# ' + repo_name)

        # gitignore
        # --------------------------------------------------------------------------------------------------------------
        content = """
# project stuff
##############################################################################
/.idea/
/data/cache/
/data/config.ini

# OS generated files
##############################################################################
.DS_Store
.DS_Store?
._*
*~
.Trashes
ehthumbs.db
Thumbs.db
*.log

# python
##############################################################################
__pycache__/
*.py[cod]
*$py.class
/venv/

# php
##############################################################################
/composer.phar
/composer.lock
/vendor/
"""
        Path(repo_name + '/.gitignore').write_text(content.lstrip())

        # PHP dummy project
        # --------------------------------------------------------------------------------------------------------------
        if argv[2] == 'php':
            # starter cli
            content = """
#! /usr/bin/env php
<?php
declare(strict_types=1);

use Application\\Kernel;

require_once __DIR__ . '/../vendor/autoload.php';

echo (new Kernel())->run($_SERVER['argv'][1] ?? '');
"""
            Path(repo_name + '/bin/cli').write_text(content.lstrip())

            # starter www
            Path(repo_name + '/public/').mkdir(parents=True)
            content = """
<?php
declare(strict_types=1);

use Application\\Kernel;

require_once __DIR__ . '/../vendor/autoload.php';

echo (new Kernel())->run(explode('?', $_SERVER['REQUEST_URI'])[0]);
"""
            Path(repo_name + '/public/index.php').write_text(content.lstrip())

            content = """
RewriteEngine On

# Reroute any incoming request that is not an existing file
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ index.php [QSA,L]

"""
            Path(repo_name + '/public/.htaccess').write_text(content.lstrip())

            # kernel
            content = """
<?php
declare(strict_types=1);

namespace Application;

use ErrorException;

class Kernel
{
    public function __construct()
    {
        // initialize environment
        // ------------------------------------------------------------------------------------------------------------
        date_default_timezone_set('UTC');
        error_reporting(- 1);
        ini_set('display.errors', '1');
        define('LF', "\\n");
        define('IS_DEBUG', isset($_COOKIE['debug'])));
        chdir(__DIR__ . '/../');

        // set up error handling
        // ------------------------------------------------------------------------------------------------------------
        set_error_handler(function ($code, $message, $file, $line) {
            $codeCaptions = [
                E_WARNING => 'Warning',
                E_NOTICE => 'Notice',
                E_USER_ERROR => 'User Error',
                E_USER_WARNING => 'User Warning',
                E_USER_NOTICE => 'User Notice',
                E_STRICT => 'Runtime Notice',
                E_RECOVERABLE_ERROR => 'Catchable Fatal Error'
            ];

            throw new ErrorException(sprintf('%s: %s in %s line %d', $codeCaptions[$code], $message, $file, $line));
        });

        set_exception_handler(function ($e) {
            if (IS_DEBUG) {
                header('Content-Type: text/plain; charset=utf-8');
                die($e);
            }

            echo "500";
            die;
        });

        // set up
        // ------------------------------------------------------------------------------------------------------------
        // TODO: fill out
    }

    public function run(string $url): string
    {
        // TODO: fill out
        return __METHOD__;
    }
}
"""
            Path(repo_name + '/sources/Kernel.php').write_text(content.lstrip())

            # composer.json
            content = """
{
    "require" : {
        "php" : ">=7.4.0",
        "ext-intl": "*",
        "ext-curl": "*",
        "ext-pdo": "*",
        "ext-json": "*"
    },
    "autoload" : {
        "psr-4" : {
            "Application\\\\" : "sources/",
            "Test\\\\Application\\\\" : "tests/"
        }
    }
}
"""
            Path(repo_name + '/composer.json').write_text(content.lstrip())

        # Python dummy project
        # --------------------------------------------------------------------------------------------------------------
        if argv[2] == 'python':
            # starter
            content = """
#! /usr/bin/env python3
from os import path

if __name__ == '__main__':
    import sys
    sys.path.append(path.join(path.dirname(__file__), '..'))
    from sources.application import main
    exit(main(len(sys.argv), sys.argv))
"""
            Path(repo_name + '/bin/' + repo_name).write_text(content.lstrip())

            # main function
            content = """
from .handler.help import HelpHandler


def main(argc: int, argv: list) -> int:
    command = None
    if argc > 1:
        command = argv[1]

    if command == 'help' and argc == 2:
        return HelpHandler.show(argc, argv)

    HelpHandler.show(argc, argv)
    return 1
"""
            Path(repo_name + '/sources/application.py').write_text(content.lstrip())

            # handler
            Path(repo_name + '/sources/handler/').mkdir(parents=True)
            content = f"""
class HelpHandler:
    @staticmethod
    def show(argc: int, argv: list) -> int:
        print('{repo_name}')
        print('-------------------------------------------------------')
        print("{repo_description}")
        print()
        print('Dummy Commands:')
        print('  bin/{repo_name} dummy:action <dummy file>')
        print('    Dummy command description')
        print()

        return 0
"""
            Path(repo_name + '/sources/handler/help.py').write_text(content.lstrip())

            # create venv
            # check_call(['python3', '-m', 'venv', 'venv'], stdout=DEVNULL, stderr=STDOUT)

        # init git
        # --------------------------------------------------------------------------------------------------------------
        cwd = os.getcwd()
        os.chdir(repo_name)
        check_call(['git', 'init'], stdout=DEVNULL, stderr=STDOUT)
        check_call(['git', 'add', '.'], stdout=DEVNULL, stderr=STDOUT)
        check_call(['git', 'commit', '-m', 'initial commit'], stdout=DEVNULL, stderr=STDOUT)
        check_call(['git', 'branch', '-M', 'main'], stdout=DEVNULL, stderr=STDOUT)
        check_call(['git', 'remote', 'add', 'origin', 'git@github.com:' + repo.full_name + '.git'], stdout=DEVNULL,
                   stderr=STDOUT)
        os.chdir(cwd)

        return 0
