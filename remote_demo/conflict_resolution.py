#!/usr/bin/env python3
"""
Git Merge Conflict Resolution Example
This script demonstrates how to handle merge conflicts in Git using Python.
"""

import subprocess
import sys
from pathlib import Path

class GitConflictResolver:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.setup_repository()

    def run_command(self, command):
        """Execute a Git command and return the output"""
        try:
            result = subprocess.run(command, cwd=self.repo_path,
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {e.stderr}")
            return None

    def setup_repository(self):
        """Set up a new repository for conflict demonstration"""
        if not self.repo_path.exists():
            self.repo_path.mkdir(parents=True)
        
        if not (self.repo_path / ".git").exists():
            self.run_command(["git", "init"])
            print("Initialized new Git repository")

    def create_file(self, filename, content):
        """Create or update a file with given content"""
        file_path = self.repo_path / filename
        file_path.write_text(content)
        print(f"Created/Updated {filename}")

    def commit_changes(self, message):
        """Stage and commit changes"""
        self.run_command(["git", "add", "."])
        result = self.run_command(["git", "commit", "-m", message])
        if result:
            print(f"Committed changes: {message}")
        return result is not None

    def create_branch(self, branch_name):
        """Create and switch to a new branch"""
        result = self.run_command(["git", "checkout", "-b", branch_name])
        if result:
            print(f"Created and switched to branch: {branch_name}")
        return result is not None

    def switch_branch(self, branch_name):
        """Switch to an existing branch"""
        result = self.run_command(["git", "checkout", branch_name])
        if result:
            print(f"Switched to branch: {branch_name}")
        return result is not None

    def merge_branch(self, branch_name):
        """Attempt to merge a branch and handle conflicts"""
        result = self.run_command(["git", "merge", branch_name])
        if result:
            print(f"Successfully merged {branch_name}")
            return True
        else:
            print(f"Merge conflict detected with {branch_name}")
            return False

    def resolve_conflict(self, filename, resolution):
        """Resolve a merge conflict in a file"""
        self.create_file(filename, resolution)
        self.run_command(["git", "add", filename])
        self.commit_changes("Resolve merge conflict")
        print(f"Resolved conflict in {filename}")

def demonstrate_conflict_resolution():
    """Demonstrate Git merge conflict resolution"""
    resolver = GitConflictResolver("conflict_demo")

    # Create initial file
    print("\nCreating initial file...")
    resolver.create_file("shared.txt", "Initial content")
    resolver.commit_changes("Initial commit")

    # Create feature branch
    resolver.create_branch("feature")
    resolver.create_file("shared.txt", "Feature branch changes")
    resolver.commit_changes("Feature branch modifications")

    # Switch back to main and make conflicting changes
    resolver.switch_branch("main")
    resolver.create_file("shared.txt", "Main branch changes")
    resolver.commit_changes("Main branch modifications")

    # Try to merge feature branch
    print("\nAttempting to merge feature branch...")
    if not resolver.merge_branch("feature"):
        # Resolve conflict
        resolution = """Resolved content:
Main branch changes
+
Feature branch changes"""
        resolver.resolve_conflict("shared.txt", resolution)
        print("Conflict resolved successfully!")

if __name__ == "__main__":
    demonstrate_conflict_resolution() 