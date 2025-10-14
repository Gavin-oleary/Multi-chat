import os
import shutil
import sys
import subprocess

print("🧹 Clearing Python cache...")

# Get the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))

# Clear all __pycache__ directories
cache_cleared = 0
for root, dirs, files in os.walk(backend_dir):
    if '__pycache__' in dirs:
        cache_path = os.path.join(root, '__pycache__')
        try:
            shutil.rmtree(cache_path)
            cache_cleared += 1
        except Exception as e:
            print(f"Could not remove {cache_path}: {e}")

# Clear all .pyc files
pyc_cleared = 0
for root, dirs, files in os.walk(backend_dir):
    for file in files:
        if file.endswith('.pyc'):
            try:
                os.remove(os.path.join(root, file))
                pyc_cleared += 1
            except Exception as e:
                print(f"Could not remove {file}: {e}")

print(f"✅ Cleared {cache_cleared} __pycache__ directories and {pyc_cleared} .pyc files")

# Force Python to reimport modules
if 'app' in sys.modules:
    print("🔄 Clearing app module from sys.modules...")
    modules_to_remove = [key for key in sys.modules.keys() if key.startswith('app')]
    for module in modules_to_remove:
        del sys.modules[module]

print("🚀 Starting FastAPI server with fresh imports...")
subprocess.run([sys.executable, "-m", "app.main"])
