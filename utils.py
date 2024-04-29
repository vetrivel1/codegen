import os


def safe_write(path, code):
    path = "./software/" + path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w+') as f:
        f.write(code)

# create safe_read function
def safe_read(path):
    path = "./software/" + path
    with open(path, 'r') as f:
        return f.read()