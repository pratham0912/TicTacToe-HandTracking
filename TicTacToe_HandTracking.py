import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import time

# Initialize Hand Detector
detector = HandDetector(detectionCon=0.7, maxHands=1)

# Winner check
def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

def check_tie(board):
    for row in board:
        if "" in row:
            return False
    return True


board = [["","",""],["","",""],["","",""]]
player = "O"
game_over = False

last_cell = None
cell_start_time = 0
hold_duration = 1.0  # seconds to confirm a move

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the screen (mirror)
    frame = cv.flip(frame, 1)

    h, w, _ = frame.shape
    h1, h2 = h//3, 2*h//3
    w1, w2 = w//3, 2*w//3

    # Detect hands
    hands, frame = detector.findHands(frame)

    finger_row, finger_col = None, None
    if hands:
        lmList = hands[0]["lmList"]  # landmark list
        x_tip, y_tip = lmList[8][0:2]  # Index finger tip

        # Which cell?
        if x_tip < w1:
            finger_col = 0
        elif x_tip < w2:
            finger_col = 1
        else:
            finger_col = 2

        if y_tip < h1:
            finger_row = 0
        elif y_tip < h2:
            finger_row = 1
        else:
            finger_row = 2

        # Preview highlight
        if finger_row is not None and finger_col is not None:
            cx = finger_col * w1 + w1//2
            cy = finger_row * h1 + h1//2
            cv.circle(frame, (cx, cy), min(w1, h1)//4, (200, 200, 0), 2)

        # If finger is in a cell
        if not game_over and finger_row is not None and finger_col is not None:
            if last_cell == (finger_row, finger_col):
                if time.time() - cell_start_time > hold_duration:
                    if board[finger_row][finger_col] == "":
                        board[finger_row][finger_col] = player
                        print(f"Player {player} marked cell ({finger_row}, {finger_col})")
                        player = "X" if player == "O" else "O"
                    last_cell = None
            else:
                last_cell = (finger_row, finger_col)
                cell_start_time = time.time()

    # Draw grid
    cv.line(frame, (w1, 0), (w1, h), (0, 0, 0), 3)
    cv.line(frame, (w2, 0), (w2, h), (0, 0, 0), 3)
    cv.line(frame, (0, h1), (w, h1), (0, 0, 0), 3)
    cv.line(frame, (0, h2), (w, h2), (0, 0, 0), 3)

    # Draw moves
    for row in range(3):
        for col in range(3):
            center_x = col * w1 + w1//2
            center_y = row * h1 + h1//2
            radius = min(w1,h1)//3
            if board[row][col] == "O":
                cv.circle(frame, (center_x, center_y), radius, (0, 0, 255), 5)
            elif board[row][col] == "X":
                size = radius
                cv.line(frame,(center_x-size, center_y-size), (center_x+size, center_y+size), (0, 0, 255), 5)
                cv.line(frame,(center_x-size, center_y+size), (center_x+size, center_y-size), (0, 0, 255), 5)

    # Check winner/tie
    winner = check_winner(board)
    if winner:
        cv.putText(frame,f"{winner} wins!",(50,50), cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3,cv.LINE_AA)
        game_over = True
    elif check_tie(board):
        cv.putText(frame,"It's a Tie!",(50,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3,cv.LINE_AA)
        game_over = True

    cv.imshow("Tic Tac Toe", frame)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        board = [["","",""],["","",""],["","",""]]
        player = "O"
        game_over = False
        last_cell = None
        cell_start_time = 0

cap.release()
cv.destroyAllWindows()
