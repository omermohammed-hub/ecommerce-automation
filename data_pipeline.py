
import subprocess
import sys
from pathlib import Path


def run_pipeline():

    # Find the project directory
    project_folder = Path(__file__).resolve().parent

    scripts_folder = project_folder / "scripts"

    # Scripts must run in this order
    pipeline_steps = [
        ("EXTRACT DATA", "extract_data.py"),
        ("TRANSFORM DATA", "transform_data.py"),
        ("LOAD SQLITE DATABASE", "load_database.py"),
        ("VALIDATE DATABASE", "validate_database.py")
    ]

    print("\n" + "=" * 60)
    print("ECOMMERCE AUTOMATED DATA PIPELINE")
    print("=" * 60)

    # Execute each pipeline stage
    for step_name, script_name in pipeline_steps:

        script_path = scripts_folder / script_name

        print(f"\n{'=' * 60}")
        print(f"STARTING: {step_name}")
        print("=" * 60)

        subprocess.run(
            [sys.executable, str(script_path)],
            cwd=project_folder,
            check=True
        )

        print(f"\nCOMPLETED: {step_name}")

    print("\n" + "=" * 60)
    print("ALL PIPELINE STAGES COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
