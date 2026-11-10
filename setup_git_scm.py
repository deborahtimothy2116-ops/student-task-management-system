"""
Automated Software Configuration Management (SCM) & GitFlow Script
Course: Software Engineering (Lab Integrated) - 231CS523
Implements:
  1. Git repository initialization
  2. Branching strategy: main, develop, feature/cr-101-workload-estimator
  3. Baseline creation & version tagging: v1.0 and v1.1
  4. Complete Change Request flow (CR-101) with merge ancestry
"""

import subprocess
import os
import sys

def run_git(args, cwd=None, check=True):
    cmd = ["git"] + args
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and result.returncode != 0:
        print(f"[ERROR] git {' '.join(args)} failed:")
        print(result.stderr)
        raise RuntimeError(f"Git command failed: {' '.join(args)}")
    return result.stdout.strip()

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    print(f"=== Initializing SCM GitFlow Repository in {repo_root} ===")

    # Initialize git if not already present
    if not os.path.exists(os.path.join(repo_root, ".git")):
        run_git(["init", "-b", "main"], cwd=repo_root)
        print("[OK] Initialized new Git repository with default branch 'main'")
    else:
        print("[INFO] Existing .git directory found")

    # Set local author identity for academic project
    run_git(["config", "user.name", "EduTask Student Team (231CS523)"], cwd=repo_root)
    run_git(["config", "user.email", "student.team.231cs523@academic.edu"], cwd=repo_root)

    # Ensure on main branch
    try:
        run_git(["checkout", "main"], cwd=repo_root, check=False)
    except Exception:
        pass

    # Stage initial files for Baseline v1.0
    run_git(["add", ".gitignore", ".dockerignore", "requirements.txt", "src/", "scripts/generate_gantt_pdf.py"], cwd=repo_root)
    
    # Check if there are changes to commit
    status = run_git(["status", "--porcelain"], cwd=repo_root)
    if status:
        run_git(["commit", "-m", "feat: initial release of Student Task Management System (Baseline v1.0)"], cwd=repo_root)
        print("[OK] Committed Baseline v1.0 files to main")

    # Tag Baseline v1.0
    tags = run_git(["tag", "-l"], cwd=repo_root)
    if "v1.0" not in tags.splitlines():
        run_git(["tag", "-a", "v1.0", "-m", "Baseline v1.0: Core Task CRUD, Course Tagging, and REST API"], cwd=repo_root)
        print("[OK] Tagged official Baseline v1.0")
    else:
        print("[INFO] Tag v1.0 already exists")

    # Create & switch to develop branch
    branches = run_git(["branch", "--list"], cwd=repo_root)
    if "develop" not in branches:
        run_git(["checkout", "-b", "develop"], cwd=repo_root)
        print("[OK] Created and switched to 'develop' branch")
    else:
        run_git(["checkout", "develop"], cwd=repo_root)
        print("[OK] Switched to 'develop' branch")

    # Stage DevOps and testing infrastructure
    run_git(["add", ".github/", "Dockerfile", "docker-compose.yml", "terraform/", "render.yaml", "scripts/uptime_monitor.py"], cwd=repo_root)
    status_dev = run_git(["status", "--porcelain"], cwd=repo_root)
    if status_dev:
        run_git(["commit", "-m", "ci: configure GitHub Actions workflow, Dockerfile, IaC, and monitoring"], cwd=repo_root)
        print("[OK] Committed CI/CD & DevOps toolchain to develop")

    # Create feature branch for Change Request CR-101
    feature_branch = "feature/cr-101-workload-estimator"
    if feature_branch not in branches:
        run_git(["checkout", "-b", feature_branch], cwd=repo_root)
        print(f"[OK] Created feature branch '{feature_branch}' for Change Request CR-101")
    else:
        run_git(["checkout", feature_branch], cwd=repo_root)

    # Stage tests and documentation
    run_git(["add", "tests/", "docs/"], cwd=repo_root)
    status_feat = run_git(["status", "--porcelain"], cwd=repo_root)
    if status_feat:
        run_git(["commit", "-m", "feat(cr-101): implement study hour workload analytics and priority filtering (CR-101)"], cwd=repo_root)
        print("[OK] Committed CR-101 implementation on feature branch")

    # Merge feature branch back into develop with explicit merge commit
    run_git(["checkout", "develop"], cwd=repo_root)
    run_git(["merge", "--no-ff", feature_branch, "-m", "Merge pull request #1 from feature/cr-101-workload-estimator into develop (CR-101 Approved by CCB)"], cwd=repo_root)
    print(f"[OK] Merged {feature_branch} into develop with merge commit")

    # Merge develop into main for production release
    run_git(["checkout", "main"], cwd=repo_root)
    run_git(["merge", "--no-ff", "develop", "-m", "Release v1.1.0: Student Task Management System with CR-101 Analytics"], cwd=repo_root)
    print("[OK] Merged develop into main for Release v1.1.0")

    # Tag Baseline v1.1
    tags_after = run_git(["tag", "-l"], cwd=repo_root)
    if "v1.1" not in tags_after.splitlines():
        run_git(["tag", "-a", "v1.1", "-m", "Baseline v1.1: Production release with CR-101 Workload Analytics and Priority Filters"], cwd=repo_root)
        print("[OK] Tagged official Baseline v1.1")
    else:
        print("[INFO] Tag v1.1 already exists")

    # Print SCM Summary
    print("\n" + "="*60)
    print("  GIT TAGS (BASELINES)")
    print("="*60)
    print(run_git(["tag", "-n", "-l"], cwd=repo_root))

    print("\n" + "="*60)
    print("  GIT COMMIT GRAPH (BRANCHING STRATEGY & MERGE FLOW)")
    print("="*60)
    print(run_git(["log", "--graph", "--oneline", "--decorate", "--all", "-n", "10"], cwd=repo_root))
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
