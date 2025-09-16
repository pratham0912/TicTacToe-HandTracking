cat <<EOL > README.md
# TicTacToe-HandTracking

**Play Tic Tac Toe using your hand! No mouse or keyboard required.**

This Python project allows you to play Tic Tac Toe using **hand gestures**. The game detects your finger hovering over the grid using your webcam and confirms a move after holding your finger over a cell for a short duration.

---

## Features

- Real-time hand tracking using **CVZone**.
- Interactive Tic Tac Toe grid displayed on webcam feed with OpenCV.
- Hover-to-play mechanism: **place your move by holding your finger over a cell**.
- Automatic player switching between **X** and **O**.
- Detects **win** and **tie** conditions.
- Safe and user-friendly interface to avoid accidental moves.

---

## Installation

1. **Clone the repository:**

\`\`\`bash
git clone https://github.com/pratham0912/TicTacToe-HandTracking.git
cd TicTacToe-HandTracking
\`\`\`

2. **Install required libraries:**

\`\`\`bash
pip install opencv-python cvzone
\`\`\`

> Make sure you have a working webcam connected.

---

## Usage

1. Run the Python script:

\`\`\`bash
python tic_tac_toe_hand.py
\`\`\`

2. Hover your index finger over a cell for **1 second** to place your move.
3. The game will display the winner or tie once the board is filled.
4. Press **\`r\`** to reset the game and **\`q\`** to quit.

---

## How It Works

- Uses **CVZone's HandDetector** to detect hand landmarks.
- Tracks the **index finger tip** (\`lmList[8]\`) to determine which cell is being hovered.
- \`cell_start_time\` tracks when the finger first enters a cell.
- A move is placed only if the finger **stays in the same cell for \`hold_duration\` seconds**.
- The board state is updated and the game checks for **winner or tie**.

---

## Author

**Prathamesh Sonwalkar**  
AIML Student | Robotics Enthusiast  

EOL
