import subprocess
import os
import questionary
import sys

def run_command(command):
    """Runs a shell command and returns the output as a list of lines."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return [line.strip() for line in result.stdout.split('\n') if line.strip()]

def main():
    print("🎯 Javelin Target Selector")
    
    # 1. Ensure workspace exists
    workspace_dir = os.path.expanduser("~/javelin-workspaces")
    os.makedirs(workspace_dir, exist_ok=True)

    # 2. Fetch all available projects (Using poetry run)
    print("Fetching available projects...")
    projects = run_command("poetry run gitbug-java pids")
    
    if not projects:
        print("Error: Could not find projects. Are you running this via 'poetry run python extract_bugs.py'?")
        sys.exit(1)

    # 3. UI: Select a Project
    selected_project = questionary.select(
        "Which project do you want to extract bugs from?",
        choices=projects
    ).ask()

    if not selected_project:
        sys.exit(0)

    # 4. Fetch bugs for the selected project (Using poetry run and correct formatting)
    print(f"Fetching bugs for {selected_project}...")
    bugs = run_command(f"poetry run gitbug-java bids {selected_project}")

    if not bugs:
        print(f"No bugs found for {selected_project}.")
        sys.exit(1)

    # 5. UI: Multi-select Bugs
    selected_bugs = questionary.checkbox(
        "Select the bugs you want to extract for Javelin (Space to select, Enter to confirm):",
        choices=bugs
    ).ask()

    if not selected_bugs:
        print("No bugs selected. Exiting.")
        sys.exit(0)

    # 6. Extraction Loop
    for bug_id in selected_bugs:
        print(f"\n🚀 Extracting {bug_id}...")
        
        buggy_path = os.path.join(workspace_dir, f"{bug_id}-buggy")
        fixed_path = os.path.join(workspace_dir, f"{bug_id}-fixed")

        # Checkout Buggy Version (Using poetry run)
        print(f"   -> Pulling historical buggy environment...")
        os.system(f"poetry run gitbug-java checkout {bug_id} {buggy_path}")
        
        # Checkout Fixed Version (Using poetry run)
        print(f"   -> Pulling developer-fixed environment...")
        os.system(f"poetry run gitbug-java checkout {bug_id} {fixed_path} --fixed")

    print(f"\n✅ All selected bugs have been extracted to {workspace_dir}")
    print("Happy bug hunting!")

if __name__ == "__main__":
    main()