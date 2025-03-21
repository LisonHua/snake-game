class Snake {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.blockSize = 20;
        this.width = canvas.width;
        this.height = canvas.height;
        this.reset();
    }

    reset() {
        this.length = 1;
        this.positions = [{
            x: Math.floor(this.width / 2 / this.blockSize) * this.blockSize,
            y: Math.floor(this.height / 2 / this.blockSize) * this.blockSize
        }];
        this.direction = this.getRandomDirection();
        this.score = 0;
        this.speed = 5;
        this.isAlive = true;
        this.updateScore();
        this.updateSpeed();
    }

    getRandomDirection() {
        const directions = [
            { x: 0, y: -1 },  // UP
            { x: 0, y: 1 },   // DOWN
            { x: -1, y: 0 },  // LEFT
            { x: 1, y: 0 }    // RIGHT
        ];
        return directions[Math.floor(Math.random() * directions.length)];
    }

    update() {
        const head = this.positions[0];
        const newHead = {
            x: head.x + this.direction.x * this.blockSize,
            y: head.y + this.direction.y * this.blockSize
        };

        // 检查是否撞到边界
        if (newHead.x < 0 || newHead.x >= this.width ||
            newHead.y < 0 || newHead.y >= this.height) {
            this.isAlive = false;
            return false;
        }

        // 检查是否撞到自己
        for (let i = 3; i < this.positions.length; i++) {
            if (newHead.x === this.positions[i].x && newHead.y === this.positions[i].y) {
                this.isAlive = false;
                return false;
            }
        }

        this.positions.unshift(newHead);
        if (this.positions.length > this.length) {
            this.positions.pop();
        }
        return true;
    }

    render() {
        this.ctx.fillStyle = '#00ff00';
        this.positions.forEach(position => {
            this.ctx.fillRect(position.x, position.y, this.blockSize, this.blockSize);
        });
    }

    grow() {
        this.length++;
        this.score++;
        this.speed = Math.min(5 + (this.length - 1) * 0.5, 25);
        this.updateScore();
        this.updateSpeed();
    }

    updateScore() {
        document.getElementById('score').textContent = `得分: ${this.score}`;
    }

    updateSpeed() {
        document.getElementById('speed').textContent = `速度: ${Math.floor(this.speed)}`;
    }
}

class Food {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.blockSize = 20;
        this.width = canvas.width;
        this.height = canvas.height;
        this.position = { x: 0, y: 0 };
        this.randomizePosition();
    }

    randomizePosition() {
        this.position = {
            x: Math.floor(Math.random() * (this.width / this.blockSize)) * this.blockSize,
            y: Math.floor(Math.random() * (this.height / this.blockSize)) * this.blockSize
        };
    }

    render() {
        this.ctx.fillStyle = '#ff0000';
        this.ctx.fillRect(this.position.x, this.position.y, this.blockSize, this.blockSize);
    }
}

class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.canvas.width = 800;
        this.canvas.height = 600;
        this.ctx = this.canvas.getContext('2d');
        this.snake = new Snake(this.canvas);
        this.food = new Food(this.canvas);
        this.gameLoop = null;
        this.setupEventListeners();
        this.setupTouchControls();
    }

    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            switch (e.key) {
                case 'ArrowUp':
                    if (this.snake.direction.y !== 1) {
                        this.snake.direction = { x: 0, y: -1 };
                    }
                    break;
                case 'ArrowDown':
                    if (this.snake.direction.y !== -1) {
                        this.snake.direction = { x: 0, y: 1 };
                    }
                    break;
                case 'ArrowLeft':
                    if (this.snake.direction.x !== 1) {
                        this.snake.direction = { x: -1, y: 0 };
                    }
                    break;
                case 'ArrowRight':
                    if (this.snake.direction.x !== -1) {
                        this.snake.direction = { x: 1, y: 0 };
                    }
                    break;
            }
        });

        document.getElementById('start-button').addEventListener('click', () => this.start());
        document.getElementById('restart-button').addEventListener('click', () => this.restart());
    }

    setupTouchControls() {
        let touchStartX = 0;
        let touchStartY = 0;

        this.canvas.addEventListener('touchstart', (e) => {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
            e.preventDefault(); // 防止页面滚动
        }, { passive: false });

        this.canvas.addEventListener('touchmove', (e) => {
            e.preventDefault(); // 防止页面滚动
        }, { passive: false });

        this.canvas.addEventListener('touchend', (e) => {
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            
            const deltaX = touchEndX - touchStartX;
            const deltaY = touchEndY - touchStartY;

            // 判断滑动方向
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                // 水平滑动
                if (deltaX > 0 && this.snake.direction.x !== -1) {
                    this.snake.direction = { x: 1, y: 0 }; // 向右
                } else if (deltaX < 0 && this.snake.direction.x !== 1) {
                    this.snake.direction = { x: -1, y: 0 }; // 向左
                }
            } else {
                // 垂直滑动
                if (deltaY > 0 && this.snake.direction.y !== -1) {
                    this.snake.direction = { x: 0, y: 1 }; // 向下
                } else if (deltaY < 0 && this.snake.direction.y !== 1) {
                    this.snake.direction = { x: 0, y: -1 }; // 向上
                }
            }
        });
    }

    start() {
        document.getElementById('start-screen').classList.add('hidden');
        document.getElementById('game-screen').classList.remove('hidden');
        this.run();
    }

    restart() {
        document.getElementById('game-over-screen').classList.add('hidden');
        document.getElementById('game-screen').classList.remove('hidden');
        this.snake.reset();
        this.food.randomizePosition();
        this.run();
    }

    gameOver() {
        clearInterval(this.gameLoop);
        document.getElementById('game-screen').classList.add('hidden');
        document.getElementById('game-over-screen').classList.remove('hidden');
        document.getElementById('final-score').textContent = `最终得分: ${this.snake.score}`;
    }

    run() {
        if (this.gameLoop) {
            clearInterval(this.gameLoop);
        }

        this.gameLoop = setInterval(() => {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

            if (!this.snake.update()) {
                this.gameOver();
                return;
            }

            // 检查是否吃到食物
            const head = this.snake.positions[0];
            if (head.x === this.food.position.x && head.y === this.food.position.y) {
                this.snake.grow();
                this.food.randomizePosition();
            }

            this.food.render();
            this.snake.render();
        }, 1000 / this.snake.speed);
    }
}

// 初始化游戏
const game = new Game(); 