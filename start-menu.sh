#!/data/data/com.termux/files/usr/bin/bash
# Main launcher for Code tools
set -u
ROOT="$HOME/storage/shared/Code"

clear_screen() { printf '\033[2J\033[H'; }

while true; do
  clear_screen
  printf '\033[1;36mCODE HUB\033[0m\n\n'
  options=("JavaScript" "Python" "Terminal" "Exit")
  selected=0
  while true; do
    for i in "${!options[@]}"; do
      if (( i == selected )); then
        printf '  \033[7m> %s\033[0m\n' "${options[$i]}"
      else
        printf '    %s\n' "${options[$i]}"
      fi
    done
    printf '\n\033[2m↑/↓ or j/k: move | Enter: select | q: exit\033[0m\n'
    IFS= read -rsn1 key || exit 0
    if [[ "$key" == $'\x1b' ]]; then
      read -rsn2 rest || true
      case "$rest" in '[A') key=up ;; '[B') key=down ;; *) key= ;; esac
    elif [[ "$key" == "" ]]; then
      choice="${options[$selected]}"
      break
    fi
    case "$key" in
      up|k) selected=$(( (selected + ${#options[@]} - 1) % ${#options[@]} )) ;;
      down|j) selected=$(( (selected + 1) % ${#options[@]} )) ;;
      q) choice="Exit"; break ;;
    esac
    # Redraw list cleanly after each key
    clear_screen
    printf '\033[1;36mCODE HUB\033[0m\n\n'
  done

  case "$choice" in
    JavaScript)
      clear_screen
      node "$ROOT/menu.js"
      ;;
    Python)
      clear_screen
      python "$ROOT/menu.py"
      ;;
    Terminal)
      clear_screen
      export CODE_TERMINAL=1
      bash --rcfile "$HOME/.bashrc"
      ;;
    Exit)
      clear_screen
      exit 0
      ;;
  esac
  printf '\nPress any key to return to CODE HUB...'
  IFS= read -rsn1 _ || true
done
