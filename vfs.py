"""Виртуальная файловая система."""
import csv
from dataclasses import dataclass, field


@dataclass
class Node:
    name: str
    is_dir: bool = True
    content: str = ""
    children: dict = field(default_factory=dict)
    parent: "Node | None" = None


class VFS:
    def __init__(self, name: str = "vfs"):
        self.name = name
        self.root = Node("/")
        self.cwd = self.root

    def load_from_csv(self, filepath: str):
        """Загружает VFS из CSV-файла в память."""
        self.root = Node("/")
        self.cwd = self.root  # ВАЖНО: сбрасываем cwd на новый корень

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                path = row['path'].strip()
                node_type = row['type'].strip()
                content = row.get('content', '')

                if path == "/":
                    continue

                parts = [p for p in path.split('/') if p]
                current = self.root

                for i, part in enumerate(parts):
                    is_last = (i == len(parts) - 1)
                    if part not in current.children:
                        new_node = Node(name=part)
                        new_node.parent = current
                        current.children[part] = new_node

                    current = current.children[part]

                    if is_last:
                        current.is_dir = (node_type == 'dir')
                        current.content = content

    def resolve_path(self, path: str) -> Node | None:
        """Возвращает узел по пути (абсолютному или относительному)."""
        if not path or path == "/":
            return self.root

        if path.startswith("/"):
            current = self.root
            parts = [p for p in path.split('/') if p]
        else:
            current = self.cwd
            parts = [p for p in path.split('/') if p]

        for part in parts:
            if part == "..":
                if current.parent:
                    current = current.parent
            elif part == ".":
                continue
            elif part in current.children:
                current = current.children[part]
            else:
                return None
        return current