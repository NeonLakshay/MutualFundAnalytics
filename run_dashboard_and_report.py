import subprocess
import time
import sys


def main():
    python_exe = r".\venv\Scripts\python.exe"
    dashboard_file = r"dashboard\app.py"
    email_file = r"dashboard\email_report.py"

    print("\n" + "=" * 65)
    print("🚀 MUTUAL FUND ANALYTICS AUTOMATION")
    print("=" * 65)

    # ---------------------------------------------------------
    # STEP 1: Start Streamlit dashboard
    # ---------------------------------------------------------
    print("\n🌐 Starting dashboard/app.py ...")

    try:
        dashboard_process = subprocess.Popen(
            [
                python_exe,
                "-m",
                "streamlit",
                "run",
                dashboard_file,
            ]
        )
    except FileNotFoundError:
        print("\n❌ Could not find the virtual-environment Python.")
        print("Make sure you are running this script from the project root.")
        sys.exit(1)

    # ---------------------------------------------------------
    # STEP 2: 60-second countdown
    # ---------------------------------------------------------
    print("\n⏳ Dashboard is running.")
    print("📊 Email report will start after 60 seconds.\n")

    try:
        for remaining in range(60, 0, -1):

            # Check whether dashboard has crashed/stopped
            if dashboard_process.poll() is not None:
                print("\n❌ Dashboard stopped unexpectedly.")
                sys.exit(1)

            print(
                f"\r⏱️  Starting email report in {remaining:02d} seconds...",
                end="",
                flush=True
            )

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Stopping automation...")

        # Stop dashboard when YOU press Ctrl+C
        dashboard_process.terminate()

        try:
            dashboard_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            dashboard_process.kill()

        print("✅ Dashboard stopped.")
        sys.exit(0)

    # ---------------------------------------------------------
    # STEP 3: Start email_report.py
    # ---------------------------------------------------------
    print("\n\n📧 60 seconds completed.")
    print("📨 Starting dashboard/email_report.py ...")
    print("-" * 65)

    try:
        subprocess.run(
            [
                python_exe,
                email_file,
            ],
            check=True
        )

        print("-" * 65)
        print("✅ Email report completed successfully.")

    except subprocess.CalledProcessError as e:
        print("-" * 65)
        print(f"❌ Email report failed with exit code {e.returncode}")

    # ---------------------------------------------------------
    # STEP 4: Keep dashboard alive
    # ---------------------------------------------------------
    print("\n" + "=" * 65)
    print("✅ DASHBOARD IS STILL RUNNING")
    print("📊 You can continue using the Streamlit application.")
    print("🛑 Press Ctrl+C in this terminal when you want to stop it.")
    print("=" * 65)

    try:
        # Keep this launcher alive while dashboard is running
        while dashboard_process.poll() is None:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Ctrl+C detected.")
        print("Stopping Streamlit dashboard...")

        dashboard_process.terminate()

        try:
            dashboard_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            dashboard_process.kill()
            dashboard_process.wait()

        print("✅ Dashboard stopped.")
        print("👋 Automation finished.")


if __name__ == "__main__":
    main()