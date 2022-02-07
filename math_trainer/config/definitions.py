from pathlib import Path

ROOT_PATH = Path(__file__).parents[2]
SRC_PATH = ROOT_PATH / "math_trainer"
AUDIO_FILES_PATH = ROOT_PATH / "audio_files"
TRAINING_FILES_PATH = ROOT_PATH / "training_files"

VERSION = "1.2"


def test_definitions():
    print(f"\nRoot path:                     {ROOT_PATH}")
    print(f"Src aka math_trainer path:     {SRC_PATH}")
    print(f"Audio files path:              {AUDIO_FILES_PATH}")
    print(f"Training files path:           {TRAINING_FILES_PATH}")

    assert "math_trainer" in str(ROOT_PATH), "Root path not correct, check definitions."
    assert "math_trainer\\math_trainer" in str(SRC_PATH), "Src aka math_trainer path not correct, check definitions."
    assert "audio_files" in str(AUDIO_FILES_PATH), "Audio files path not correct, check definitions."
    assert "training_files" in str(TRAINING_FILES_PATH), "Training files path not correct, check definitions."

    print("\nDefinitions work!")


if __name__ == "__main__":
    test_definitions()
