# TODOs

## Commands

### Project
- [x] `project:create <language> <project name> [<project description>]` to create a new project on GitHub with an initial commit.
- [ ] `project:load <project name>` to download a repository from GitHub and executes directly pip or composer - depending of the programming language.

### Httpd
- [x] `httpd:create <domain> [<domain aliases ...>]` to create a new vhost for a domain with TLS certificate.
- [x] `httpd:refresh-tls <domain>` to update the TLS certificate of a domain.

### Directory
- [ ] `directory:dispatch` to move files depending of their extension into directories.

### Timer
- [ ] `timer:start [<description>]` to start an internal timer to evaluate the worktime on a task.
- [ ] `timer:stop` to stop the timer and display the duration.
- [ ] `timer:show` to display display the times and dureations.


