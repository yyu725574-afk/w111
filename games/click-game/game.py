# 引入 Brython 相關模組
from browser import document, timer
import random
import time

# --- 遊戲設定 ---
GAME_DURATION = 30  # 遊戲時長 (秒)
score = 0
game_active = False

# --- 獲取 DOM 元素及初始化 ---
game_area = document["brython_div1"]
game_area.style.width = "600px"
game_area.style.height = "400px"
game_area.style.margin = "20px auto"
game_area.style.border = "3px solid #333"
game_area.style.backgroundColor = "#e0e0ff"
game_area.style.position = "relative"
game_area.style.overflow = "hidden"
game_area.style.cursor = "crosshair"

# 分數顯示
score_display = document.createElement("div")
score_display.id = "score_display"
score_display.style.position = "absolute"
score_display.style.top = "10px"
score_display.style.left = "10px"
score_display.style.fontSize = "1.2em"
score_display.style.fontWeight = "bold"
score_display.style.backgroundColor = "rgba(255, 255, 255, 0.7)"
score_display.style.padding = "5px"
game_area <= score_display

# 計時器顯示
timer_display = document.createElement("div")
timer_display.id = "timer_display"
timer_display.style.position = "absolute"
timer_display.style.top = "10px"
timer_display.style.right = "10px"
timer_display.style.fontSize = "1.2em"
timer_display.style.fontWeight = "bold"
timer_display.style.backgroundColor = "rgba(255, 255, 255, 0.7)"
timer_display.style.padding = "5px"
game_area <= timer_display

# 創建目標元素
target = document.createElement("div")
target.id = "target"
target.style.width = "50px"
target.style.height = "50px"
target.style.backgroundColor = "#ff4500"
target.style.position = "absolute"
target.style.borderRadius = "50%"
target.style.cursor = "pointer"
target.style.transition = "background-color 0.1s, top 0.3s, left 0.3s, width 0.3s, height 0.3s"
game_area <= target

# 遊戲結束訊息
game_over_msg = document.createElement("div")
game_over_msg.style.position = "absolute"
game_over_msg.style.top = "50%"
game_over_msg.style.left = "50%"
game_over_msg.style.transform = "translate(-50%, -50%)"
game_over_msg.style.backgroundColor = "rgba(0, 0, 0, 0.9)"
game_over_msg.style.color = "white"
game_over_msg.style.padding = "30px"
game_over_msg.style.borderRadius = "10px"
game_over_msg.style.fontSize = "2em"
game_over_msg.style.zIndex = "100"
game_over_msg.style.display = "none"
game_over_msg.style.textAlign = "center"
game_area <= game_over_msg

# --- 遊戲核心邏輯 ---
def move_target():
    """將目標移動到隨機位置，並依據分數調整大小"""
    if not game_active:
        return

    # 動態調整目標大小，最小 30px，最大 100px
    new_size = min(30 + score * 2, 100)
    target.style.width = f"{new_size}px"
    target.style.height = f"{new_size}px"

    max_x = game_area.clientWidth - new_size
    max_y = game_area.clientHeight - new_size
    min_y = 40

    new_x = random.randint(0, max(0, max_x))
    new_y = random.randint(min_y, max(min_y, max_y))

    target.style.backgroundColor = f"rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})"
    target.style.left = f"{new_x}px"
    target.style.top = f"{new_y}px"

@target.bind("click")
def hit_target(event):
    """點擊目標得分"""
    global score
    if not game_active:
        return

    score += 1
    score_display.text = f"分數: {score}"
    move_target()
    event.stopPropagation()

def restart_game(event):
    """重新開始遊戲"""
    global score
    game_over_msg.style.display = "none"
    score = 0
    start_game()
    event.stopPropagation()

def check_time():
    """更新計時器並檢查遊戲是否結束"""
    global game_active
    remaining = int(game_over_time - time.time())

    if remaining <= 0:
        timer_display.text = "時間: 0s"
        if game_active:
            game_active = False
            game_over_msg.innerHTML = f"遊戲結束！<br>最終分數: {score}"

            restart_btn = document.createElement("button")
            restart_btn.text = "重新開始"
            restart_btn.style.marginTop = "15px"
            restart_btn.style.padding = "10px 20px"
            restart_btn.style.fontSize = "0.7em"
            restart_btn.style.cursor = "pointer"
            restart_btn.bind("click", restart_game)

            game_over_msg <= document.createElement("br")
            game_over_msg <= restart_btn
            game_over_msg.style.display = "block"

            timer.clear_interval(move_interval_handle)
    else:
        timer_display.text = f"時間: {remaining}s"
        timer.set_timeout(check_time, 1000)

# --- 遊戲啟動 ---
def start_game():
    global game_active, game_over_time, move_interval_handle, score

    game_active = True
    score = 0
    score_display.text = "分數: 0"
    timer_display.text = f"時間: {GAME_DURATION}s"

    game_over_time = time.time() + GAME_DURATION
    check_time()
    move_target()

    # 設置目標元素定時自動移動（延長停留時間為 5 秒）
    move_interval_handle = timer.set_interval(move_target, 5000)  # 每 5 秒移動一次

# 啟動遊戲
start_game()
