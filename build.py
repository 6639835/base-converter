#!/usr/bin/env python3
"""
Build script for creating cross-platform executables using PyInstaller.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def get_platform_info():
    """Get platform-specific information."""
    system = platform.system().lower()
    architecture = platform.machine().lower()
    
    if architecture == 'x86_64':
        architecture = 'amd64'
    elif architecture == 'aarch64' or architecture == 'arm64':
        architecture = 'arm64'
    elif architecture.startswith('arm'):
        architecture = 'arm'
    
    return system, architecture


def clean_build_dirs():
    """Clean build and dist directories."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name} directory")


def create_spec_file():
    """Create PyInstaller spec file with proper configuration."""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# Determine the appropriate name for the executable
exe_name = 'base-converter'
if sys.platform.startswith('win'):
    exe_name += '.exe'

a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('src/*.py', 'src'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox', 
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'argparse',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
'''
    
    with open('base-converter.spec', 'w') as f:
        f.write(spec_content.strip())
    print("Created PyInstaller spec file")


def build_executable():
    """Build the executable using PyInstaller."""
    system, arch = get_platform_info()
    
    print(f"Building for {system}-{arch}...")
    
    # Create spec file
    create_spec_file()
    
    # Build command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        'base-converter.spec'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(result.stdout)
        
        # Rename output file to include platform info
        exe_name = 'base-converter'
        if system == 'windows':
            exe_name += '.exe'
            
        dist_path = Path('dist')
        original_exe = dist_path / exe_name
        platform_exe = dist_path / f'base-converter-{system}-{arch}{".exe" if system == "windows" else ""}'
        
        if original_exe.exists():
            if platform_exe.exists():
                platform_exe.unlink()
            original_exe.rename(platform_exe)
            print(f"Created: {platform_exe}")
            
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def create_installer_script():
    """Create installer script for different platforms."""
    system, arch = get_platform_info()
    
    if system == 'windows':
        create_windows_installer()
    elif system == 'darwin':
        create_macos_installer()
    else:
        create_linux_installer()


def create_windows_installer():
    """Create Windows installer script."""
    installer_content = '''
@echo off
echo Installing Base Converter...

REM Create installation directory
set INSTALL_DIR=%PROGRAMFILES%\\BaseConverter
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
copy base-converter-windows-*.exe "%INSTALL_DIR%\\base-converter.exe"

REM Add to PATH (requires admin privileges)
setx PATH "%PATH%;%INSTALL_DIR%" /M

echo Base Converter installed successfully!
echo You can now use 'base-converter' command from any command prompt.
pause
'''
    
    with open('install-windows.bat', 'w') as f:
        f.write(installer_content.strip())
    print("Created Windows installer script")


def create_macos_installer():
    """Create macOS installer script."""
    installer_content = '''#!/bin/bash
echo "Installing Base Converter..."

# Create installation directory
INSTALL_DIR="/usr/local/bin"
sudo mkdir -p "$INSTALL_DIR"

# Copy executable
sudo cp base-converter-darwin-* "$INSTALL_DIR/base-converter"
sudo chmod +x "$INSTALL_DIR/base-converter"

echo "Base Converter installed successfully!"
echo "You can now use 'base-converter' command from any terminal."
'''
    
    with open('install-macos.sh', 'w') as f:
        f.write(installer_content.strip())
    os.chmod('install-macos.sh', 0o755)
    print("Created macOS installer script")


def create_linux_installer():
    """Create Linux installer script."""
    installer_content = '''#!/bin/bash
echo "Installing Base Converter..."

# Create installation directory
INSTALL_DIR="/usr/local/bin"
sudo mkdir -p "$INSTALL_DIR"

# Copy executable
sudo cp base-converter-linux-* "$INSTALL_DIR/base-converter"
sudo chmod +x "$INSTALL_DIR/base-converter"

# Create desktop entry (optional)
DESKTOP_FILE="$HOME/.local/share/applications/base-converter.desktop"
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=Base Converter
Comment=A comprehensive base conversion utility
Exec=base-converter --gui
Icon=accessories-calculator
Terminal=false
Type=Application
Categories=Utility;Calculator;
EOF

echo "Base Converter installed successfully!"
echo "You can now use 'base-converter' command from any terminal."
echo "A desktop entry has been created for GUI access."
'''
    
    with open('install-linux.sh', 'w') as f:
        f.write(installer_content.strip())
    os.chmod('install-linux.sh', 0o755)
    print("Created Linux installer script")


def create_package_info():
    """Create package information file."""
    system, arch = get_platform_info()
    
    info_content = f'''Base Converter v1.0
Platform: {system}-{arch}
Build Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

INSTALLATION:
Run the appropriate installer script for your platform:
- Windows: install-windows.bat (run as administrator)
- macOS: ./install-macos.sh
- Linux: ./install-linux.sh

MANUAL INSTALLATION:
Copy the executable to a directory in your PATH.

USAGE:
base-converter --gui          # Launch graphical interface
base-converter 1010 -f 2 -t 10  # Convert binary to decimal
base-converter --help         # Show help

For more information, visit:
https://github.com/6639835/base-converter
'''
    
    with open('PACKAGE_INFO.txt', 'w') as f:
        f.write(info_content.strip())
    print("Created package information file")


def test_executable():
    """Test the built executable."""
    system, arch = get_platform_info()
    exe_name = f'base-converter-{system}-{arch}'
    if system == 'windows':
        exe_name += '.exe'
        
    exe_path = Path('dist') / exe_name
    
    if not exe_path.exists():
        print(f"Executable not found: {exe_path}")
        return False
        
    try:
        # Test basic functionality
        result = subprocess.run([str(exe_path), '--list-bases'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and 'Binary' in result.stdout:
            print("Executable test passed!")
            return True
        else:
            print(f"Executable test failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("Executable test timed out")
        return False
    except Exception as e:
        print(f"Error testing executable: {e}")
        return False


def main():
    """Main build function."""
    print("Base Converter Build Script")
    print("=" * 40)
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executable
    if not build_executable():
        print("Build failed!")
        sys.exit(1)
    
    # Test executable
    if not test_executable():
        print("Warning: Executable test failed, but build completed")
    
    # Create installer scripts
    create_installer_script()
    create_package_info()
    
    print("\nBuild completed successfully!")
    print("\nFiles created:")
    print(f"- dist/base-converter-{get_platform_info()[0]}-{get_platform_info()[1]}")
    print("- Installer script")
    print("- PACKAGE_INFO.txt")
    
    print("\nTo create a release package:")
    print("1. Test the executable thoroughly")
    print("2. Create a zip/tar.gz archive with the executable and installer")
    print("3. Upload to GitHub Releases")


if __name__ == '__main__':
    main()
