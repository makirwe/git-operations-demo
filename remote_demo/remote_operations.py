#!/usr/bin/env python3
"""
Git Remote Operations Example
This script demonstrates remote repository operations using Python.
"""

import subprocess
import sys
from pathlib import Path
import os

class GitRemoteManager:
    def __init__(self, local_path):
        self.repo_path = Path(local_path)
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
        """Ensure the repository exists and is initialized"""
        if not self.repo_path.exists():
            self.repo_path.mkdir(parents=True)
        if not (self.repo_path / ".git").exists():
            self.run_command(["git", "init"])
            print(f"Initialized new Git repository in {self.repo_path}")

    def clone_repository(self, remote_url, branch=None):
        """Clone a remote repository"""
        if self.repo_path.exists() and any(self.repo_path.iterdir()):
            print(f"Directory {self.repo_path} is not empty")
            return False

        cmd = ["git", "clone"]
        if branch:
            cmd.extend(["-b", branch])
        cmd.extend([remote_url, str(self.repo_path)])

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Successfully cloned {remote_url}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone repository: {e.stderr}")
            return False

    def add_remote(self, name, url):
        """Add a new remote"""
        result = self.run_command(["git", "remote", "add", name, url],
                                f"Failed to add remote {name}")
        if result is not None:
            print(f"Added remote {name}: {url}")
            return True
        return False

    def list_remotes(self):
        """List all configured remotes"""
        print("\nConfigured remotes:")
        self.run_command(["git", "remote", "-v"])

    def push_to_remote(self, remote="origin", branch="master"):
        """Push changes to remote repository"""
        print(f"\nPushing to {remote}/{branch}")
        result = self.run_command(["git", "push", "-u", remote, branch],
                                "Failed to push changes")
        return result is not None

    def pull_from_remote(self, remote="origin", branch="master"):
        """Pull changes from remote repository"""
        print(f"\nPulling from {remote}/{branch}")
        result = self.run_command(["git", "pull", remote, branch],
                                "Failed to pull changes")
        return result is not None

    def list_remote_branches(self):
        """List all remote branches"""
        print("\nRemote branches:")
        self.run_command(["git", "branch", "-r"])

    def create_and_track_branch(self, branch_name, remote="origin"):
        """Create and track a remote branch"""
        cmd = ["git", "checkout", "-b", branch_name, f"{remote}/{branch_name}"]
        result = self.run_command(cmd, f"Failed to track branch {branch_name}")
        if result is not None:
            print(f"Created and tracking branch {branch_name}")
            return True
        return False

def demonstrate_remote_operations():
    """Demonstrate Git remote operations"""
    # Initialize remote manager
    remote_manager = GitRemoteManager("remote_ops_demo")

    # Add a remote repository
    remote_url = "https://github.com/makirwe/git-operations-demo.git"
    remote_manager.add_remote("origin", remote_url)
    
    # List configured remotes
    remote_manager.list_remotes()

    # Create a new file
    test_file = remote_manager.repo_path / "remote_test.txt"
    test_file.write_text("Testing remote operations")
    
    # Commit changes
    remote_manager.run_command(["git", "add", "."])
    remote_manager.run_command(["git", "commit", "-m", "Add remote test file"])

    # Push changes to remote
    remote_manager.push_to_remote()

    # List remote branches
    remote_manager.list_remote_branches()

    # Pull latest changes
    remote_manager.pull_from_remote()

if __name__ == "__main__":
    demonstrate_remote_operations() 