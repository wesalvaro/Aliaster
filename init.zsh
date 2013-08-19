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

# Tallies your usage of aliases and functions.
function tally-aliaster {
  python $DOTZSH/modules/aliaster/aliaster.py \
    $1 "`whence -w $1 | egrep -q \"function|alias\" && whence -f $1 | wc -c`"
  export ALIASTER=$?
}
add-zsh-hook preexec tally-aliaster

