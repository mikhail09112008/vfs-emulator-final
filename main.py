"""Эмулятор оболочки ОС с VFS. Вариант №21. Этап 5."""
import argparse
import tkinter as tk
from tkinter import scrolledtext

from commands import (
    CommandError,
    cmd_cat,
    cmd_cd,
    cmd_ls,
    cmd_rmdir,
    cmd_uname,
    cmd_whoami,
)
from parser import parse
from vfs import VFS


class EmulatorGUI:
    def __init__(self, vfs: VFS, script_path: str | None = None):
        self.vfs = vfs
        self.script_path = script_path
        
        self.root = tk.Tk()
        self.root.title(f"VFS: {vfs.name}")
        self.root.iconname(f"VFS: {vfs.name}")
        self.root.geometry("800x500")

        self.output = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 11), height=20
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=4, pady=(4, 0))

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.entry_var, font=("Consolas", 11), width=50)
        self.entry.pack(fill=tk.X, side=tk.BOTTOM, padx=4, pady=4)
        self.entry.bind("<Return>", self.on_enter)
        
        self.entry.focus_set()
        self.root.focus_force()  # Принудительный фокус на окно при запуске

        self.print_line(f"VFS '{vfs.name}' загружена. Введите 'exit' для выхода.")

        if self.script_path:
            self.root.after(500, self.run_script)

    def print_line(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def prompt(self) -> str:
        return f"{self.vfs.name}:~$ "

    def on_enter(self, event=None):
        line = self.entry_var.get()
        self.entry_var.set("")
        self.print_line(self.prompt() + line)
        self.execute(line)

    def execute(self, line: str) -> bool:
        if not line.strip():
            return True
        try:
            tokens = parse(line)
        except ValueError as e:
            self.print_line(f"Ошибка: {e}")
            return False

        if not tokens:
            return True

        cmd, args = tokens[0], tokens[1:]
        try:
            if cmd == "exit":
                self.root.destroy()
                return False
            elif cmd == "ls":
                self.print_line(cmd_ls(self.vfs, args))
            elif cmd == "cd":
                self.print_line(cmd_cd(self.vfs, args))
            elif cmd == "cat":
                self.print_line(cmd_cat(self.vfs, args))
            elif cmd == "whoami":
                self.print_line(cmd_whoami(self.vfs, args))
            elif cmd == "uname":
                self.print_line(cmd_uname(self.vfs, args))
            elif cmd == "rmdir":
                self.print_line(cmd_rmdir(self.vfs, args))
            elif cmd == "echo":
                self.print_line(" ".join(args))
            else:
                raise CommandError(f"{cmd}: команда не найдена")
        except CommandError as e:
            self.print_line(f"Ошибка: {e}")
            return False
        return True

    def run_script(self):
        self.print_line(f"--- Запуск скрипта: {self.script_path} ---")
        try:
            with open(self.script_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    self.print_line(self.prompt() + line)
                    if not self.execute(line):
                        self.print_line("--- Скрипт остановлен из-за ошибки ---")
                        return
            self.print_line("--- Скрипт успешно завершен ---")
        except FileNotFoundError:
            self.print_line(f"Ошибка: файл скрипта '{self.script_path}' не найден")

    def run(self):
        self.root.mainloop()


def main():
    parser = argparse.ArgumentParser(description="Эмулятор оболочки ОС с VFS")
    parser.add_argument("--vfs", type=str, help="Путь к CSV-файлу VFS")
    parser.add_argument("--script", type=str, help="Путь к стартовому скрипту")
    args = parser.parse_args()

    print(f"DEBUG: Запуск эмулятора")
    print(f"DEBUG: VFS path = {args.vfs}")
    print(f"DEBUG: Script path = {args.script}")

    vfs_name = args.vfs.split('/')[-1].replace('.csv', '') if args.vfs else "vfs"
    vfs = VFS(name=vfs_name)
    
    if args.vfs:
        try:
            vfs.load_from_csv(args.vfs)
            print(f"DEBUG: VFS успешно загружена из {args.vfs}")
        except FileNotFoundError:
            print(f"ОШИБКА: Файл {args.vfs} не найден!")
            return
        except Exception as e:
            print(f"ОШИБКА при загрузке VFS: {e}")
            return

    app = EmulatorGUI(vfs, script_path=args.script)
    app.run()


if __name__ == "__main__":
    main()