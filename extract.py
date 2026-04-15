import subprocess
import os
import sys
import questionary

def run_poetry_command(cmd, cwd):
    """Runs a command securely inside the gitbug-java directory."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"❌ Error executing: {cmd}")
        print(result.stderr)
        return False
    return True

def run_command(command):
    """Runs a shell command and returns the output as a list of lines."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return [line.strip() for line in result.stdout.split('\n') if line.strip()]

def main():
    print("🎯 Javelin Target Selector (Interactive Mode)")
    
    # 1. Setup paths
    gitbug_dir = os.path.expanduser("~/gitbug-java")
    workspace_dir = os.path.expanduser("~/javelin-workspaces")
    os.makedirs(workspace_dir, exist_ok=True)

    if not os.path.exists(os.path.join(gitbug_dir, "poetry.lock")):
        print(f"Error: Could not find GitBug-Java at {gitbug_dir}.")
        sys.exit(1)

    # 2. UI: Select a Project
    print("Fetching available projects...")
    projects = run_command("poetry run gitbug-java pids")
    
    if not projects:
        print("Error: Could not find projects.")
        sys.exit(1)

    selected_project = questionary.select(
        "Which project do you want to extract bugs from?",
        choices=projects
    ).ask()

    if not selected_project:
        sys.exit(0)

    # 3. UI: Select Bugs from that Project
    print(f"Fetching bugs for {selected_project}...")
    bugs = run_command(f"poetry run gitbug-java bids {selected_project}")

    if not bugs:
        print(f"No bugs found for {selected_project}.")
        sys.exit(1)

    selected_bugs = questionary.checkbox(
        "Select the bugs you want to extract (Space to select, Enter to confirm):",
        choices=bugs
    ).ask()

    if not selected_bugs:
        print("No bugs selected. Exiting.")
        sys.exit(0)

    # 4. The Bulletproof Extraction Engine
    print(f"\n🚀 Starting safe extraction for {len(selected_bugs)} bugs...")
    success_count = 0
    
    for bug_id in selected_bugs:
        print(f"\n📦 Processing {bug_id}...")
        
        buggy_path = os.path.join(workspace_dir, f"{bug_id}-buggy")
        fixed_path = os.path.join(workspace_dir, f"{bug_id}-fixed")

        # Step A: Safe Buggy Extraction
        if not os.path.exists(buggy_path):
            print(f"   -> Pulling buggy environment...")
            cmd_buggy = f"poetry run gitbug-java checkout {bug_id} {buggy_path}"
            if not run_poetry_command(cmd_buggy, gitbug_dir):
                continue
        else:
            print(f"   -> Buggy folder exists. Skipping.")

        # Step B: Safe Fixed Extraction (Forces the --fixed flag!)
        if not os.path.exists(fixed_path):
            print(f"   -> Pulling developer-fixed environment...")
            cmd_fixed = f"poetry run gitbug-java checkout {bug_id} {fixed_path} --fixed"
            if not run_poetry_command(cmd_fixed, gitbug_dir):
                continue
        else:
            print(f"   -> Fixed folder exists. Skipping.")
            
        success_count += 1

    print(f"\n✅ All done! Successfully extracted {success_count}/{len(selected_bugs)} bugs to {workspace_dir}")
    print("\n========================================================")
    print("NEXT STEPS:")
    print("1. Compile the buggy project:")
    print("   cd ~/javelin-workspaces/YOUR-BUG-ID-buggy")
    print("   mvn clean compile test-compile")
    print("2. Run Javelin in IntelliJ to generate your .csv ranking.")
    print("3. Move the .csv to Windows and run your Python Evaluation Pipeline!")
    print("========================================================\n")

if __name__ == "__main__":
    main()
