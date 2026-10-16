import os
import curses
from pathlib import Path

# =========================
# CONFIG
# =========================
WORKDIR = Path.home() / "storage/shared/Python"
WORKDIR.mkdir(parents=True, exist_ok=True)

OPTIONS = [
    "Run Python file",
    "Edit Python file",
    "Create file",
    "Delete file",
    "Rename file",
    "Git Push",
    "Git Status",
    "File list",
    "Terminal"
]


# =========================
# FILES
# =========================
def list_py_files():
    return sorted([
        f for f in WORKDIR.iterdir()
        if f.is_file() and f.suffix == ".py"
    ])


# =========================
# TERMINAL MODE
# =========================
def run_external(stdscr, cmd, wait=True):
    """
    Safely suspend curses, run terminal command,
    then restore curses without crashing.
    """

    # save curses state
    curses.def_prog_mode()

    # leave curses screen
    curses.endwin()

    # clean terminal
    os.system("clear")

    # run command
    os.system(cmd)

    # wait before returning
    if wait:
        input("\nPress ENTER to return...")

    # restore curses mode
    curses.reset_prog_mode()

    stdscr.refresh()
    curses.curs_set(0)

    stdscr.keypad(True)
    

# =========================
# TERMINAL
# =========================
def terminal(stdscr):
    run_external(
        stdscr,
        "bash",
        wait=False
    )

# =========================
# INPUT BOX
# =========================
def input_box(stdscr, prompt):
    curses.echo()

    stdscr.clear()

    stdscr.addstr(2, 2, prompt)

    stdscr.refresh()

    value = stdscr.getstr(3, 2).decode(errors="ignore")

    curses.noecho()

    return value.strip()


# =========================
# FILE PICKER
# =========================
def pick_file(stdscr, title):
    files = list_py_files()

    if not files:
        stdscr.clear()

        stdscr.addstr(2, 2, "No Python files found.")
        stdscr.addstr(4, 2, "Press any key...")

        stdscr.getch()

        return None

    idx = 0

    while True:
        stdscr.clear()

        h, w = stdscr.getmaxyx()

        stdscr.addstr(1, 2, title, curses.A_BOLD)

        max_visible = h - 6

        start = max(0, idx - max_visible + 1)

        visible = files[start:start + max_visible]

        for i, f in enumerate(visible):
            real_idx = start + i

            line = f.name[: w - 10]

            if real_idx == idx:
                stdscr.addstr(
                    3 + i,
                    4,
                    f"> {line}",
                    curses.A_REVERSE
                )
            else:
                stdscr.addstr(
                    3 + i,
                    4,
                    f"  {line}"
                )

        stdscr.addstr(
            h - 2,
            2,
            "↑ ↓ move | Enter select | q cancel"
        )

        key = stdscr.getch()

        if key == curses.KEY_UP:
            idx = (idx - 1) % len(files)

        elif key == curses.KEY_DOWN:
            idx = (idx + 1) % len(files)

        elif key in [10, 13]:
            return files[idx]

        elif key == ord("q"):
            return None


# =========================
# RUN PYTHON
# =========================
def run_python(stdscr):
    f = pick_file(stdscr, "Run Python file")

    if not f:
        return

    run_external(
        stdscr,
        f"python3 '{f}'"
    )


# =========================
# EDIT FILE
# =========================
def edit_python(stdscr):
    f = pick_file(stdscr, "Edit Python file")

    if not f:
        return

    run_external(
        stdscr,
        f"nvim '{f}'",
        wait=False
    )


# =========================
# CREATE FILE
# =========================
def create_file(stdscr):
    name = input_box(stdscr, "Enter file name (.py):")

    if not name:
        return

    if not name.endswith(".py"):
        name += ".py"

    path = WORKDIR / name

    stdscr.clear()

    if path.exists():
        stdscr.addstr(2, 2, "File already exists.")
    else:
        path.touch()
        stdscr.addstr(2, 2, f"Created: {name}")

    stdscr.addstr(4, 2, "Press any key...")

    stdscr.getch()


# =========================
# DELETE FILE
# =========================
def delete_file(stdscr):
    f = pick_file(stdscr, "Delete file")

    if not f:
        return

    f.unlink()

    stdscr.clear()

    stdscr.addstr(2, 2, f"Deleted: {f.name}")
    stdscr.addstr(4, 2, "Press any key...")

    stdscr.getch()


# =========================
# RENAME FILE
# =========================
def rename_file(stdscr):
    f = pick_file(stdscr, "Rename file")

    if not f:
        return

    new = input_box(stdscr, "New name (.py):")

    if not new:
        return

    if not new.endswith(".py"):
        new += ".py"

    target = WORKDIR / new

    stdscr.clear()

    if target.exists():
        stdscr.addstr(2, 2, "File already exists.")
    else:
        f.rename(target)
        stdscr.addstr(2, 2, f"Renamed to: {new}")

    stdscr.addstr(4, 2, "Press any key...")

    stdscr.getch()


# =========================
# GIT PUSH
# =========================
def git_push(stdscr):
    run_external(
        stdscr,
        (
            f"cd '{WORKDIR}' && "
            f"git add . && "
            f"git commit -m 'update' && "
            f"git push"
        )
    )


# =========================
# GIT STATUS
# =========================
def git_status(stdscr):
    run_external(
        stdscr,
        f"cd '{WORKDIR}' && git status"
    )


# =========================
# FILE LIST
# =========================
def file_list(stdscr):
    files = list_py_files()

    stdscr.clear()

    h, w = stdscr.getmaxyx()

    stdscr.addstr(
        1,
        2,
        "FILES:",
        curses.A_BOLD
    )

    if not files:
        stdscr.addstr(3, 2, "No Python files.")

    else:
        max_show = h - 6

        for i, f in enumerate(files[:max_show]):
            stdscr.addstr(
                3 + i,
                2,
                f.name[: w - 4]
            )

    stdscr.addstr(h - 2, 2, "Press any key...")

    stdscr.getch()


# =========================
# MAIN MENU
# =========================
def main(stdscr):
    curses.curs_set(0)

    stdscr.keypad(True)

    idx = 0

    while True:
        stdscr.clear()

        h, w = stdscr.getmaxyx()

        stdscr.addstr(
            1,
            2,
            "PYTHON IDE",
            curses.A_BOLD
        )

        for i, opt in enumerate(OPTIONS):
            line = opt[: w - 10]

            if i == idx:
                stdscr.addstr(
                    3 + i,
                    4,
                    f"> {line}",
                    curses.A_REVERSE
                )
            else:
                stdscr.addstr(
                    3 + i,
                    4,
                    f"  {line}"
                )

        stdscr.addstr(
            h - 2,
            2,
            "↑ ↓ move | Enter select"
        )

        key = stdscr.getch()

        if key == curses.KEY_UP:
            idx = (idx - 1) % len(OPTIONS)

        elif key == curses.KEY_DOWN:
            idx = (idx + 1) % len(OPTIONS)

        elif key in [10, 13]:
            choice = OPTIONS[idx]

            if choice == "Run Python file":
                run_python(stdscr)

            elif choice == "Edit Python file":
                edit_python(stdscr)

            elif choice == "Create file":
                create_file(stdscr)

            elif choice == "Delete file":
                delete_file(stdscr)

            elif choice == "Rename file":
                rename_file(stdscr)

            elif choice == "Git Push":
                git_push(stdscr)

            elif choice == "Git Status":
                git_status(stdscr)

            elif choice == "File list":
                file_list(stdscr)

            elif choice == "Terminal":
                terminal(stdscr)


# =========================
# START
# =========================
if __name__ == "__main__":
    os.system("clear")

    stdscr = curses.initscr()

    curses.noecho()
    curses.cbreak()

    try:
        main(stdscr)

    finally:
        try:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
        except:
            pass

        os.system("clear")
