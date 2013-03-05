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

"""
import os
import shlex
import sys

FREQ_FILE = os.path.join(os.getenv('HOME'), '.aliaster')
FREQ_THRESHOLD = 10
SUGG_LENGTH_THRESHOLD = 4


class Aliaster(object):

  def _Load(self):
    self.aliaster = {}
    for cmd in self._LoadCmds():
      self._LoadCounts(cmd)

  def _LoadCmds(self):
    with open(FREQ_FILE, 'r') as fd:
      lines = fd.readlines()
    cmd = ''
    while lines:
      cmd += lines.pop()
      try:
        cmd_list = shlex.split(cmd.strip())
      except ValueError:
        continue  # We probably just need another line.
      else:
        yield cmd_list
        cmd = ''

  def _LoadCounts(self, cmd):
    while cmd:
      alias = ' '.join(cmd).strip()
      if len(alias) < SUGG_LENGTH_THRESHOLD:
        break
      self.aliaster[alias] = self.aliaster.get(alias, 0) + 1
      cmd.pop()

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
    self.points = 0
    self.score = int(os.getenv(self.VAR, 0))

  def Winning(self, cmd, expanded_cnt):
    points = expanded_cnt - len(cmd) - 1
    self.points += points
    self.score += self.points

  def __str__(self):
    return '\033[95mBAM! \033[92m+%d \033[93m= \033[94m%d\033[0m' % (
        self.points, self.score)


def main(_, cmd, expanded_cnt):
  expanded_cnt = int(expanded_cnt or 0)
  game = Gamificalias()
  if cmd == 'aliaster':
    print Aliaster()
  elif expanded_cnt:
    game.Winning(cmd, expanded_cnt)
    print game
  else:
    Aliaster().Store(cmd)
  sys.exit(game.score)


if __name__ == '__main__':
  main(*sys.argv)

