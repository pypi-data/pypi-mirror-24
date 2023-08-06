todo
========
###### Simple TODO list generator

### Why
Because i couldn't find any other tool to do (pun unintended) this. Also i
found it annoying to `Ctrl+F` (`Cmd+F`) all the time or run project wide
searches every 2 minutes.

### How
Well, code is a bit dirty and the ignore list is hardcoded, but it is
OpenSource so be my guest and improve it (Could use some regex). The script
cheks for an existing `.git` directory, finds the user and repo (this way it 
creates links to the GitHub file and line) and then searches for the `# TODO`
tag in all source files. Feel free to change it to `// TODO` and `.c`.

### Install
Option 0:
```
pip install todo2
```

Option 1:
```
git clone git@github.com:thee-engineer/todo.git
cd todo
pip install .
```

### Use
Go into your git project folder, run the `todo` command, and then look at your
awesome `TODO.md` file. Add it, commit it, push it, look at it, click on it.
```
cd my_git_project
todo
git add TODO.md
git commit -m "Add TODO.md"
git push
```


### Contribution
Add whatever. Right know the project could use (but I don't want to invest
the time):
- [ ] Regex matches for gitignore rules
- [ ] CL Arguments (this way more feature can be implemented)
- [ ] Option for non-git projects
- [ ] Branch checking
- [ ] Local file links
- [ ] TODO completion check and comment removal

### Support the developer
Buy me a beer or something, donations are welcome.

![](https://img.shields.io/badge/Bitcoin-14xkoFmGcHDaaSbqiVd5fw3FREQeditJ5L-yellow.svg)
[![](https://img.shields.io/badge/Patreon-theeengineer-orange.svg)](https://www.patreon.com/theeengineer)


