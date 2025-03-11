import os

def add_init_files(root_dir):
    for dirpath, dirnames, _ in os.walk(root_dir):
        init_file = os.path.join(dirpath, "__init__.py")
        if not os.path.exists(init_file):  # Avoid overwriting existing files
            with open(init_file, "w") as f:
                pass  # Create an empty file
            print(f"Added: {init_file}")

# Set your root directory here
root_directory = "W:\BPU\Gdiist-BPU-Toolkit/bpusdk"

add_init_files(root_directory)
