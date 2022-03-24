# cli-stryktet

CLI for the popular swedish betting game [Stryktipset](https://spela.svenskaspel.se/stryktipset)

Enter your system rows and let the CLI correct it for you, live!

The CLI is built using the curses python library which supplies a terminal-independent screen-painting and keyboard-handling facility for text-based terminals.

## How to run

`python3 cli-stryket.py system.txt`

`system.txt` is the file containing your system. 

Example `system.txt` : 

```
1x
1x2
12
x
1
2
12
1x2
1x
x2
x
2
x2
```

One row per game. 

## TODO

I've only found a hidden API for Stryktipset, which provides data before the games start. See the temporary script in main.py.

I need to find an API for getting the live results of the 13 games.

Currently, the CLI runs with fake data.
