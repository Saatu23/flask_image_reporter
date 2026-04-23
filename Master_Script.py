import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS_ORDER = [
    "TIF_To_PNG.py",
    "Contour_Form.py",
    "PDF_Making.py",
    "Merge_Custom.py",
    "Clear_Folders.py"
]

def convert_notebook(notebook_path):
    """Convert Jupyter notebook to Python script and execute"""
    try:
        full_path = os.path.join(BASE_DIR, notebook_path)

        subprocess.run(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "python",
                "--execute",
                "--inplace",
                full_path
            ],
            check=True
        )

        py_file = full_path.replace(".ipynb", ".py")

        subprocess.run(
            [sys.executable, py_file],
            check=True
        )

    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing notebook {notebook_path}: {e}")
        sys.exit(1)


def run_python_script(script_path):
    """Execute Python script"""
    try:
        full_path = os.path.join(BASE_DIR, script_path)

        if not os.path.exists(full_path):
            print(f"❌ File not found: {script_path}")
            sys.exit(1)

        subprocess.run(
            [sys.executable, full_path],
            check=True
        )

    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing {script_path}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🚀 Starting Image Processing Pipeline...\n")

    for script in SCRIPTS_ORDER:
        print(f"▶ Executing {script}")

        if script.endswith(".ipynb"):
            convert_notebook(script)

        elif script.endswith(".py"):
            run_python_script(script)

        else:
            print(f"❌ Unsupported file format: {script}")
            sys.exit(1)

    output_file = os.path.join(BASE_DIR, "Quality-Report.pdf")

    print("\n✅ All scripts executed successfully")

    if os.path.exists(output_file):
        print(f"📄 Output PDF: {output_file}")
    else:
        print("⚠️ PDF generated step completed, but file not found.")
