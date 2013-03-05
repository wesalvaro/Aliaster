# Aliaster

### What is this?

You and I both type way too much on the console. This helps us quit.
    
When you use an alias, you get points equal to the number of keystrokes you saved in the process. Each command you type is put in a file along with how many times you used the command. Commands are split so that partial commands are counted, as well.

For example:

    make -j8 foo
    make -j8 bar

After these two commands, `make` and `make -j8` have a count of 2. But `make -j8 foo` and `make -j8 bar` have a count of only one. In this way, partial commands can be suggested for aliases, as well.

### Requirements:
ZSH or you to figure out your shell's preexec analog.

### Installation:
    touch $HOME/.aliaster
    function preexec {
      python /path/to/aliaster.py $1 "`whence -w $1 | egrep -q \"function|alias\" && whence -f $1 | wc -c`"
      export ALIASTER=$?
    }

### Usage:
1. Use your shell as normal.
2. To view suggestions, type `aliaster` as if it were a command.

### Configure:
There are a few settings you may wish to change:

* `FREQ_FILE`: In which file will the counts go?
* `FREQ_THRESHOLD`: How many times should a command be used before listing it as a suggestion?
* `SUGG_LENGTH_THRESHOLD`: How long must a command be to warrant keeping its counts in the file for suggestions?

### Anything else I should know?

* You can clear the count file by recreating the `FREQ_FILE`.
* You can see the counts of everthing by looking in the `FREQ_FILE`.
* Your current score can be found in `$ALIASTER`.

#### License:
GPLv3