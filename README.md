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

1. Open your Ubuntu terminal.
2. Download the setup script:
   ```bash
   wget [https://raw.githubusercontent.com/FPValentino/javelin-env-setup/main/setup_javelin.sh](https://raw.githubusercontent.com/FPValentino/javelin-env-setup/main/setup_javelin.sh)
   ```
3. Run the installer:
   ```bash
   bash setup_javelin.sh
   ```
*Note: The large dataset downloads use auto-resume (`wget -c`). If your internet drops during the download phase, re-run `bash setup_javelin.sh` and `wget` will resume where it left off. Earlier steps (apt installs, git clone) will safely re-run without issue.*

---

## 🐛 Step 2: Extracting Bugs for Javelin

Once the setup is complete, you can pull bugs into your `~/javelin-workspaces` folder for testing. The interactive script automatically enforces strict naming conventions and safely pulls both the buggy and fixed versions.

1. Navigate to the GitBug-Java framework folder:
   ```bash
   cd ~/gitbug-java
   ```
2. Download the interactive target selector script:
   ```bash
   wget [https://raw.githubusercontent.com/FPValentino/javelin-env-setup/main/extract.py](https://raw.githubusercontent.com/FPValentino/javelin-env-setup/main/extract.py)
   ```
3. Install the UI dependency and run the script:
   ```bash
   poetry run pip install questionary
   poetry run python extract.py
   ```
*The script will ask you which project and bugs you want. It will automatically create a `~/javelin-workspaces` folder and extract both the buggy and fixed versions of the code there.*

---

## 🔨 Step 3: Compiling the Bug (Required for JaCoCo)

Javelin’s JaCoCo engine relies on Java Bytecode to track test coverage. Because of this, it cannot read raw `.java` files. You **must** compile the extracted bug before Javelin can analyze it.

1. Navigate to the newly extracted **buggy** folder (replace `BUG-ID` with the actual folder name):
   ```bash
   cd ~/javelin-workspaces/BUG-ID-buggy
   ```
2. Compile the project and its tests using Maven:
   ```bash
   mvn clean compile test-compile
   ```
*Wait until you see a **BUILD SUCCESS** message. If the build fails, the project may require a specific Java version (e.g., Java 8 vs Java 21).*

---

## 🎯 Step 4: Running Javelin (Data Generation)

Now that the code is compiled into `.class` files, you can fire the Javelin engine to generate the fault localization rankings.

1. Open the `javelin-cli` source code in **IntelliJ IDEA**.
2. Edit your **Run Configuration** arguments to point directly to the compiled workspace in WSL. 
   
   *Example arguments for the **Ochiai-MS** algorithm:*
   ```text
   run --args="-a ochiai-ms -t /home/paul/javelin-workspaces/BUG-ID-buggy/target/classes -T /home/paul/javelin-workspaces/BUG-ID-buggy/target/test-classes -s /home/paul/javelin-workspaces/BUG-ID-buggy/src/main/java -o /home/paul/javelin-workspaces/BUG-ID-buggy/BUG-ID.csv"
   ```
3. Click **Run**. Once finished, Javelin will generate your `.csv` ranking file directly inside the workspace folder.

---

## 📊 Step 5: The Evaluation Pipeline (Grading)

Once Javelin generates the `.csv` ranking file, the data generation phase is officially complete! 

To calculate the EXAM Score and Top-N accuracy against the "Fixed" ground truth, you must move your data to the evaluation pipeline.

1. Using Windows File Explorer, navigate to your WSL directory (`\\wsl.localhost\Ubuntu\home\paul\javelin-workspaces\`).
2. Copy your newly generated `.csv` file.
3. Head over to the dedicated Evaluation Repository for the final grading steps:
   
   👉 **[Javelin Evaluation Pipeline Repository](https://github.com/FPValentino/javelin-evaluation-pipeline)**

Follow the `README.md` instructions in that repository to place your data, run the Python scripts (`generate_patches.py`, `build_ground_truth.py`, etc.), and calculate your final thesis results!
