# 贪吃蛇游戏

这是一个使用 HTML5 Canvas 和 JavaScript 开发的经典贪吃蛇游戏。

## 在线游玩

访问 [贪吃蛇游戏](https://LisonHua.github.io/snake-game) 即可开始游戏！

## 本地运行

1. 克隆仓库：
```bash
git clone https://github.com/LisonHua/snake-game.git
cd snake-game
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行游戏：
```bash
python app.py
```

4. 在浏览器中访问：
```
https://LisonHua.github.io/snake-game
```

## 游戏控制

- 点击"开始游戏"按钮开始游戏
- 使用方向键（↑↓←→）控制蛇的移动方向
- 吃到红色食物可以增加长度和分数
- 撞到自己或边界会显示游戏结束画面
- 按窗口的关闭按钮可以退出游戏

## 游戏特性

- 动态速度系统：蛇的长度增加时，移动速度会逐渐加快
- 游戏开始界面：需要点击按钮才能开始游戏
- 游戏结束画面：显示最终得分
- 实时显示得分和速度
- 流畅的游戏体验
- 简洁的界面设计

## 技术栈

- HTML5 Canvas
- JavaScript (ES6+)
- CSS3
- Flask (用于本地开发) 