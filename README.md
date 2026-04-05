# 🎯 Javelin Environment Setup (GitBug-Java)

Welcome to the backend setup for the Javelin IntelliJ Extension. This repository contains the automated scripts needed to download and configure the GitBug-Java dataset (130GB+) so we can extract historical bugs and test our Ochiai-MS fault localization implementation.

## ⚠️ Prerequisites (READ FIRST)
Before running anything, your machine **must** have the following installed. You also need at least **250GB of free space** on the drive where your WSL virtual machine is installed.

1. **[WSL 2 & Ubuntu](https://learn.microsoft.com/en-us/windows/wsl/install):** Open a Windows PowerShell as Administrator and run: `wsl --install`. Ensure you are using Ubuntu as your default distribution.
2. **[Docker Desktop](https://www.docker.com/products/docker-desktop/):**
   Download and install Docker Desktop for Windows. 
   * **Crucial:** Go to Docker Settings > Resources > WSL Integration, and ensure integration is turned ON for your Ubuntu distro. Docker must be running in the background before you start the installation.

---

## 🚀 Step 1: Automated Installation (REPLACE [YOUR_USERNAME] WITH GITHUB USERNAME!)

1. Open your Ubuntu terminal.
2. Download the setup script:
   ```bash
   wget [https://raw.githubusercontent.com/](https://raw.githubusercontent.com/)[YOUR_USERNAME]/javelin-env-setup/main/setup_javelin.sh
   ```
3. Run the installer:
   ```bash
   bash setup_javelin.sh
   ```
*Note: This script uses an auto-resume feature. If your internet drops, simply press the UP arrow and run `bash setup_javelin.sh` again. It will resume exactly where it left off.*

---

## 🐛 Step 2: Extracting Bugs for Javelin

Once the setup is complete, you can use our interactive Python tool to pull specific bugs for testing in our IntelliJ Sandbox.

1. Navigate to the GitBug-Java folder:
   ```bash
   cd ~/gitbug-java
   ```
2. Download the Javelin target selector script:
   ```bash
   wget [https://raw.githubusercontent.com/](https://raw.githubusercontent.com/)[YOUR_USERNAME]/javelin-env-setup/main/extract_bugs.py
   ```
3. Install the UI dependency:
   ```bash
   poetry run pip install questionary
   ```
4. Launch the extractor!
   ```bash
   poetry run python extract_bugs.py
   ```

The script will ask you which project and bugs you want. It will automatically create a `~/javelin-workspaces` folder and extract both the buggy and fixed versions of the code there.