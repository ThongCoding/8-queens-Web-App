from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

numQueens = 8  # Default number of queens (can be changed dynamically)
currentSolution = []  # Will hold current testing data
solutions = []  # Found solutions
currentSolutionIndex = 0  # Index to track the current solution being displayed
currentStepRow = 0  # Row tracker for the step-by-step "Next" button

# Check if it's safe to place a queen in the current row and column
def isSafe(testRow, testCol):
    for row in range(testRow):
        # Check vertical attack
        if currentSolution[row] == testCol:
            return False

        # Check diagonal attack
        if abs(testRow - row) == abs(currentSolution[row] - testCol):
            return False

    return True

# Recursive function to generate solutions
def place_queen(row):
    global solutions

    if row == numQueens:  # All queens are placed
        solutions.append(currentSolution.copy())
        return

    for col in range(numQueens):  # Try every column in the current row
        if isSafe(row, col):
            currentSolution[row] = col  # Place the queen
            place_queen(row + 1)  # Recur to place the next queen

# Generate all possible solutions using recursive backtracking
def generate_solutions():
    global currentSolution, solutions
    solutions = []  # Clear any existing solutions
    currentSolution = [-1] * numQueens  # Initialize solution array

    # Start placing queens from row 0
    place_queen(0)

# Initialize solutions on app start
generate_solutions()

# Serve the home page
@app.route('/')
def index():
    return render_template('index.html')

# API to get the current board state
@app.route('/get_board', methods=['GET'])
def get_board():
    global currentSolutionIndex, solutions
    board = [[0 for _ in range(numQueens)] for _ in range(numQueens)]

    if currentSolutionIndex < len(solutions):
        solution = solutions[currentSolutionIndex]
        for row in range(numQueens):
            board[row][solution[row]] = 1  # Place the queen in the correct column

    return jsonify(board=board)

# API to handle "Solve" action (increment to the next solution)
@app.route('/solve', methods=['POST'])
def solve_step():
    global currentSolutionIndex, solutions
    currentSolutionIndex += 1
    if currentSolutionIndex >= len(solutions):
        currentSolutionIndex = 0  # Loop back to the first solution if out of range
    return jsonify(success=True)

# API to handle "Next" action (step-by-step queen placement)
@app.route('/next', methods=['POST'])
def next_step():
    global currentStepRow, currentSolutionIndex, solutions
    board = [[0 for _ in range(numQueens)] for _ in range(numQueens)]

    if currentSolutionIndex < len(solutions):
        solution = solutions[currentSolutionIndex]
        
        # If we've finished displaying the current solution, move to the next one
        if currentStepRow >= numQueens:
            currentSolutionIndex += 1
            if currentSolutionIndex >= len(solutions):
                currentSolutionIndex = 0  # Loop back to the first solution if out of range
            currentStepRow = 0  # Reset step-by-step progress for the next solution

        # Place queens row by row up to the current step
        for row in range(currentStepRow + 1):
            board[row][solution[row]] = 1

        currentStepRow += 1

    return jsonify(board=board)

# API to handle "Restart" action (reset to the first solution)
@app.route('/restart', methods=['POST'])
def restart():
    global currentSolutionIndex, currentStepRow
    currentSolutionIndex = 0  # Reset to the first solution
    currentStepRow = 0  # Reset step-by-step progress
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
