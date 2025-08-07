import os
import sys

def parse_manifest(manifest_path):
    base_dir = os.path.dirname(os.path.abspath(manifest_path))

    with open(manifest_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    path_stack = []
    prev_level = 0

    for lineno, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        indent_spaces = len(line) - len(line.lstrip())
        if indent_spaces % 2 != 0:
            raise ValueError(f"❌ Line {lineno}: Indentation must be multiples of 2 spaces.\n→ {line.rstrip()}")

        level = indent_spaces // 2
        entry = line.strip()

        while len(path_stack) > level:
            path_stack.pop()

        current_path = os.path.join(base_dir, *path_stack)

        if entry.startswith("R:"):
            folder_name = entry[2:].strip()
            full_path = os.path.join(current_path, folder_name)
            os.makedirs(full_path, exist_ok=True)
            path_stack.append(folder_name)
            print(f"[DIR ] {full_path}")
        elif entry.startswith("F:"):
            file_name = entry[2:].strip()
            full_path = os.path.join(current_path, file_name)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            open(full_path, 'w').close()
            print(f"[FILE] {full_path}")
        else:
            raise ValueError(f"❌ Line {lineno}: Must start with 'R:' or 'F:'\n→ {line.rstrip()}")

    print("\n✅ Structure created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Tree_generator.py path/to/structure.txt")
        sys.exit(1)

    manifest_file = sys.argv[1]
    if not os.path.isfile(manifest_file):
        print("❌ Manifest file not found.")
        sys.exit(1)

    parse_manifest(manifest_file)