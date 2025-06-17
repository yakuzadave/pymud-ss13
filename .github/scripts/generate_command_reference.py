import ast
from pathlib import Path


def extract_commands(commands_dir: Path):
    for file in sorted(commands_dir.glob('*.py')):
        text = file.read_text()
        tree = ast.parse(text)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Call) and getattr(dec.func, 'id', '') == 'register':
                        if dec.args and isinstance(dec.args[0], ast.Constant):
                            name = dec.args[0].value
                            doc = ast.get_docstring(node) or ''
                            first_line = doc.strip().splitlines()[0] if doc else ''
                            yield name, first_line


def build_table(commands):
    lines = ['# Command Reference', '', '| Command | Description |', '|---------|-------------|']
    for name, desc in commands:
        lines.append(f'| `{name}` | {desc or ""} |')
    lines.append('')
    return '\n'.join(lines)


def main() -> None:
    commands_dir = Path('commands')
    if not commands_dir.is_dir():
        print('No commands directory found')
        return
    commands = list(extract_commands(commands_dir))
    output = build_table(commands)
    Path('docs/commands_reference.md').write_text(output)
    print('Command reference generated')


if __name__ == '__main__':
    main()
