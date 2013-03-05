#
# Aliaster : https://github.com/wesalvaro/Aliaster
#
# Gamifies aliasing commands.
#
# Authors:
#   Wes Alvaro <hello@wesalvaro.com>
#

# Don't override precmd/preexec; append to hook array.
autoload -Uz add-zsh-hook

# Sets the tab and window titles before command execution.
function tally-aliaster {
  python /path/to/aliaster.py \
    $1 "`whence -w $1 | egrep -q \"function|alias\" && whence -f $1 | wc -c`"
  export ALIASTER=$?
}
add-zsh-hook preexec tally-aliaster

