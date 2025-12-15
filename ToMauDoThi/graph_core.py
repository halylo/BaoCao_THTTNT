import networkx as nx
import random
import numpy as np

# ======================
# GREEDY COLORING
# ======================
def greedy_coloring(G):
    """
    Thực hiện thuật toán tô màu tham lam (Greedy Coloring)
    với chiến lược 'largest_first' (ưu tiên đỉnh có bậc lớn nhất).
    Trả về một dictionary: {đỉnh: màu}.
    """
    # largest_first: tô màu các đỉnh theo thứ tự giảm dần của bậc (degree).
    # Đây là một chiến lược heuristic được sử dụng trong NetworkX.
    return nx.greedy_color(G, strategy='largest_first')

# ======================
# TẠO ĐỒ THỊ NGẪU NHIÊN
# ======================
def random_graph(n, p=0.5):
    """
    Tạo một đồ thị ngẫu nhiên theo mô hình Erdos-Renyi (G(n, p)).
    :param n: Số lượng đỉnh.
    :param p: Xác suất để tồn tại một cạnh giữa hai đỉnh bất kỳ.
    :return: Đối tượng nx.Graph.
    """
    G = nx.Graph()
    if n > 0:
        G.add_nodes_from(range(n))
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < p:
                    G.add_edge(i, j)
    return G

# ======================
# LẤY MA TRẬN KỀ
# ======================
def get_adjacency_matrix(G):
    """
    Trả về ma trận kề của đồ thị dưới dạng mảng numpy.
    """
    if G is None or G.number_of_nodes() == 0:
        return np.array([])
    return nx.to_numpy_array(G, dtype=int)
