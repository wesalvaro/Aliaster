"""

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
      python /path/to/aliaster.py $1 "`alias $1`"
      ALIASTER=$?
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

"""
import os
import shlex
import subprocess
import sys
from os import path

FREQ_FILE = path.join(os.getenv('HOME'), '.aliaster')
FREQ_THRESHOLD = 10
SUGG_LENGTH_THRESHOLD = 4

class Aliaster(object):

  def _Load(self):
    with open(FREQ_FILE, 'r') as fd:
      cmds = fd.readlines()
    self.aliaster = {}
    for cmd in cmds:
      for cnt, alias in self._Count(cmd):
        if len(alias) < SUGG_LENGTH_THRESHOLD:
          continue
        self.aliaster[alias] = cnt + 1

  def _Count(self, cmd):
    cmd_list = shlex.split(cmd)
    while len(cmd_list):
      alias = ' '.join(cmd_list)
      yield self.aliaster.setdefault(alias, 0), alias
      cmd_list.pop()

  def _Print(self, cmd, cnt):
    return '\033[92m%d\033[0m: %s' % (cnt, cmd)

  def __str__(self, cmd=None, threshold=FREQ_THRESHOLD):
    self._Load()
    strings = []
    if cmd:
      for cnt, cmd in self._Count(cmd):
        if cnt < threshold:
          continue
        strings.append(self._Print(cmd, cnt))
    else:
      for cmd, cnt in sorted(self.aliaster.iteritems(), key=lambda t: t[1]):
        if cnt < threshold:
          continue
        strings.append(self._Print(cmd, cnt))
    return '\n'.join(strings)

  def Store(self, cmd):
    with open(FREQ_FILE, 'a') as fd:
      fd.write('%s\n' % cmd)


class Gamificalias(object):
  VAR = 'ALIASTER'

  def __init__(self):
    self.score = int(os.getenv(self.VAR, 0))

  def Winning(self, cmd, alias):
    alias = alias.partition('=')
    self.pts = len(alias[2].strip("'")) - len(alias[0])
    self.score += self.pts

  def __str__(self):
    return '\033[95mBAM! \033[92m+%d \033[93m= \033[94m%d\033[0m' % (
        self.pts, self.score)


if __name__ == '__main__':
  cmd = sys.argv[1]
  alias = sys.argv[2]
  game = Gamificalias()
  if cmd == 'aliaster':
    print Aliaster()
  elif len(alias):
    game.Winning(cmd, alias)
    print game
  else:
    Aliaster().Store(cmd)
  sys.exit(game.score)

