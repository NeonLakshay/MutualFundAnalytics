import subprocess
import sys


def main():
    command = [
        r".\venv\Scripts\python.exe",
        "-m",
        "streamlit",
        "run",
        r"dashboard/app.py",
    ]

    print("🚀 Starting Mutual Fund Analytics Dashboard...")
    print("   Running:", " ".join(command))
    print()

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("❌ Could not find .\\venv\\Scripts\\python.exe")
        print("Make sure you are running this script from the project root.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit exited with code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
