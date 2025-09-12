document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.querySelector('.grid-container');
    const scoreElement = document.getElementById('score');
    const bestScoreElement = document.getElementById('best-score');
    const newGameButton = document.getElementById('new-game');
    const tryAgainButton = document.getElementById('try-again');
    const keepGoingButton = document.getElementById('keep-going');
    const gameOverScreen = document.querySelector('.game-over');
    const gameWonScreen = document.querySelector('.game-won');

    let grid = [];
    let score = 0;
    let bestScore = localStorage.getItem('bestScore') || 0;
    let gameOver = false;
    let gameWon = false;

    // Initialize the game
    function initGame() {
        // Clear the grid
        grid = Array(4).fill().map(() => Array(4).fill(0));
        score = 0;
        gameOver = false;
        gameWon = false;
        
        // Clear the grid container
        gridContainer.innerHTML = '';
        
        // Create the grid cells
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                const cell = document.createElement('div');
                cell.className = 'grid-cell';
                gridContainer.appendChild(cell);
            }
        }
        
        // Add initial tiles
        addRandomTile();
        addRandomTile();
        
        // Update the score display
        updateScore();
        
        // Hide game over/win screens
        gameOverScreen.style.display = 'none';
        gameWonScreen.style.display = 'none';
    }

    // Add a random tile (2 or 4) to an empty cell
    function addRandomTile() {
        const emptyCells = [];
        
        // Find all empty cells
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (grid[i][j] === 0) {
                    emptyCells.push({x: i, y: j});
                }
            }
        }
        
        if (emptyCells.length > 0) {
            // Choose a random empty cell
            const {x, y} = emptyCells[Math.floor(Math.random() * emptyCells.length)];
            // 90% chance for 2, 10% chance for 4
            grid[x][y] = Math.random() < 0.9 ? 2 : 4;
            
            // Create and animate the new tile
            createTile(x, y, grid[x][y], true);
        }
    }

    // Create a tile element at the specified position
    function createTile(x, y, value, isNew = false) {
        const tile = document.createElement('div');
        tile.className = `tile tile-${value} ${isNew ? 'new-tile' : ''}`;
        tile.textContent = value;
        
        // Position the tile
        const posX = y * 25 + (y * 15);
        const posY = x * 25 + (x * 15);
        
        tile.style.left = `${posX}%`;
        tile.style.top = `${posY}%`;
        
        // Add data attributes for tracking position
        tile.dataset.x = x;
        tile.dataset.y = y;
        tile.dataset.value = value;
        
        gridContainer.appendChild(tile);
        return tile;
    }

    // Update the score display
    function updateScore() {
        scoreElement.textContent = score;
        bestScore = Math.max(score, bestScore);
        bestScoreElement.textContent = bestScore;
        localStorage.setItem('bestScore', bestScore);
    }

    // Check if there are any moves left
    function hasMovesLeft() {
        // Check for any empty cells
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (grid[i][j] === 0) return true;
                
                // Check adjacent cells for possible merges
                if (i < 3 && grid[i][j] === grid[i + 1][j]) return true;
                if (j < 3 && grid[i][j] === grid[i][j + 1]) return true;
            }
        }
        return false;
    }

    // Move tiles in the specified direction
    function moveTiles(direction) {
        if (gameOver || gameWon) return false;
        
        let moved = false;
        const oldGrid = JSON.parse(JSON.stringify(grid));
        
        // Remove all tiles from the DOM (we'll recreate them after moving)
        const tiles = document.querySelectorAll('.tile');
        const tilesData = Array.from(tiles).map(tile => ({
            x: parseInt(tile.dataset.x),
            y: parseInt(tile.dataset.y),
            value: parseInt(tile.dataset.value),
            element: tile
        }));
        
        tiles.forEach(tile => tile.remove());
        
        // Process the move based on direction
        switch (direction) {
            case 'up':
                moved = moveUp();
                break;
            case 'right':
                moved = moveRight();
                break;
            case 'down':
                moved = moveDown();
                break;
            case 'left':
                moved = moveLeft();
                break;
        }
        
        // If the grid changed, add a new random tile
        if (moved) {
            addRandomTile();
            updateScore();
            
            // Check for win condition
            if (!gameWon && checkWin()) {
                gameWon = true;
                gameWonScreen.style.display = 'flex';
            }
            // Check for game over
            else if (!hasMovesLeft()) {
                gameOver = true;
                gameOverScreen.style.display = 'flex';
            }
        }
        
        // Recreate tiles with new positions
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (grid[i][j] !== 0) {
                    createTile(i, j, grid[i][j]);
                }
            }
        }
        
        return moved;
    }

    // Move tiles up
    function moveUp() {
        let moved = false;
        
        for (let j = 0; j < 4; j++) {
            // Move all tiles up as much as possible
            for (let i = 1; i < 4; i++) {
                if (grid[i][j] !== 0) {
                    let row = i;
                    while (row > 0 && grid[row - 1][j] === 0) {
                        grid[row - 1][j] = grid[row][j];
                        grid[row][j] = 0;
                        row--;
                        moved = true;
                    }
                    
                    // Check for merge with the tile above
                    if (row > 0 && grid[row - 1][j] === grid[row][j] && 
                        !document.querySelector(`.tile[data-x="${row-1}"][data-y="${j}"].merged`)) {
                        grid[row - 1][j] *= 2;
                        score += grid[row - 1][j];
                        grid[row][j] = 0;
                        moved = true;
                    }
                }
            }
        }
        
        return moved;
    }

    // Move tiles right
    function moveRight() {
        let moved = false;
        
        for (let i = 0; i < 4; i++) {
            for (let j = 2; j >= 0; j--) {
                if (grid[i][j] !== 0) {
                    let col = j;
                    while (col < 3 && grid[i][col + 1] === 0) {
                        grid[i][col + 1] = grid[i][col];
                        grid[i][col] = 0;
                        col++;
                        moved = true;
                    }
                    
                    // Check for merge with the tile to the right
                    if (col < 3 && grid[i][col + 1] === grid[i][col] && 
                        !document.querySelector(`.tile[data-x="${i}"][data-y="${col+1}"].merged`)) {
                        grid[i][col + 1] *= 2;
                        score += grid[i][col + 1];
                        grid[i][col] = 0;
                        moved = true;
                    }
                }
            }
        }
        
        return moved;
    }

    // Move tiles down
    function moveDown() {
        let moved = false;
        
        for (let j = 0; j < 4; j++) {
            for (let i = 2; i >= 0; i--) {
                if (grid[i][j] !== 0) {
                    let row = i;
                    while (row < 3 && grid[row + 1][j] === 0) {
                        grid[row + 1][j] = grid[row][j];
                        grid[row][j] = 0;
                        row++;
                        moved = true;
                    }
                    
                    // Check for merge with the tile below
                    if (row < 3 && grid[row + 1][j] === grid[row][j] && 
                        !document.querySelector(`.tile[data-x="${row+1}"][data-y="${j}"].merged`)) {
                        grid[row + 1][j] *= 2;
                        score += grid[row + 1][j];
                        grid[row][j] = 0;
                        moved = true;
                    }
                }
            }
        }
        
        return moved;
    }

    // Move tiles left
    function moveLeft() {
        let moved = false;
        
        for (let i = 0; i < 4; i++) {
            for (let j = 1; j < 4; j++) {
                if (grid[i][j] !== 0) {
                    let col = j;
                    while (col > 0 && grid[i][col - 1] === 0) {
                        grid[i][col - 1] = grid[i][col];
                        grid[i][col] = 0;
                        col--;
                        moved = true;
                    }
                    
                    // Check for merge with the tile to the left
                    if (col > 0 && grid[i][col - 1] === grid[i][col] && 
                        !document.querySelector(`.tile[data-x="${i}"][data-y="${col-1}"].merged`)) {
                        grid[i][col - 1] *= 2;
                        score += grid[i][col - 1];
                        grid[i][col] = 0;
                        moved = true;
                    }
                }
            }
        }
        
        return moved;
    }

    // Check if the player has won (reached 2048)
    function checkWin() {
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (grid[i][j] === 2048) {
                    return true;
                }
            }
        }
        return false;
    }

    // Event listeners
    document.addEventListener('keydown', (e) => {
        switch (e.key) {
            case 'ArrowUp':
                e.preventDefault();
                moveTiles('up');
                break;
            case 'ArrowRight':
                e.preventDefault();
                moveTiles('right');
                break;
            case 'ArrowDown':
                e.preventDefault();
                moveTiles('down');
                break;
            case 'ArrowLeft':
                e.preventDefault();
                moveTiles('left');
                break;
        }
    });

    // Touch support for mobile devices
    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
    let touchEndY = 0;

    document.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    }, false);

    document.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].clientX;
        touchEndY = e.changedTouches[0].clientY;
        handleSwipe();
    }, false);

    function handleSwipe() {
        const dx = touchEndX - touchStartX;
        const dy = touchEndY - touchStartY;
        
        // Determine if the swipe was more horizontal or vertical
        if (Math.abs(dx) > Math.abs(dy)) {
            // Horizontal swipe
            if (dx > 0) {
                moveTiles('right');
            } else {
                moveTiles('left');
            }
        } else {
            // Vertical swipe
            if (dy > 0) {
                moveTiles('down');
            } else {
                moveTiles('up');
            }
        }
    }

    // Button event listeners
    newGameButton.addEventListener('click', initGame);
    tryAgainButton.addEventListener('click', initGame);
    keepGoingButton.addEventListener('click', () => {
        gameWonScreen.style.display = 'none';
        gameWon = false;
    });

    // Initialize the game
    initGame();
});
