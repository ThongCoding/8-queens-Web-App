// Function to render the board and update the logs
function renderBoard(board) {
  const chessboard = document.getElementById("chessboard");
  chessboard.innerHTML = ""; // Clear the board

  // Render the chessboard (even if empty)
  for (let i = 0; i < board.length; i++) {
    const row = document.createElement("div");
    row.className = "row";

    // Create and style the chessboard rows and cells
    for (let j = 0; j < board[i].length; j++) {
      const cell = document.createElement("div");
      cell.className = "cell";

      // Add the queen if board[i][j] == 1
      if (board[i][j] === 1) {
        const queenImg = document.createElement("img");
        queenImg.src = "/static/img/black_queen.svg"; // Absolute path to the SVG image
        queenImg.className = "queen-image"; // Add a class for styling the queen image
        cell.appendChild(queenImg); // Append the image to the cell
      }
      row.appendChild(cell);
    }
    chessboard.appendChild(row);
  }
}

// Fetch the board state and render it
function fetchBoard() {
  fetch("/get_board")
    .then((response) => response.json())
    .then((data) => renderBoard(data.board));
}

// Handle "Solve" button click (show full solution)
function solveStep() {
  fetch("/solve", { method: "POST" }).then(() => fetchBoard());
}

// Handle "Next" button click (step-by-step queen placement)
function nextStep() {
  fetch("/next", { method: "POST" })
    .then((response) => response.json())
    .then((data) => renderBoard(data.board));
}

// Handle "Restart" button click
function restart() {
  fetch("/restart", { method: "POST" }).then(() => fetchBoard());
}

// Initial render
window.onload = fetchBoard;
