#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias pokefastfetch="pokeget bulbasaur --hide-name | fastfetch --file-raw -"
alias comp_phys="conda activate && cd Documents/homework/phys2415 && jupyter notebook"
PS1='[\u@\h \W]\$ '

eval "$(starship init $(basename $SHELL))"
eval "fastfetch"

# >>> juliaup initialize >>>

# !! Contents within this block are managed by juliaup !!

case ":$PATH:" in
    *:/home/aagowl/.juliaup/bin:*)
        ;;

    *)
        export PATH=/home/aagowl/.juliaup/bin${PATH:+:${PATH}}
        ;;
esac

# <<< juliaup initialize <<<

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/aagowl/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/aagowl/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/aagowl/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/aagowl/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

alias config='/usr/bin/git --git-dir=/home/aagowl/.dotfiles/ --work-tree=/home/aagowl'
