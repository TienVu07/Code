CODE HUB (Termux)

Folder structure:
Code/
  start-menu.sh
  menu.py
  menu.js
  Python/src/          <- menu.py manages .py files here
  Python/projects/     <- Python projects
  JavaScript/src/      <- menu.js manages .js files here
  JavaScript/projects/ <- JavaScript projects

Manual start:
  bash ~/storage/shared/Code/start-menu.sh

To show CODE HUB automatically when opening Termux, append this block to ~/.bashrc:

  # CODE HUB startup menu
  if [[ $- == *i* && -z "${CODE_TERMINAL:-}" && -f "$HOME/storage/shared/Code/start-menu.sh" ]]; then
    bash "$HOME/storage/shared/Code/start-menu.sh"
  fi

If you already have a ~/.bashrc, append the block rather than replacing the file.
