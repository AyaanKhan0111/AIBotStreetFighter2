# AI Game Bot for Street Fighter II Turbo

**Contributors:** 22I2066 Ayaan Khan | 22I-1915 Ahmed Mehmood | 22I-2066 Ahmed Luqman | 22I-1977 M Afnan
**Submission Date:** May 9, 2025

---

## Table of Contents

1. Introduction
2. Objectives
3. Project Setup and Dependencies
4. Code Architecture
   4.1 controller.py
   4.2 bot.py
   4.3 command.py and buttons.py
   4.4 game\_state.py and player.py
   4.5 project.py (Data Merging)
5. Dataset Generation
6. Feature Extraction
7. Model Development and Training
8. Integration and Execution
9. Usage Instructions
10. Results and Observations
11. Conclusion
12. References

---

## 1. Introduction

This project presents the design and implementation of an AI-driven bot for the game *Street Fighter II Turbo*. The bot replaces traditional rule-based systems using a neural network trained on gameplay data to predict optimal button presses in real time.

## 2. Objectives

* Replace static rule-based logic with a neural network.
* Support any character generically.
* Automate gameplay data collection.
* Ensure the project is easily reproducible.

## 3. Project Setup and Dependencies

**Operating System:** Windows 7 or above (64-bit)
**Python Version:** 3.6.3 (tested), compatible with Python ≥ 3.7
**Libraries:**

* TensorFlow
* NumPy
* pandas
* scikit-learn

**Emulator:** BizHawk (EmuHawk.exe)

**Installation Steps:**

1. Install Python and pip.
2. Install dependencies:

```bash
pip install tensorflow numpy pandas scikit-learn
```

3. Extract BizHawk and place `EmuHawk.exe` appropriately.
4. Extract source files and `model.h5` into your project folder.

## 4. Code Architecture

### 4.1 controller.py

* Handles socket communication with BizHawk.
* Logs game state to `game_data.csv`.
* Functions:

  * `connect()`, `receive()`, `send()`
  * `DataLogger` class for writing game + action data.

### 4.2 bot.py

* `Bot` class:

  * Loads `model.h5`
  * Extracts features from game state
  * Feeds features into the neural network to predict button actions

### 4.3 command.py and buttons.py

* `Buttons`: 12 SNES button states (up, down, left, right, Y, B, X, A, L, R, select, start)
* `Command`: Holds two button states and converts to JSON for socket transmission

### 4.4 game\_state.py and player.py

* `GameState`: Parses JSON into `Player` objects + match metadata
* `Player`: Attributes like health, position, move states, etc.

### 4.5 project.py

* Merges CSV files (`sfdataset*.csv`) using pandas
* Removes duplicates and saves as `sfmerged.csv`

## 5. Dataset Generation

1. Launch BizHawk in single-player mode
2. Run:

```bash
python controller.py 1
```

3. Play rounds to log human actions
4. Repeat for various characters
5. Merge datasets via `project.py`

## 6. Feature Extraction

Extracted per frame:

* Timer, flags
* Player/opponent: character ID, health, x/y position, jumping/crouching status, move ID
* 17 total features used as model inputs

## 7. Model Development and Training

**Data Preparation:**

* Boolean to integer conversion
* Split dataset (80% train, 20% test)

**Model Architecture:**

* Input: 17
* Dense(128, relu) -> Dense(64, relu) -> Dense(10, sigmoid)

**Compilation:**

* Optimizer: Adam
* Loss: Binary Crossentropy
* Metrics: Accuracy

**Training:**

* 100 epochs, batch size 32, validation split 0.1

**Model Saving:**

* Save to `model.h5`

## 8. Integration and Execution

1. Place `model.h5` in root directory
2. Launch ROM in BizHawk
3. Connect via emulator UI (Tool Box - Shift+T)
4. Run:

```bash
python controller.py [1|2]
```

5. Watch bot play and generate logs

## 9. Usage Instructions

Zip package includes:

* Source files: `.py` scripts listed above
* Trained model: `model.h5`
* Documentation: README.md or PDF/Word version

## 10. Results and Observations

* Performs coherent combos
* Occasionally fails under pressure (time constraints)
* Future improvements:

  * Fine-tune prediction thresholds
  * Add RNN/LSTM for temporal dependencies

## 11. Conclusion

The project effectively demonstrates how AI can replace deterministic logic in classic games. It provides a modular, scalable, and reproducible pipeline from data collection to deployment.

## 12. References

1. BizHawk Emulator API documentation
2. TensorFlow Keras documentation
3. Kaggle Street Fighter datasets
