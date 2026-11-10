"""File tools that can only touch one folder. Limits are enforced here, in code, not by
asking the model nicely."""

import os


class ToolError(Exception):
    pass


class Workspace:
    MAX_WRITE_BYTES = 10_000
    ALLOWED_SUFFIXES = (".txt", ".md")

    def __init__(self, root):
        self.root = os.path.realpath(root)

    def _path(self, name):
        if not isinstance(name, str) or not name:
            raise ToolError("a file name is required")
        path = os.path.realpath(os.path.join(self.root, name))
        if os.path.dirname(path) != self.root:
            raise ToolError(f"{name!r} is outside the workspace folder")  # also blocks sub-folders
        if not path.endswith(self.ALLOWED_SUFFIXES):
            raise ToolError("only .txt and .md files may be used")
        return path

    def list_files(self):
        return "\n".join(sorted(os.listdir(self.root)))

    def read_file(self, name):
        path = self._path(name)
        if not os.path.exists(path):
            raise ToolError(f"{name!r} does not exist")
        with open(path, encoding="utf-8") as f:
            return f.read(5000)

    def write_file(self, name, text):
        path = self._path(name)
        if len(text.encode()) > self.MAX_WRITE_BYTES:
            raise ToolError("text is too long")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return f"wrote {len(text)} characters to {name}"

    def delete_file(self, name):
        path = self._path(name)
        if not os.path.exists(path):
            raise ToolError(f"{name!r} does not exist")
        os.remove(path)
        return f"deleted {name}"


# risky tools change or remove data, so a person must approve each call
TOOLS = {
    "list_files": {"args": [], "risky": False},
    "read_file": {"args": ["name"], "risky": False},
    "write_file": {"args": ["name", "text"], "risky": True},
    "delete_file": {"args": ["name"], "risky": True},
}
