import subprocess
import sys

PIPELINE_STEPS = [
    "scripts/collectors/manual_event_logger.py",
    "scripts/collectors/weather_collector.py",
    "scripts/loaders/load_events.py",
    "scripts/loaders/load_weather.py",
    "scripts/preprocessing/create_processed_dataset.py",
    "scripts/preprocessing/feature_engineering.py",
    "scripts/preprocessing/merge_event_weather.py",
    "scripts/modeling/select_best_model.py",
]

if __name__ == "__main__":
    for step in PIPELINE_STEPS:
        print(f"\nRunning: {step}")
        result = subprocess.run([sys.executable, step], check=False)
        if result.returncode != 0:
            print(f"Pipeline stopped at: {step}")
            sys.exit(result.returncode)

    print("\nPipeline completed successfully.")