# core.py - Logic Trò chơi và AI (Alpha-Beta Pruning có Heuristic)

import copy
import math
import random

# Định nghĩa các hằng số
X = "X"
O = "O"
EMPTY = " "

class TicTacToeNXN:
    """
    Lớp chứa logic cốt lõi của trò chơi Tic-Tac-Toe NxN,
    bao gồm các thuật toán Alpha-Beta Pruning.
    """
    def __init__(self, n=3, user=None, ai=None):
        self.n = n
        self.board = [[EMPTY for _ in range(n)] for _ in range(n)]
        self.user = user
        self.ai = ai

    def copy(self):
        new = TicTacToeNXN(self.n, self.user, self.ai)
        new.board = copy.deepcopy(self.board)
        return new

    def player_turn(self):
        """Xác định lượt chơi hiện tại (X hoặc O). X luôn đi trước."""
        count = sum(1 for row in self.board for cell in row if cell != EMPTY)
        return X if count % 2 == 0 else O

    def actions(self):
        """Trả về danh sách các nước đi hợp lệ (vị trí trống)."""
        return [(i, j) for i in range(self.n) for j in range(self.n) if self.board[i][j] == EMPTY]

    def result(self, action):
        """Trả về trạng thái trò chơi mới sau khi thực hiện nước đi."""
        game = self.copy()
        i, j = action
        game.board[i][j] = self.player_turn()
        return game

    def winner(self):
        """Kiểm tra và trả về người chiến thắng (X hoặc O) nếu có."""
        # Kiểm tra hàng, cột, đường chéo (Full N liên tiếp để thắng)
        for i in range(self.n):
            if self.board[i][0] != EMPTY and all(self.board[i][j] == self.board[i][0] for j in range(self.n)):
                return self.board[i][0]
        for j in range(self.n):
            if self.board[0][j] != EMPTY and all(self.board[i][j] == self.board[0][j] for i in range(self.n)):
                return self.board[0][j]

        # Đường chéo chính
        if self.board[0][0] != EMPTY and all(self.board[i][i] == self.board[0][0] for i in range(self.n)):
            return self.board[0][0]

        # Đường chéo phụ
        if self.board[0][self.n-1] != EMPTY and all(self.board[i][self.n-1-i] == self.board[0][self.n-1] for i in range(self.n)):
            return self.board[0][self.n-1]

        return None

    def terminal(self):
        """Kiểm tra trạng thái kết thúc trò chơi."""
        return self.winner() is not None or not self.actions()

    def utility(self):
        """Tính giá trị tiện ích cho trạng thái cuối (AI thắng: 1, User thắng: -1, Hòa: 0)."""
        win = self.winner()
        if win == self.ai: return 1
        if win == self.user: return -1
        return 0

    # === Hàm Heuristic để đánh giá trạng thái không kết thúc ===
    def evaluate(self):
        """
        Hàm Heuristic: Đánh giá sức mạnh của bảng hiện tại (non-terminal state).
        Điểm thưởng/phạt cho các hàng/cột/đường chéo gần thắng (N-1, N-2 quân).
        """
        score = 0
        lines = []

        # Lấy tất cả các đường (hàng, cột, đường chéo)
        for r in range(self.n):
            lines.append([self.board[r][c] for c in range(self.n)])
        for c in range(self.n):
            lines.append([self.board[r][c] for r in range(self.n)])
        lines.append([self.board[i][i] for i in range(self.n)]) # Chéo chính
        lines.append([self.board[i][self.n-1-i] for i in range(self.n)]) # Chéo phụ

        for line in lines:
            ai_count = line.count(self.ai)
            user_count = line.count(self.user)
            empty_count = line.count(EMPTY)

            # Bỏ qua các đường đã bị chặn hoàn toàn
            if ai_count > 0 and user_count > 0:
                continue

            # Đánh giá cho AI (Maximizing Player)
            if ai_count > 0:
                if ai_count == self.n - 1 and empty_count >= 1:
                    score += 1000  # Ngay lập tức thắng
                elif ai_count == self.n - 2 and empty_count >= 2:
                    score += 50   # Tạo thế 2 nước nữa thắng
                elif ai_count == 1 and empty_count == self.n - 1:
                    score += 1

            # Đánh giá cho Người chơi (Minimizing Player) - Cần chặn
            if user_count > 0:
                if user_count == self.n - 1 and empty_count >= 1:
                    score -= 1000 # Cần chặn gấp
                elif user_count == self.n - 2 and empty_count >= 2:
                    score -= 50   # Khả năng người chơi sắp thắng

        return score

    # === Alpha-Beta Giới hạn độ sâu (Sử dụng Heuristic) ===

    def alpha_beta_limited(self, depth, cur_depth=0, alpha=-math.inf, beta=math.inf, maximizing=True):
        if self.terminal():
            # Trạng thái kết thúc: Trả về utility với giá trị rất lớn để ưu tiên tuyệt đối
            return self.utility() * 1000000

        if cur_depth >= depth:
            # Đạt giới hạn độ sâu: Trả về Heuristic
            return self.evaluate()

        if maximizing:
            max_eval = -math.inf
            for a in self.actions():
                score = self.result(a).alpha_beta_limited(depth, cur_depth+1, alpha, beta, False)
                max_eval = max(max_eval, score)
                alpha = max(alpha, max_eval)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = math.inf
            for a in self.actions():
                score = self.result(a).alpha_beta_limited(depth, cur_depth+1, alpha, beta, True)
                min_eval = min(min_eval, score)
                beta = min(beta, min_eval)
                if beta <= alpha: break
            return min_eval

    # === Hàm Alpha-Beta Full đã bị loại bỏ vì quá chậm, chỉ giữ lại để tham khảo (nếu cần) ===
    def alpha_beta_full(self, alpha=-math.inf, beta=math.inf, maximizing=True):
        # KHÔNG SỬ DỤNG HÀM NÀY cho N >= 4. Giữ lại nếu N=3
        if self.terminal():
            return self.utility() * 1000000

        # ... (code Alpha-Beta Full) ...
        pass


    def get_best_move(self, difficulty):
        """Tính toán và trả về nước đi tối ưu cho AI dựa trên độ khó."""
        if difficulty == "Dễ":
            return random.choice(self.actions()) if self.actions() else None

        maximizing_player = (self.player_turn() == self.ai)
        best_val = -math.inf
        best_move = None

        # Thiết lập giới hạn độ sâu (Depth Limit) cho Heuristic Search
        if difficulty == "Trung bình":
            depth_limit = 4
        elif difficulty == "Khó":
            # Tăng độ sâu cho độ khó cao, cân bằng giữa tốc độ và độ sâu chiến thuật
            depth_limit = 6

        if self.n > 4 and difficulty == "Khó":
             # Giảm độ sâu nếu kích thước quá lớn để tránh timeout
            depth_limit = 4

        if not self.actions():
            return None

        # Sử dụng Alpha-Beta giới hạn cho cả 2 độ khó (trừ Dễ)
        for a in self.actions():
            val = self.result(a).alpha_beta_limited(depth_limit, 1, maximizing=not maximizing_player)

            # Cập nhật nước đi tốt nhất
            if val > best_val or best_move is None:
                best_val = val
                best_move = a
        return best_move
