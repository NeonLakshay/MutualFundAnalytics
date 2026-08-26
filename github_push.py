import subprocess
import sys


def run_command(command, description):
    """Run a Git command and stop if it fails."""
    print(f"\n🔹 {description}")
    print(f"   > {' '.join(command)}")

    result = subprocess.run(
        command,
        text=True,
        capture_output=True
    )

    if result.stdout:
        print(result.stdout.strip())

    if result.returncode != 0:
        if result.stderr:
            print(f"\n❌ Error:\n{result.stderr.strip()}")
        sys.exit(result.returncode)

    return result.stdout.strip()


def main():
    print("\n🚀 MUTUAL FUND ANALYTICS — GIT AUTO PUSH")
    print("=" * 55)

    # 1. Check current Git status
    status = run_command(
        ["git", "status", "--short"],
        "Checking changed files..."
    )

    if not status:
        print("\n✅ No changes detected.")
        print("Nothing needs to be committed or pushed.")
        return

    print("\n📁 Files that will be included:")
    print(status)

    # 2. Ask for confirmation
    confirm = input(
        "\n⚠️  Stage ALL changes and push them to GitHub? (y/n): "
    ).strip().lower()

    if confirm not in ("y", "yes"):
        print("\n⛔ Operation cancelled.")
        return

    # 3. Stage everything
    run_command(
        ["git", "add", "."],
        "Staging all changes..."
    )

    # 4. Verify staged changes
    run_command(
        ["git", "status", "--short"],
        "Verifying staged changes..."
    )

    # 5. Ask for commit message
    commit_message = input(
        "\n📝 Enter commit message [default: Update project]: " #put ->Final project update
    ).strip()

    if not commit_message:
        commit_message = "Update project"

    # 6. Commit
    run_command(
        ["git", "commit", "-m", commit_message],
        "Creating commit..."
    )

    # 7. Push
    run_command(
        ["git", "push", "origin", "main"],
        "Pushing changes to GitHub..."
    )

    print("\n" + "=" * 55)
    print("🎉 SUCCESS!")
    print("✅ Changes committed")
    print("✅ Changes pushed to GitHub")
    print("=" * 55)


if __name__ == "__main__":
    main()
