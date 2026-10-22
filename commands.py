"""Команды эмулятора."""
from vfs import VFS


class CommandError(Exception):
    """Ошибка выполнения команды."""
    pass


def cmd_ls(vfs: VFS, args: list[str]) -> str:
    path = args[0] if args else "."
    node = vfs.resolve_path(path)
    
    if not node:
        raise CommandError(f"ls: {path}: No such file or directory")
    if not node.is_dir:
        return node.name
        
    items = sorted(node.children.keys())
    return "  ".join(items) if items else ""


def cmd_cd(vfs: VFS, args: list[str]) -> str:
    if len(args) != 1:
        raise CommandError("cd: неверное число аргументов")
    
    path = args[0]
    node = vfs.resolve_path(path)
    
    if not node:
        raise CommandError(f"cd: {path}: No such file or directory")
    if not node.is_dir:
        raise CommandError(f"cd: {path}: Not a directory")
        
    vfs.cwd = node
    return ""


def cmd_cat(vfs: VFS, args: list[str]) -> str:
    if not args:
        raise CommandError("cat: не указан файл")
    path = args[0]
    node = vfs.resolve_path(path)
    if not node:
        raise CommandError(f"cat: {path}: No such file or directory")
    if node.is_dir:
        raise CommandError(f"cat: {path}: Is a directory")
    return node.content


def cmd_whoami(vfs: VFS, args: list[str]) -> str:
    if args:
        raise CommandError("whoami: неверное число аргументов")
    return "root"


def cmd_uname(vfs: VFS, args: list[str]) -> str:
    if args:
        raise CommandError("uname: неверное число аргументов")
    return "VFS-Emulator"


def cmd_rmdir(vfs: VFS, args: list[str]) -> str:
    if len(args) != 1:
        raise CommandError("rmdir: неверное число аргументов")
    
    path = args[0]
    if path == "/":
        raise CommandError("rmdir: cannot remove '/': Permission denied")
        
    node = vfs.resolve_path(path)
    if not node:
        raise CommandError(f"rmdir: {path}: No such file or directory")
    if not node.is_dir:
        raise CommandError(f"rmdir: {path}: Not a directory")
    if node.children:
        raise CommandError(f"rmdir: {path}: Directory not empty")
        
    if node.parent:
        del node.parent.children[node.name]
    
    return ""