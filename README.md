# cli-stryket

CLI for the popular Swedish betting game [Stryktipset](https://spela.svenskaspel.se/stryktipset)

Enter your system and work your way to 13 correct and the millions using the cli-stryket. Your friends will probably think you are the coolest person alive, or the geekiest person alive.

cli-stryket fetches live data and correct your system in real-time.

The CLI is built using the curses python library which supplies a terminal-independent screen-painting and keyboard-handling facility for text-based terminals.

![image](https://user-images.githubusercontent.com/8545435/164912734-094959df-8ad5-4a4e-8916-c2b434e40aee.png)


## Requirements
- Python3

## Installation

```bash
git clone https://github.com/mile95/cli-stryket.git
cd cli-stryket
pip3 install .

```
## How to run

```
cli-stryket --input-file system.txt
```

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

## Known Issues
- When a game goes from NOT STARTED to STARTED state, the time text is not cleared properly, resulting in some overwriting of text. Fix: Restart the application.
- Between 4 pm and 7 pm on Saturdays, the traffic at Svenskaspel is high, resulting in the requests sometimes timeouts after 8s, which is currently not handled by the application. Fix: Restart the application.

# Contribute?

Questions, Issues, or PRs are more than welcome! Happy Hacking.
