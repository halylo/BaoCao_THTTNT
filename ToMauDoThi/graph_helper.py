import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Palette mặc định từ Matplotlib
DEFAULT_COLORS = [mcolors.to_hex(c) for c in plt.cm.tab10.colors]

# ======================
# VẼ ĐỒ THỊ
# ======================
def draw_graph(G, color_dict, palette, pos):
    """
    Vẽ đồ thị với màu sắc và layout đã cho.
    :param G: Đối tượng nx.Graph.
    :param color_dict: Dictionary {đỉnh: màu_id}.
    :param palette: Danh sách các mã màu (hex) tương ứng với màu_id.
    :param pos: Dictionary layout vị trí của các đỉnh.
    """
    if G is None or not G.nodes():
        return

    # Tạo danh sách màu cho mỗi đỉnh dựa trên color_dict và palette
    node_colors = [palette[color_dict[v]] for v in G.nodes()]
    num_colors = len(palette)

    plt.figure(figsize=(8, 6))
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=900,
        font_size=16,
        font_color='white',
        edge_color='gray',
        linewidths=2
    )
    plt.title(f"Đồ thị sau khi tô màu ({num_colors} màu)")
    plt.show()

# ======================
# TÍNH LAYOUT
# ======================
def get_graph_layout(G, seed=42):
    """
    Tính toán layout (vị trí) của các đỉnh.
    Dùng seed để đảm bảo layout không đổi.
    """
    if G is None or not G.nodes():
        return {}
    return nx.spring_layout(G, seed=seed)

# ======================
# IN MA TRẬN KỀ
# ======================
def print_adjacency_matrix(A):
    """
    In ma trận kề (numpy array) ra console.
    """
    if A.size == 0:
        print("Ma trận kề rỗng.")
        return

    n = A.shape[0]
    print("\nMa trận kề (Adjacency Matrix):")
    # In chỉ mục cột
    print("   ", " ".join([f"{i:3}" for i in range(n)]))
    # In từng hàng với chỉ mục hàng
    for i in range(n):
        row = " ".join([f"{A[i][j]:3}" for j in range(n)])
        print(f"{i:2}  {row}")

# ======================
# IN THÔNG TIN TÔ MÀU
# ======================
def print_coloring_info(G, color_dict):
    """
    In thông tin chi tiết về kết quả tô màu.
    """
    if G is None or not G.nodes():
        print("Đồ thị rỗng. Không có thông tin tô màu.")
        return

    num_colors = max(color_dict.values()) + 1 if color_dict else 0

    print("Kết quả Greedy Coloring (largest_first):")
    for v in sorted(color_dict):
        print(f"Đỉnh {v} → Màu {color_dict[v]}")
    print(f"\n👉 Số màu sử dụng: {num_colors}")

    # In chi tiết các cạnh và thông tin cơ bản
    print(f"\nSố cạnh: {G.number_of_edges()}")
    print("Danh sách cạnh:")
    if G.edges():
        for u, v in sorted(G.edges()):
            print(f"  ({u} — {v})")
    else:
        print("  (Không có cạnh nào)")
