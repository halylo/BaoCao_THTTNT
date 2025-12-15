import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

# ----------- Hiển thị bảng bằng HTML (Đã chỉnh sửa để đồng nhất với hình ảnh) ----------------
def board_to_html(state, size, title="", is_start=False, is_goal=False):
    """
    Chuyển trạng thái bảng (tuple) thành HTML để hiển thị đẹp mắt,
    đồng nhất với giao diện hình ảnh (khung viền màu, nền ô trắng).
    """
    cell_size = "80px" if size == 3 else "65px"
    
    # Thiết lập màu sắc dựa trên trạng thái
    if is_start:
        border_color = "#2196F3" 
        title_color = "#1565C0"
    elif is_goal:
        border_color = "#4CAF50"  
        title_color = "#2E7D32"
    else:
        border_color = "#BDBDBD" 
        title_color = "#424242"
    
    shadow = "0 2px 4px rgba(0,0,0,0.1)"
    
    html = f"<div style='text-align:center; margin:15px; font-family:Arial, sans-serif;'>"
    if title:
        html += f"<h4 style='color:{title_color}; margin:8px 0 12px; font-size:18px; font-weight:bold;'>{title}</h4>"

    # Khung bao ngoài với border màu
    html += f"<div style='display:inline-block; border:3px solid {border_color}; border-radius:4px; padding:10px; box-shadow:{shadow}; background-color:#FFFFFF;'>"
    html += f"<table style='border-collapse:collapse; border-spacing:0;'>"
    for i in range(0, len(state), size):
        html += "<tr>"
        for val in state[i:i+size]:
            # Cài đặt ô: Nền trắng, viền xám, chữ đen (như trong hình ảnh)
            if val == 0:
                bg = "transparent" # Ô trống
                text = ""
                border = "1px solid #757575" 
            else:
                bg = "#FFFFFF" 
                text = f"<span style='font-size:28px; font-weight:bold; color:#000000;'>{val}</span>" 
                border = "1px solid #757575" 
            
            html += f"<td style='width:{cell_size}; height:{cell_size}; background:{bg}; color:black; text-align:center; border:{border}; padding:0;'>{text}</td>"
        html += "</tr>"
    html += "</table></div></div>"
    return HTML(html)

# ----------- Tạo lưới input (Đã chỉnh sửa để đồng nhất với hình ảnh) ----------------
def create_input_grids(size):
    """
    Tạo lưới các ô input cho Trạng thái ban đầu và Trạng thái đích.
    Trả về các widget HBox (layout) và danh sách các ô input (global).
    """
    n = size * size
    cell_size_px = "80px" if size == 3 else "65px"

    input_box_layout = widgets.Layout(
        width=cell_size_px,
        height=cell_size_px,
        margin='0px', 
        border='1px solid #757575' 
    )
    input_box_style = {'font_size': '24px', 'font_weight': 'bold', 'text_align': 'center', 'background': '#FFFFFF', 'text_color': '#000000'}

    input_boxes_start = [widgets.BoundedIntText(value=0, min=0, max=n-1, layout=input_box_layout, style=input_box_style) for _ in range(n)]
    input_boxes_goal  = [widgets.BoundedIntText(value=0, min=0, max=n-1, layout=input_box_layout, style=input_box_style) for _ in range(n)]

    # Giá trị mặc định (sử dụng giá trị từ hình ảnh)
    if size == 3:
        default_start = [1, 2, 3, 4, 5, 0, 6, 7, 8]
        default_goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    else:
        default_start = list(range(1, n))
        default_start.insert(n//2 + size//2, 0)
        default_goal = list(range(1, n)) + [0]


    for i, v in enumerate(default_start): input_boxes_start[i].value = v % n if i < len(default_start) else 0
    for i, v in enumerate(default_goal): input_boxes_goal[i].value = v

    grid_layout = widgets.Layout(
        grid_template_columns=f"repeat({size}, {cell_size_px})",
        justify_content='center',
        gap='0px', 
        padding='0px',
    )
    grid_start = widgets.GridBox(input_boxes_start, layout=grid_layout)
    grid_goal  = widgets.GridBox(input_boxes_goal, layout=grid_layout)
    
    # Viền ngoài màu xanh dương/xanh lá
    start_border = '3px solid #2196F3' 
    goal_border = '3px solid #4CAF50' 

    start_card = widgets.VBox([
        widgets.HTML("<h3 style='color:#1565C0; margin-bottom:10px; text-align:center;'>Trạng thái ban đầu</h3>"),
        grid_start
    ], layout=widgets.Layout(align_items='center', padding='10px', border=start_border, border_radius='4px', background_color='#FFFFFF', margin='10px'))

    goal_card = widgets.VBox([
        widgets.HTML("<h3 style='color:#2E7D32; margin-bottom:10px; text-align:center;'>Trạng thái đích</h3>"),
        grid_goal
    ], layout=widgets.Layout(align_items='center', padding='10px', border=goal_border, border_radius='4px', background_color='#FFFFFF', margin='10px'))

    return widgets.HBox([start_card, goal_card], layout=widgets.Layout(justify_content='center', margin='30px 0')), input_boxes_start, input_boxes_goal

def get_state(boxes):
    """Lấy giá trị từ các ô input và kiểm tra tính hợp lệ của trạng thái."""
    vals = [b.value for b in boxes]
    expected = list(range(len(vals)))
    if sorted(vals) != expected or vals.count(0) != 1:
        return None
    return tuple(vals)
