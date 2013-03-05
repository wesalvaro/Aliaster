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
  python /usr/local/google/home/wesalvaro/third_party/Aliaster/aliaster.py \
    $1 "`alias $1`" "`type $1 | grep function > /dev/null && which $1 | wc -c`"
  export ALIASTER=$?
}
add-zsh-hook preexec tally-aliaster

