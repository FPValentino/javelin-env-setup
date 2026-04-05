#!/bin/bash

# ==========================================
# 🛑 JAVELIN ENVIRONMENT SETUP WARNING 🛑
# ==========================================
echo "⚠️  CRITICAL DISK SPACE WARNING ⚠️"
echo "This script will download the full historical GitBug-Java dataset."
echo "You MUST have at least 250GB of FREE SPACE on your WSL drive."
echo "If you do not have enough space, STOP NOW by pressing Ctrl+C."
echo "=========================================="
echo "Starting installation in 10 seconds..."
sleep 10

echo "🚀 Booting up Javelin Environment Installation..."

# 1. Update Linux and install core dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv git

# 2. Install pipx and poetry (the package manager)
sudo apt install -y pipx
pipx ensurepath
pipx install poetry

# 3. Clone GitBug-Java
echo "📦 Cloning GitBug-Java repository..."
cd ~
if [ ! -d "gitbug-java" ]; then
    git clone https://github.com/gitbugactions/gitbug-java.git
fi
cd gitbug-java

# 4. Permanently fix the PATH so the CLI tool works everywhere
if ! grep -q 'gitbug-java/bin' ~/.bashrc; then
    echo 'export PATH="$HOME/gitbug-java:$HOME/gitbug-java/bin:$PATH"' >> ~/.bashrc
fi
export PATH="$HOME/gitbug-java:$HOME/gitbug-java/bin:$PATH"

# 5. Initialize the Poetry environment
echo "🐍 Setting up Python environment..."
poetry self add poetry-plugin-shell
poetry install --no-root

echo "⏳ Triggering the massive Docker dataset setup..."
echo "⚠️  This will take 1.5 to 3 hours depending on your drive and internet speed."

# 6. BULLETPROOF DOWNLOAD: Pre-fetch files with auto-resume
echo "📥 Securing offline environments via wget..."
mkdir -p data
cd data
wget -c https://zenodo.org/records/10578602/files/gitbug-java_offline_environments_1.tar.gz
wget -c https://zenodo.org/records/10578617/files/gitbug-java_offline_environments_2.tar.gz
cd ..

# 7. Extract the secured files
echo "📦 Downloads locked in! Starting extraction phase..."
poetry run gitbug-java setup

# 8. Deep Clean
echo "🧹 Cleaning up temporary Docker cache to save disk space..."
# Use -n to automatically confirm clearing the cache
poetry cache clear --all pypi -n
docker builder prune -f
docker image prune -f

echo "✅ Javelin Environment Setup Complete! You are ready to extract bugs."