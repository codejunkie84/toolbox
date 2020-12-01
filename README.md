# toolbox
Simple tool in which my common work steps are automated and collected.

## Installation
There is actually no setup script, so the installation have to be done manually. Just enter the following in your local Shell - after this you can just write `toolbox` to use the application.

```bash
# clone
git clone git@github.com:codejunkie84/toolbox.git
cd toolbox

# create config
cp data/config.ini.dist data/config.ini
vim data/config.ini

# setup venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

# setup environment
echo "# add this to your environment"
echo "export PATH=\$PATH:'$(pwd)/bin/'"
```

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

### Httpd Commands
Commands for managing the Httpd service on centos (Apache 2)
```
bin/toolbox httpd:create <domain> [<domain aliases ...>]
  Creates a new virtual host configuration and hosting directory with TLS certificate

bin/toolbox httpd:refresh-tls <domain>
  Refreshes the TLS certificate
```

## Contribute
As an open source project all contributions are welcome. Feel free to support this project with pull requests and your own improvements.

## Copyright
**toolbox** is released under MIT license and is open to contributions. Toolbox was originally written by Patrick Ullmann.