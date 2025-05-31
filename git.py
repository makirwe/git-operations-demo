from pathlib import Path
import subprocess
import sys
import os

class GitOperationError(Exception):
    """Custom exception for Git operation failures"""
    pass

def run_git_command(command, cwd, error_message="Git operation failed"):
    """
    Safely execute a git command with proper error handling
    
    Args:
        command (list): Git command as a list of strings
        cwd (Path): Working directory for the command
        error_message (str): Custom error message for failures
    
    Returns:
        subprocess.CompletedProcess: Result of the command if successful
        
    Raises:
        GitOperationError: If the command fails
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        raise GitOperationError(f"{error_message}: {e.stderr}")
    except FileNotFoundError:
        raise GitOperationError("Git executable not found. Please install Git.")

def safe_git_operations(project_path):
    """
    Perform Git operations safely with error handling
    
    Args:
        project_path (Path): Path to the project directory
    """
    try:
        # Ensure directory exists
        if not project_path.exists():
            print(f"Creating directory: {project_path}")
            project_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize git repository
        print("\nInitializing Git repository...")
        run_git_command(["git", "init"], project_path)
        
        # Create a sample file
        sample_file = project_path / "sample.txt"
        sample_file.write_text("Hello, Git!")
        
        # Check status
        print("\nChecking repository status...")
        status_result = run_git_command(["git", "status"], project_path)
        print(status_result.stdout)
        
        # Add files to staging
        print("\nAdding files to staging...")
        run_git_command(["git", "add", "."], project_path)
        
        # Configure git user (if not already configured)
        try:
            run_git_command(["git", "config", "user.email", "example@example.com"], project_path)
            run_git_command(["git", "config", "user.name", "Example User"], project_path)
        except GitOperationError:
            print("Warning: Could not configure Git user. Commits may fail.")
        
        # Commit changes
        print("\nCommitting changes...")
        run_git_command(
            ["git", "commit", "-m", "Initial commit"],
            project_path
        )
        
        # Show commit log
        print("\nShowing commit log...")
        log_result = run_git_command(["git", "log", "--oneline"], project_path)
        print(log_result.stdout)
        
    except GitOperationError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    else:
        print("\nAll Git operations completed successfully!")
        return True

if __name__ == "__main__":
    # Use the current directory as the project directory
    project_dir = Path.cwd()
    
    print(f"Starting Git operations in: {project_dir}")
    success = safe_git_operations(project_dir)
    
    sys.exit(0 if success else 1)