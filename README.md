# 🎯 Javelin Environment Setup (GitBug-Java)

Welcome to the backend setup for the Javelin IntelliJ Extension. This repository contains the automated scripts needed to download and configure the GitBug-Java dataset (130GB+) so we can extract historical bugs and test our Ochiai-MS fault localization implementation.

## ⚠️ Prerequisites (READ FIRST)
Before running anything, your machine **must** have the following installed. You also need at least **250GB of free space** on the drive where your WSL virtual machine is installed.

https://www.youtube.com/watch?v=5Mfe54238xE - Pwede niyo panoorin to for installation ng Docker - Then proceed kayo sa * **Crucial** part.

1. **[WSL 2 & Ubuntu](https://learn.microsoft.com/en-us/windows/wsl/install):** Open a Windows PowerShell as Administrator and run: `wsl --install`. Ensure you are using Ubuntu as your default distribution.
2. **[Docker Desktop](https://www.docker.com/products/docker-desktop/):**
   Download and install Docker Desktop for Windows. 
   * **Crucial:** Go to Docker Settings > Resources > WSL Integration, and ensure integration is turned ON for your Ubuntu distro. Docker must be running in the background before you start the installation.

---

## 🚀 Step 1: Automated Installation

*Note: Please REPLACE `[YOUR_USERNAME]` in the links below with the actual GitHub username hosting this repository!*

1. Open your Ubuntu terminal.
2. Download the setup script:
   ```bash
   wget https://raw.githubusercontent.com/[YOUR_USERNAME]/javelin-env-setup/main/setup_javelin.sh
   ```
3. Run the installer:
   ```bash
   bash setup_javelin.sh
   ```
*Note: The large dataset downloads use auto-resume (`wget -c`). If your internet drops during the download phase, re-run `bash setup_javelin.sh` and `wget` will resume where it left off. Earlier steps (apt installs, git clone) will safely re-run without issue.*

---

## 🐛 Step 2: Extracting Bugs for Javelin

Once the setup is complete, you have two ways to pull bugs into your `~/javelin-workspaces` folder for testing. Both scripts automatically enforce strict naming conventions and safely apply the `--fixed` flag for you.

<<<<<<< HEAD
First, navigate to the GitBug-Java framework folder:
```bash
cd ~/gitbug-java
```

### Option A: Interactive Mode (Select specific bugs)
Use this if you want a visual menu to browse projects and select individual bugs to download.

1. Download the script and install the UI dependency:
=======
1. Navigate to the GitBug-Java folder:
   ```bash
   cd ~/gitbug-java
   ```
2. Download the Javelin target selector script:
   ```bash
   wget https://raw.githubusercontent.com/[YOUR_USERNAME]/javelin-env-setup/main/extract_bugs.py
   ```
3. Install the UI dependency:
>>>>>>> 82abfe8d79033de3327560939f2cb6b8999c65ac
   ```bash
   wget [https://raw.githubusercontent.com/](https://raw.githubusercontent.com/)[YOUR_USERNAME]/javelin-env-setup/main/extract.py
   poetry run pip install questionary
   ```
2. Launch the extractor:
   ```bash
   poetry run python extract.py
   ```
<<<<<<< HEAD
---
**Next Steps for the Evaluation Team:** Once the bugs are extracted, move over to the `javelin-evaluation-pipeline` repository and run `generate_patches.py` to build the ground truth!
=======

The script will ask you which project and bugs you want. It will automatically create a `~/javelin-workspaces` folder and extract both the buggy and fixed versions of the code there.
>>>>>>> 82abfe8d79033de3327560939f2cb6b8999c65ac
