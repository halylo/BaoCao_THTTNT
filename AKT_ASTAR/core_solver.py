import heapq
from abc import ABC, abstractmethod

# ----------- Class cơ sở ----------------
class PuzzleSolver(ABC):
    """
    Lớp cơ sở trừu tượng cho các thuật toán giải N-Puzzle.
    Cung cấp các thuộc tính chung và phương thức tìm láng giềng.
    """
    def __init__(self, size, start_state, goal_state):
        self.size = size
        self.n = size * size
        self.start_state = tuple(start_state)
        self.goal_state = tuple(goal_state)
        # self.visited được dùng để tránh lặp trạng thái trong tìm kiếm
        self.visited = set() 

    @abstractmethod
    def solve(self):
        """Phương thức giải cần được triển khai bởi các lớp con."""
        pass

    def get_neighbors(self, state):
        """Tìm tất cả các trạng thái láng giềng hợp lệ (bằng cách di chuyển ô trống)."""
        neighbors = []
        zero_index = state.index(0)
        row, col = divmod(zero_index, self.size)
        
        # Các bước di chuyển có thể (Lên, Xuống, Trái, Phải)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        
        for dx, dy in moves:
            new_row, new_col = row + dx, col + dy
            
            # Kiểm tra xem ô mới có nằm trong lưới không
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                new_index = new_row * self.size + new_col
                new_state = list(state)
                
                # Hoán đổi ô trống (0) với ô láng giềng
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                neighbors.append(tuple(new_state))
        return neighbors

# ----------- AKT (Tìm kiếm theo chiều sâu - DFS) ----------------
class AKT(PuzzleSolver):
    """
    Giải N-Puzzle bằng thuật toán Tìm kiếm theo chiều sâu (AKT/DFS).
    Sử dụng ngăn xếp (stack) để duyệt.
    """
    def solve(self):
        stack = [(self.start_state, [self.start_state])]
        self.visited.add(self.start_state)
        
        while stack:
            state, path = stack.pop()
            
            if state == self.goal_state:
                return path
            
            # Khám phá láng giềng
            for neighbor in self.get_neighbors(state):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        return None

# ----------- A* ----------------
class AStar(PuzzleSolver):
    """
    Giải N-Puzzle bằng thuật toán A*.
    Sử dụng hàm heuristic là Manhattan Distance để ước tính chi phí.
    """
    def heuristic(self, state):
        """Tính Manhattan Distance (khoảng cách giữa ô hiện tại và vị trí mục tiêu)."""
        distance = 0
        for i, value in enumerate(state):
            if value != 0:
                goal_index = self.goal_state.index(value)
                # Tọa độ hiện tại (x1, y1)
                x1, y1 = divmod(i, self.size) 
                # Tọa độ mục tiêu (x2, y2)
                x2, y2 = divmod(goal_index, self.size) 
                # Khoảng cách Manhattan: |x1 - x2| + |y1 - y2|
                distance += abs(x1 - x2) + abs(y1 - y2)
        return distance

    def solve(self):
        # Priority Queue: (f_score, g_score, state, path)
        h = self.heuristic(self.start_state)
        pq = [(h, 0, self.start_state, [self.start_state])]
        
        # g_score: Chi phí thực tế từ trạng thái bắt đầu đến trạng thái hiện tại
        g_score = {self.start_state: 0}
        
        # explored: Tập hợp các trạng thái đã được xử lý (đã pop ra khỏi PQ)
        explored = set()
        
        while pq:
            _, g, state, path = heapq.heappop(pq)
            
            if state == self.goal_state:
                return path
            
            if state in explored:
                continue
            explored.add(state)
            
            for neighbor in self.get_neighbors(state):
                tentative_g = g + 1 # Chi phí mới = chi phí cũ + 1 bước di chuyển
                
                # Kiểm tra trạng thái láng giềng
                # Nếu láng giềng đã được khám phá với chi phí tốt hơn, bỏ qua
                if neighbor in explored:
                    if tentative_g >= g_score.get(neighbor, float('inf')):
                        continue

                # Nếu đây là đường đi tốt hơn hoặc trạng thái mới
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor)
                    heapq.heappush(pq, (f, tentative_g, neighbor, path + [neighbor]))
        return None
