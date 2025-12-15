from core import X, O, TicTacToeNXN, EMPTY
from helper import (
    initialize_widgets, create_board_ui, update_board_ui,
    display_game_end, display_initial_ui
)
from IPython.display import clear_output, HTML

# === BIẾN TOÀN CỤC ===
game: TicTacToeNXN = None
buttons = []
current_difficulty = "Khó"

# === KHỞI TẠO WIDGETS ===
(n_slider, player_choice, difficulty_choice, start_button, restart_button,
 out, status_label, grid_container) = initialize_widgets()

# === HÀM XỬ LÝ SỰ KIỆN ===

def handle_player_click(row, col):
    """Xử lý sự kiện khi người dùng click vào một ô trên bảng."""
    global game
    if not game or game.terminal() or game.player_turn() != game.user or game.board[row][col] != EMPTY:
        return

    # 1. Người dùng đi
    game.board[row][col] = game.user
    update_board_ui(game, buttons)

    if game.terminal():
        display_game_end(game, out, status_label)
        return

    # 2. Lượt AI
    handle_ai_turn()

def handle_ai_turn():
    """Xử lý lượt đi của AI."""
    global game, current_difficulty

    status_label.value = f"🤖 AI ({current_difficulty}) đang suy nghĩ..."
    with out:
        clear_output(wait=True)
        display(HTML("<i>Đang tính nước đi tối ưu...</i>"))

    move = game.get_best_move(current_difficulty)

    if move:
        game.board[move[0]][move[1]] = game.ai
        update_board_ui(game, buttons)

        if game.terminal():
            display_game_end(game, out, status_label)
        else:
            status_label.value = f"🟢 Lượt của bạn ({game.user})"
            with out:
                clear_output()
    else:
        # Xử lý trường hợp không còn nước đi (chỉ xảy ra khi trò chơi đã kết thúc)
        if game.terminal():
             display_game_end(game, out, status_label)

def start_game(b):
    """Xử lý sự kiện khi click nút Bắt đầu chơi."""
    global game, current_difficulty, buttons
    n = n_slider.value
    user_sym = player_choice.value
    current_difficulty = difficulty_choice.value

    # AI là ký hiệu còn lại
    ai_sym = O if user_sym == X else X

    game = TicTacToeNXN(n, user_sym, ai_sym)

    with grid_container:
        clear_output(wait=True)
        # Tạo bảng giao diện và lưu trữ các nút bấm
        grid, buttons = create_board_ui(n, handle_player_click)
        display(grid)

    update_board_ui(game, buttons)
    status_label.value = f"📏 {n}x{n} | Bạn: {game.user} | AI: {game.ai} | Độ khó: {current_difficulty} | Lượt: {game.player_turn()}"
    with out:
        clear_output()

    # Nếu là lượt AI → tự động đánh ngay
    if game.player_turn() == game.ai:
        handle_ai_turn()

def reset_game(b):
    """Xử lý sự kiện khi click nút Chơi lại."""
    global game, buttons
    game = None
    buttons = []
    with grid_container:
        clear_output(wait=True)
    with out:
        clear_output(wait=True)
    status_label.value = "🎮 Chào mừng đến với Tic-Tac-Toe NxN!"

# === GẮN HÀM XỬ LÝ VÀ HIỂN THỊ CUỐI CÙNG ===
start_button.on_click(start_game)
restart_button.on_click(reset_game)

if __name__ == '__main__':
    # Hiển thị giao diện chính trong Colab/Jupyter Notebook
    display_initial_ui(n_slider, player_choice, difficulty_choice, start_button, restart_button, status_label, grid_container, out)
