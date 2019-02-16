#! /bin/bash

(tmux new-window -n "w=0.1" './Imitate 5 2 12000 10000 0.1; zsh -i')&
(tmux new-window -n "w=0.3" './Imitate 5 2 12000 10000 0.3; zsh -i')&
(tmux new-window -n "w=0.5" './Imitate 5 2 12000 10000 0.5; zsh -i')&
(tmux new-window -n "w=0.7" './Imitate 5 2 12000 10000 0.7; zsh -i')&
(tmux new-window -n "w=0.9" './Imitate 5 2 12000 10000 0.9; zsh -i')&
