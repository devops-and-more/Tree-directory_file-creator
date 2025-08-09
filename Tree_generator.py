import os
import sys
import shutil

INDENT_SIZE = 2

def parse_manifest(manifest_path):
    base_dir = os.path.dirname(os.path.abspath(manifest_path))

    with open(manifest_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    path_stack = []
    root_name = None
    expected_dirs = set()
    expected_files = set()

    # Step 1: Parse manifest & build expected sets
    for lineno, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        indent_spaces = len(line) - len(line.lstrip())
        if indent_spaces % INDENT_SIZE != 0:
            raise ValueError(f"❌ Line {lineno}: Indentation must be multiples of {INDENT_SIZE} spaces.\n→ {line.rstrip()}")

        level = indent_spaces // INDENT_SIZE
        entry = line.strip()

        while len(path_stack) > level:
            path_stack.pop()

        if entry.startswith("R:"):
            folder_name = entry[2:].strip()
            if level == 0:
                root_name = folder_name
                path_stack[:] = [root_name]
            else:
                path_stack.append(folder_name)
            rel_dir = os.path.join(*path_stack[1:]) if len(path_stack) > 1 else ""
            expected_dirs.add(rel_dir)
        elif entry.startswith("F:"):
            file_name = entry[2:].strip()
            rel_file = os.path.join(*(path_stack[1:] + [file_name]))
            expected_files.add(rel_file)
        else:
            raise ValueError(f"❌ Line {lineno}: Must start with 'R:' or 'F:'\n→ {line.rstrip()}")

    if root_name is None:
        raise ValueError("❌ No root folder found in manifest.")

    root_dir = os.path.join(base_dir, root_name)
    os.makedirs(root_dir, exist_ok=True)

    # Ensure all parent dirs for files are in expected_dirs
    for f in list(expected_files):
        parent = os.path.dirname(f)
        while parent and parent not in expected_dirs:
            expected_dirs.add(parent)
            parent = os.path.dirname(parent)

    # Step 2: Delete unexpected files
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        rel_dir = os.path.relpath(dirpath, root_dir)
        if rel_dir == ".":
            rel_dir = ""
        for fn in filenames:
            rel_file = os.path.join(rel_dir, fn) if rel_dir else fn
            if rel_file not in expected_files:
                abs_file = os.path.join(dirpath, fn)
                os.remove(abs_file)
                print(f"[DEL FILE] {abs_file}")
        for d in dirnames:
            rel_subdir = os.path.join(rel_dir, d) if rel_dir else d
            if rel_subdir not in expected_dirs:
                abs_subdir = os.path.join(dirpath, d)
                shutil.rmtree(abs_subdir)
                print(f"[DEL DIR ] {abs_subdir}")

    # Step 3: Create missing directories
    for rel_dir in sorted(expected_dirs, key=lambda d: d.count(os.sep)):
        if rel_dir:
            abs_dir = os.path.join(root_dir, rel_dir)
            if not os.path.isdir(abs_dir):
                os.makedirs(abs_dir, exist_ok=True)
                print(f"[ADD DIR ] {abs_dir}")

    # Step 4: Create missing files
    for rel_file in sorted(expected_files, key=lambda f: f.count(os.sep)):
        abs_file = os.path.join(root_dir, rel_file)
        os.makedirs(os.path.dirname(abs_file), exist_ok=True)
        if not os.path.exists(abs_file):
            open(abs_file, 'w').close()
            print(f"[ADD FILE] {abs_file}")

    print("\n✅ Structure synchronized with manifest. Extras deleted.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Tree_generator.py path/to/structure.txt")
        sys.exit(1)

    manifest_file = sys.argv[1]
    if not os.path.isfile(manifest_file):
        print("❌ Manifest file not found.")
        sys.exit(1)

    parse_manifest(manifest_file)
