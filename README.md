# toolbox
Simple tool in which my common work steps are automated and collected

## Installation
For a simple "installation" just clone or download this repository, create a copy of `data/config.ini.dist` to `data/config.ini` and fill it out, after that just start using this tool by executing `bin/toolbox` with Python at the command line.

## Description
**toolbox** is a simple command-line program which contains my common work steps in an automated form. It requires the Python interpreter, version 3.7+, and it is not platform specific. The application works on your macOS, Linux and Windows.

## Commands
In toolbox the commands are prefixed regarding their topic.

### Project Commands
```
bin/toolbox project:create <language> <project name> [<project description>]
  Creates a new private GitHub repository for <project name> with a <language> template
  Supported languages: python
```

## Contribute
As an open source project all contributions are welcome. Feel free to support this project with pull requests and your own improvements.

## Copyright
**toolbox** is released under MIT license and is open to contributions. Toolbox was originally written by Patrick Ullmann.