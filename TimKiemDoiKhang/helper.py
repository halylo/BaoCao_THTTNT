import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
from core import X, O, EMPTY, TicTacToeNXN # Import các hằng số và lớp từ core.py

# === KHỞI TẠO CÁC WIDGET CHUNG ===

def initialize_widgets():
    """Khởi tạo và trả về các widget chính cho giao diện."""
    display(HTML("""
    <style>
    .widget-slider, .widget-radio-buttons, .widget-dropdown {
        background-color: #FFF9C4 !important;
        border: 2px solid #FFECB3 !important;
        border-radius: 12px !important;
        padding: 5px !important;
        margin: 5px 0 !important;
    }
    .widget-label { color: #333 !important; font-weight: bold !important; }
    </style>
    """))

    out = widgets.Output()
    status_label = widgets.Label(value="🎮 Chào mừng đến với Tic-Tac-Toe NxN!", style={'font_weight': 'bold', 'font_size': '18px'})
    grid_container = widgets.Output()

    n_slider = widgets.IntSlider(value=3, min=3, max=5, step=1, description='Kích thước N:', description_width='120px')
    player_choice = widgets.RadioButtons(options=[('X - Bạn đi trước', X), ('O - AI đi trước', O)], description='Bạn chơi:', description_width='120px')
    difficulty_choice = widgets.Dropdown(
        options=[('Dễ 🟢', 'Dễ'), ('Trung bình 🟡', 'Trung bình'), ('Khó 🔴', 'Khó')],
        value='Khó',
        description='Độ khó AI:', description_width='120px'
    )

    start_button = widgets.Button(description="🚀 Bắt đầu chơi", button_style='success',
                                  layout=widgets.Layout(width='240px', height='60px'))
    restart_button = widgets.Button(description="🔄 Chơi lại", button_style='warning',
                                    layout=widgets.Layout(width='160px', height='50px'))

    return n_slider, player_choice, difficulty_choice, start_button, restart_button, out, status_label, grid_container

# === HÀM VẼ BẢNG VÀ CẬP NHẬT GIAO DIỆN ===

def create_board_ui(n, player_click_handler):
    """Tạo GridBox chứa các nút bấm cho bảng trò chơi."""
    buttons = []
    grid = widgets.GridBox(layout=widgets.Layout(
        grid_template_columns=f"repeat({n}, 120px)",
        grid_gap="12px",
        justify_content="center",
        padding="20px"
    ))
    for i in range(n):
        for j in range(n):
            btn = widgets.Button(
                description="",
                layout=widgets.Layout(width='115px', height='115px'),
                style={'font_size': '52px', 'font_weight': 'bold', 'button_color': '#ffffff'}
            )
            # Gán hàm xử lý sự kiện click
            btn.on_click(lambda b, r=i, c=j: player_click_handler(r, c))
            buttons.append(btn)
            grid.children += (btn,)
    return grid, buttons

def update_board_ui(game, buttons):
    """Cập nhật trạng thái các nút bấm trên giao diện dựa trên trạng thái trò chơi."""
    for idx, btn in enumerate(buttons):
        i, j = divmod(idx, game.n)
        val = game.board[i][j]
        btn.description = val if val != EMPTY else ""
        btn.style.text_color = '#0d6efd' if val == X else '#dc3545' if val == O else '#666'
        btn.style.button_color = '#FFF9C4' if val != EMPTY else '#FFF9C4'
        btn.disabled = (val != EMPTY or game.terminal())

def display_game_end(game, out, status_label):
    """Hiển thị thông báo kết thúc trò chơi (thắng/hòa)."""
    win = game.winner()
    if win:
        winner = "Bạn" if win == game.user else "AI"
        color = "green" if win == game.user else "red"
        status_label.value = f"🎉 {winner} thắng!"
        msg = f"<h2 style='color:{color}; text-align:center; font-size:36px'>🎉 {winner} THẮNG!</h2>"
    else:
        status_label.value = "🤝 Hòa!"
        msg = "<h2 style='color:#fd7e14; text-align:center; font-size:36px'>🤝 HÒA!</h2>"
    with out:
        clear_output()
        display(HTML(msg))

def display_initial_ui(n_slider, player_choice, difficulty_choice, start_button, restart_button, status_label, grid_container, out):
    """Hiển thị toàn bộ giao diện trò chơi."""
    display(HTML("<h1 style='text-align:center; color:#1976D2; font-family:Arial Black'>🎮 TIC-TAC-TOE</h1>"))
    display(HTML("<p style='text-align:center; font-size:18px; color:#666'> Alpha-Beta Pruning ✨</p>"))

    display(widgets.VBox([
        widgets.HBox([n_slider, player_choice, difficulty_choice], layout=widgets.Layout(justify_content='center', margin='15px', align_items='center')),
        widgets.HBox([start_button], layout=widgets.Layout(justify_content='center')),
        status_label,
        grid_container,
        out,
        widgets.HBox([restart_button], layout=widgets.Layout(justify_content='center', margin='20px 0 10px 0'))
    ]))
