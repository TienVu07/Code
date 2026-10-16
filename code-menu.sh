#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="$HOME/storage/shared/Code"
clear_screen() { printf '\033[2J\033[H\033[3J'; }
printf '\033[?25l'
trap 'printf "\033[?25l"' EXIT

while true; do
  clear_screen
  cols=$(tput cols)
  rows=$(tput lines)

  options=("JavaScript" "Python" "Terminal")
  selected=0
  choice=""
  top=$(( (rows - 6) / 2 ))
  (( top < 1 )) && top=1

  while true; do
    clear_screen
    title="CODE"
    printf '\033[%d;%dH\033[1;36m%s\033[0m' \
      "$top" "$(( (cols - ${#title}) / 2 + 1 ))" "$title"

    for i in "${!options[@]}"; do
      text="${options[$i]}"
      width=$((${#text} + 2))
      left=$(( (cols - width) / 2 + 1 ))
      (( left < 1 )) && left=1

      printf '\033[%d;%dH' "$((top + i + 2))" "$left"
      if (( i == selected )); then
        printf '\033[7m> %s\033[0m' "$text"
      else
        printf '  %s' "$text"
      fi
    done

    IFS= read -rsn1 key || exit 0

    if [[ "$key" == $'\x1b' ]]; then
      rest=""
      read -rsn2 -t 0.2 rest || true
      case "$rest" in
        '[A') key=up ;;
        '[B') key=down ;;
        *) key="" ;;
      esac
    elif [[ -z "$key" ]]; then
      choice="${options[$selected]}"
      break
    fi

    case "$key" in
      up|k) selected=$(( (selected + ${#options[@]} - 1) % ${#options[@]} )) ;;
      down|j) selected=$(( (selected + 1) % ${#options[@]} )) ;;
      q) choice="Exit"; break ;;
    esac
  done

  case "$choice" in
    JavaScript)
      clear_screen
      node "$ROOT/menu.js"
      printf '\033[?25l'
      ;;
    Python)
      clear_screen
      python "$ROOT/menu.py"
      printf '\033[?25l'
      ;;
    Terminal)
      printf '\033[?25h'
      stty sane
      clear
      CODE_TERMINAL=1 bash -i
      printf '\033[?25l'
      ;;
    Exit)
      clear_screen
      exit 0
      ;;
  esac
done
