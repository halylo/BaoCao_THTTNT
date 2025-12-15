import networkx as nx
import matplotlib.pyplot as plt
import random
import ipywidgets as widgets
from IPython.display import display, clear_output
import networkx as nx

# Import các hàm từ các file khác
from graph_core import greedy_coloring, random_graph, get_adjacency_matrix
from graph_helper import (
    draw_graph,
    print_adjacency_matrix,
    print_coloring_info,
    get_graph_layout,
    DEFAULT_COLORS
)

# ======================
# BIẾN TOÀN CỤC VÀ KHỞI TẠO
# ======================
out_graph = widgets.Output()    # Chỉ dùng để hiển thị đồ thị
out_info = widgets.Output()     # Dùng để hiển thị thông tin một lần (ma trận, cạnh, coloring...)

G = None
color_dict = None
current_palette = []
pos = None  # Lưu layout để không thay đổi khi vẽ lại

# ======================
# THIẾT LẬP WIDGETS
# ======================
n_input = widgets.IntText(
    value=6,
    min=3,
    max=15,
    description="Số đỉnh:"
)

p_input = widgets.FloatSlider(
    value=0.5,
    min=0.1,
    max=1.0,
    step=0.1,
    description="Xác suất cạnh:",
    style={'description_width': 'initial'}
)

gen_btn = widgets.Button(
    description="Tạo đồ thị & tô màu",
    button_style='success'
)

color_picker_box = widgets.VBox()
status = widgets.Label(value="Sẵn sàng! Điều chỉnh thông số rồi nhấn nút để bắt đầu.")

# ======================
# HÀM XỬ LÝ SỰ KIỆN
# ======================
def on_generate(b):
    """Xử lý sự kiện khi nút 'Tạo đồ thị & tô màu' được nhấn."""
    global G, color_dict, current_palette, pos

    # Xóa thông tin cũ
    with out_info:
        clear_output()
    with out_graph:
        clear_output()

    n = n_input.value
    p = p_input.value

    with out_info:
        print("Đang tạo đồ thị ngẫu nhiên...\n")

    # 1. TẠO ĐỒ THỊ & TÔ MÀU (Gọi từ graph_core)
    G = random_graph(n, p=p)
    color_dict = greedy_coloring(G)
    num_colors = max(color_dict.values()) + 1 if G.nodes else 0

    # 2. TÍNH TOÁN LAYOUT (Gọi từ graph_helper)
    pos = get_graph_layout(G)

    # 3. HIỂN THỊ THÔNG TIN (Gọi từ graph_helper)
    with out_info:
        clear_output(wait=True)
        print(f"Đồ thị ngẫu nhiên: {n} đỉnh, xác suất cạnh p = {p}")

        print_adjacency_matrix(get_adjacency_matrix(G))
        print_coloring_info(G, color_dict)
        print("\nBạn có thể thay đổi màu bên dưới – đồ thị sẽ cập nhật ngay lập tức mà không làm mất thông tin này.")

    # 4. TẠO COLOR PICKER
    pickers = []
    current_palette = []
    for i in range(num_colors):
        color_hex = DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
        cp = widgets.ColorPicker(
            concise=False,
            description=f"Màu {i}:",
            value=color_hex
        )
        # Sử dụng lambda để đảm bảo cp được capture đúng giá trị trong vòng lặp
        cp.observe(on_color_change, names='value')
        pickers.append(cp)
        current_palette.append(color_hex)

    color_picker_box.children = pickers

    # 5. Vẽ đồ thị lần đầu
    update_graph()

def on_color_change(change):
    """Xử lý sự kiện khi một ColorPicker thay đổi giá trị."""
    global current_palette
    # Cập nhật lại palette từ tất cả ColorPicker
    current_palette = [cp.value for cp in color_picker_box.children]
    update_graph()

def update_graph():
    """Hàm riêng chỉ để vẽ lại đồ thị – không in thêm bất kỳ text nào."""
    if G is None:
        return

    with out_graph:
        clear_output(wait=True)
        #   Gọi hàm vẽ từ graph_helper
        draw_graph(G, color_dict, current_palette, pos)

# Gắn sự kiện
gen_btn.on_click(on_generate)

# ======================
# HIỂN THỊ GIAO DIỆN CHÍNH
# ======================
def run_app():
    """Hàm chạy chính để hiển thị tất cả widgets."""
    display(widgets.HTML("<h2>🎨 Tô màu đồ thị – Greedy Coloring (NetworkX)</h2>"))
    display(widgets.HTML("<p><strong>Thông tin đồ thị (ma trận kề, cạnh, kết quả tô màu) chỉ hiển thị một lần khi tạo mới.</strong><br>Khi thay đổi màu: chỉ cập nhật đồ thị bên dưới.</p>"))

    display(widgets.HBox([n_input, p_input]))
    display(gen_btn)
    display(status)
    display(out_info) # Thông tin chi tiết (chỉ in 1 lần)
    display(widgets.HTML("<hr><h3>Điều chỉnh màu:</h3>"))
    display(color_picker_box)
    display(widgets.HTML("<h3>Đồ thị:</h3>"))
    display(out_graph) # Chỉ hiển thị đồ thị, cập nhật liên tục khi đổi màu

    status.value = "Sẵn sàng! Nhấn nút để tạo đồ thị mới."

if __name__ == '__main__':
    # Đảm bảo bạn chạy hàm này trong môi trường Jupyter/Colab
    run_app()
