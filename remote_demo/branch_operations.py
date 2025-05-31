#!/usr/bin/env python3
"""
Git Branch Operations Example
This script demonstrates Git branching and merging operations using Python.
"""

import subprocess
import sys
from pathlib import Path
import time

class GitBranchManager:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.ensure_repo_exists()

    def run_command(self, command, error_msg=None):
        """Execute a Git command and return the output"""
        try:
            result = subprocess.run(command, cwd=self.repo_path, 
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            if error_msg:
                print(f"{error_msg}: {e.stderr}")
            else:
                print(f"Error executing command: {e.stderr}")
            return None

    def ensure_repo_exists(self):
        """Ensure we're in a Git repository"""
        if not self.repo_path.exists():
            self.repo_path.mkdir(parents=True)
        if not (self.repo_path / ".git").exists():
            self.run_command(["git", "init"], "Failed to initialize repository")

    def create_branch(self, branch_name):
        """Create and switch to a new branch"""
        print(f"\nCreating branch: {branch_name}")
        result = self.run_command(["git", "checkout", "-b", branch_name],
                                f"Failed to create branch {branch_name}")
        return result is not None

    def switch_branch(self, branch_name):
        """Switch to an existing branch"""
        print(f"\nSwitching to branch: {branch_name}")
        result = self.run_command(["git", "checkout", branch_name],
                                f"Failed to switch to branch {branch_name}")
        return result is not None

    def create_file(self, filename, content):
        """Create a file with specified content"""
        file_path = self.repo_path / filename
        file_path.write_text(content)
        return file_path.exists()

    def commit_changes(self, message):
        """Stage and commit changes"""
        self.run_command(["git", "add", "."], "Failed to stage changes")
        result = self.run_command(["git", "commit", "-m", message],
                                "Failed to commit changes")
        return result is not None

    def merge_branch(self, source_branch):
        """Merge source branch into current branch"""
        print(f"\nMerging {source_branch} into current branch")
        result = self.run_command(["git", "merge", source_branch],
                                f"Failed to merge {source_branch}")
        return result is not None

    def show_branch_status(self):
        """Show current branch and status"""
        print("\nCurrent branch status:")
        self.run_command(["git", "branch"], "Failed to show branches")
        self.run_command(["git", "status"], "Failed to show status")

def demonstrate_branching():
    """Demonstrate Git branching operations"""
    manager = GitBranchManager("branch_demo")

    # Create main branch content
    print("\nCreating main branch content...")
    manager.create_file("main.txt", "Main branch content")
    manager.commit_changes("Initial commit on main")

    # Create and work on feature branch
    manager.create_branch("feature")
    manager.create_file("feature.txt", "Feature branch content")
    manager.commit_changes("Add feature")

    # Switch back to main and create parallel changes
    manager.switch_branch("main")
    manager.create_file("parallel.txt", "Parallel main branch work")
    manager.commit_changes("Parallel work on main")

    # Merge feature into main
    manager.merge_branch("feature")
    
    # Show final status
    manager.show_branch_status()

if __name__ == "__main__":
    demonstrate_branching() 