# #!/usr/bin/env python3
# import os
# import subprocess
# import re

# VERSION_FILE = 'version.py'

# def get_last_commit_msg():
#     return subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode().strip()

# def get_last_commit_hash():
#     return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()

# def read_current_version():
#     if not os.path.exists(VERSION_FILE):
#         return 0, 0, 0
#     with open(VERSION_FILE, 'r') as f:
#         match = re.search(r'version = "(\d+)\.(\d+)\.(\d+)"', f.read())
#         if match:
#             return map(int, match.groups())
#         else:
#             return 0, 0, 0

# def write_version_file(major, minor, patch, comment, commit_hash):
#     with open(VERSION_FILE, 'w') as f:
#         f.write(f'''# This file is created by the pre-push script
# class Version:
#     comment = "{comment}"
#     hash = "{commit_hash}"
#     version = "{major}.{minor}.{patch}"

# if __name__ == "__main__":
#     print(Version.version)
# ''')

# def main():
#     major, minor, patch = read_current_version()
#     patch += 1
#     comment = get_last_commit_msg()
#     commit_hash = get_last_commit_hash()
#     write_version_file(major, minor, patch, comment, commit_hash)
#     subprocess.call(['git', 'add', VERSION_FILE])

# if __name__ == "__main__":
#     main()


#!/usr/bin/env python3
import os
import subprocess
import re

VERSION_FILE = 'version.py'

def get_last_commit_msg():
    return subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode().strip()

def get_last_commit_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()

def read_current_version():
    if not os.path.exists(VERSION_FILE):
        return 1, 0, 0, 0  # Start from v1.0.0.0 if file doesn't exist
    with open(VERSION_FILE, 'r') as f:
        content = f.read()
        match = re.search(r'version = "v(\d+)\.(\d+)\.(\d+)\.(\d+)"', content)
        if match:
            return map(int, match.groups())
        else:
            return 1, 0, 0, 0  # fallback default

def write_version_file(major, minor, patch, build, comment, commit_hash):
    with open(VERSION_FILE, 'w') as f:
        f.write(f'''# This file is created by the version bump script
class Version:
    comment = "{comment}"
    hash = "{commit_hash}"
    version = "v{major}.{minor}.{patch}.{build}"

if __name__ == "__main__":
    print(Version.version)
''')

def main():
    major, minor, patch, build = read_current_version()
    comment = get_last_commit_msg()
    commit_hash = get_last_commit_hash()

    # Check commit message for version bump keyword
    if '#major' in comment:
        major += 1
        minor, patch, build = 0, 0, 0
    elif '#minor' in comment:
        minor += 1
        patch, build = 0, 0
    elif '#patch' in comment:
        patch += 1
        build = 0
    else:
        build += 1  # default bump

    write_version_file(major, minor, patch, build, comment, commit_hash)
    subprocess.call(['git', 'add', VERSION_FILE])

if __name__ == "__main__":
    main()
