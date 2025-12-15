import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
# Import các lớp và hàm từ các file đã tạo
from core_solver import AKT, AStar 
from helper_widgets import board_to_html, create_input_grids, get_state 

# ----------- Biến toàn cục ----------------
path = None
current_size = 3
input_boxes_start = []
input_boxes_goal = []

out = widgets.Output()
solution_out = widgets.Output()
algorithm_label = widgets.Label(value="", layout=widgets.Layout(padding="10px 0"), style={'font_weight': 'bold', 'font_size': '20px', 'color': '#1565C0'})

# ----------- Chọn kích thước ----------------
size_selector = widgets.Dropdown(
    options=[('3x3 (8-Puzzle)', 3), ('4x4 (15-Puzzle)', 4)],
    value=3,
    description='Kích thước:',
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='300px')
)

input_container = widgets.Output()

def update_input_grids(size):
    """Cập nhật lưới input khi kích thước thay đổi."""
    global input_boxes_start, input_boxes_goal
    input_widget, start_boxes, goal_boxes = create_input_grids(size)
    
    # Cập nhật biến toàn cục
    input_boxes_start = start_boxes
    input_boxes_goal = goal_boxes
    
    with input_container:
        clear_output()
        display(input_widget)

# Khởi tạo lưới input ban đầu
update_input_grids(current_size)

def on_size_change(change):
    """Xử lý sự kiện khi kích thước được chọn thay đổi."""
    global current_size
    current_size = change['new']
    update_input_grids(current_size)
    with solution_out: 
        clear_output()
    algorithm_label.value = ""

size_selector.observe(on_size_change, names='value')

# ----------- Nút giải (đẹp hơn) ----------------
btn_style = widgets.ButtonStyle(font_weight='bold')
btn_layout = widgets.Layout(width='300px', height='60px', margin='15px')

btn_akt = widgets.Button(description="🔍 Giải bằng AKT (DFS)", button_style='info', layout=btn_layout, style=btn_style)
btn_astar = widgets.Button(description="⭐ Giải bằng A*", button_style='success', layout=btn_layout, style=btn_style)

# CSS cho hiệu ứng hover của nút
display(HTML("""
<style>
.hover-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
}
</style>
"""))

btn_akt.add_class("hover-button")
btn_astar.add_class("hover-button")

# ----------- Logic Giải ----------------
def solve(algo_name, solver_class):
    """Hàm chính thực hiện việc giải bài toán."""
    global path
    # Lấy trạng thái từ input boxes (sử dụng helper function)
    start = get_state(input_boxes_start)
    goal  = get_state(input_boxes_goal)

    if not start or not goal:
        with solution_out:
            clear_output()
            display(HTML(f"<h3 style='color:#D32F2F; text-align:center; background:#FFEBEE; padding:20px; border-radius:12px;'>"
                         f"⚠️ Lỗi: Trạng thái không hợp lệ!<br>"
                         f"Phải chứa đúng các số từ 0 đến {current_size**2 - 1}, mỗi số xuất hiện đúng một lần.</h3>"))
        return

    with solution_out:
        clear_output()
        display(HTML("<h3 style='text-align:center; color:#424242;'>⏳ Đang tìm lời giải bằng <b>{}</b>...</h3>".format(algo_name)))

    try:
        solver = solver_class(current_size, start, goal)
        path = solver.solve()
    except Exception as e:
        with solution_out:
            clear_output()
            algorithm_label.value = f"❌ {algo_name} — Đã xảy ra lỗi!"
            display(HTML(f"<h3 style='color:#D32F2F; text-align:center; background:#FFEBEE; padding:30px; border-radius:16px;'>"
                         f"⚠️ Lỗi trong quá trình giải: {e}</h3>"))
        return


    with solution_out:
        clear_output()
        if path:
            steps = len(path) - 1
            algorithm_label.value = f"✅ {algo_name} — Tìm thấy lời giải trong {steps} bước!"
            steps_html = "<div style='display:flex; flex-wrap:wrap; justify-content:center; gap:25px; margin:30px 0;'>"
            for i, state in enumerate(path):
                title = "Bước 0 (Trạng thái ban đầu)" if i == 0 else f"Bước {i}" if i < len(path)-1 else "Trạng thái đích (Goal)"
                is_start = (i == 0)
                is_goal = (i == len(path)-1)
                
                # Hiển thị bảng (sử dụng helper function)
                steps_html += board_to_html(state, current_size, title, is_start=is_start, is_goal=is_goal).data
                if i < len(path)-1:
                    steps_html += "<div style='align-self:center; font-size:48px; color:#90A4AE;'>➜</div>"
            steps_html += "</div>"
            display(HTML(f"<h2 style='text-align:center; color:#1565C0; margin:30px 0;'>Các bước giải ({steps} bước)</h2>"))
            display(HTML(steps_html))
        else:
            algorithm_label.value = f"❌ {algo_name} — Không tìm thấy lời giải!"
            display(HTML("<h3 style='color:#D32F2F; text-align:center; background:#FFEBEE; padding:30px; border-radius:16px;'>"
                         "Không tồn tại đường đi từ trạng thái ban đầu đến trạng thái đích.<br>"
                         "(Có thể do tính chẵn lẻ của hoán vị không khớp)</h3>"))

btn_akt.on_click(lambda b: solve("AKT (DFS)", AKT))
btn_astar.on_click(lambda b: solve("A*", AStar))

# ----------- Giao diện chính ----------------
display(HTML("""
<h1 style='text-align:center; color:#1565C0; font-family:Arial, sans-serif; margin:40px 0;'>
    🧩 N-PUZZLE SOLVER
</h1>
<h3 style='text-align:center; color:#424242; margin-bottom:40px;'>
    Giải bài toán 8-Puzzle (3x3) hoặc 15-Puzzle (4x4) bằng AKT (DFS) hoặc A*
</h3>
"""))

display(widgets.HBox([widgets.Label("Chọn kích thước:", style={'font_size':'18px', 'font_weight':'bold'}), size_selector],
                     layout=widgets.Layout(justify_content='center', margin='20px 0')))

display(input_container)

display(widgets.HBox([btn_akt, btn_astar], layout=widgets.Layout(justify_content='center')))

display(algorithm_label)
display(solution_out)
