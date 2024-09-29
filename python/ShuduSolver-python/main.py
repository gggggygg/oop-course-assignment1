import pygame
import sys

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Grid:
    # 初始化一个9x9的方格为0
    def __init__(self, grid_size=9):
        self.GRID_SIZE = grid_size
        self.BOX_SIZE = 3
        self.grid = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]

    # 得到方格的特定行
    def get_row(self, row):
        return self.grid[row]

    # 得到方格的特定列
    def get_col(self, col):
        return [self.grid[i][col] for i in range(self.GRID_SIZE)]

    # 得到一个3x3的子方格
    def get_box(self, row, col):
        box = []
        box_row_start = (row // self.BOX_SIZE) * self.BOX_SIZE
        box_col_start = (col // self.BOX_SIZE) * self.BOX_SIZE
        for i in range(self.BOX_SIZE):
            for j in range(self.BOX_SIZE):
                box.append(self.grid[box_row_start + i][box_col_start + j])
        return box

    # 对方格的对应索引位置赋值
    def set_value(self, row, col, value):
        self.grid[row][col] = value


class Sudoku(Grid):
    #继承grid类
    def __init__(self, input_str):
        super().__init__()
        self.parse(input_str)

    #解析字符串输入，反串行化
    def parse(self, input_str):
        index = 0
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                self.grid[i][j] = int(input_str[index])
                index += 1

    #推理函数
    def get_inference(self, row, col):
        if self.grid[row][col] != 0:#如果该位置已赋值，直接return
            return []

        used = [False] * 10 #记录已在行、列和框中使用的数字
        for num in self.get_row(row) + self.get_col(col) + self.get_box(row, col): #标记已在行、列和框中使用的数字
            used[num] = True

        possible_values = [i for i in range(1, 10) if not used[i]] #枚举所有未在行、列和框中使用的数字
        return possible_values

#界面交互类
class SudokuGame:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.width = 450
        self.height = 500
        self.cell_size = self.width // sudoku.GRID_SIZE
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sudoku Solver") ## 创建 "Solve" 按钮
        self.font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 20)  # 候选值字体应较小
        self.selected = None
        self.running = True
        self.candidates = None
        self.button_rect = pygame.Rect(150, 460, 150, 30)  # 创建 "Solve" 按钮

    #界面绘制
    def draw_grid(self):
        for row in range(self.sudoku.GRID_SIZE):
            for col in range(self.sudoku.GRID_SIZE):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                if self.selected == (row, col):
                    pygame.draw.rect(self.screen, BLUE, rect)
                else:
                    pygame.draw.rect(self.screen, WHITE, rect)

                pygame.draw.rect(self.screen, BLACK, rect, 1)

                # 显示数值
                if self.sudoku.grid[row][col] != 0:
                    value = self.sudoku.grid[row][col]
                    text = self.font.render(str(value), True, BLACK)
                    self.screen.blit(text, (col * self.cell_size + 20, row * self.cell_size + 10))
                elif self.candidates:
                    # 显示可能值
                    self.draw_candidates(row, col, self.candidates[row][col])

        # 绘制线条
        for i in range(0, self.width, self.cell_size * 3):
            pygame.draw.line(self.screen, BLACK, (i, 0), (i, self.height - 50), 4)
            pygame.draw.line(self.screen, BLACK, (0, i), (self.width, i), 4)

    def draw_candidates(self, row, col, candidates):
        # 在每个空单元格内绘制较小的候选数字
        if candidates:
            x_offset = col * self.cell_size + 5
            y_offset = row * self.cell_size + 5
            for i, value in enumerate(candidates):
                text = self.small_font.render(str(value), True, GREY)
                self.screen.blit(text, (x_offset + (i % 3) * 15, y_offset + (i // 3) * 15))

    def draw_button(self):
        # 绘制求解按钮
        pygame.draw.rect(self.screen, GREY, self.button_rect)
        text = self.font.render("Solve", True, BLACK)
        self.screen.blit(text, (self.button_rect.x + 25, self.button_rect.y + 5))

    def select_cell(self, row, col):
        self.selected = (row, col)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row = pos[1] // self.cell_size
            col = pos[0] // self.cell_size

            if self.button_rect.collidepoint(pos):
                self.solve_grid()
            elif row < self.sudoku.GRID_SIZE and col < self.sudoku.GRID_SIZE:
                self.select_cell(row, col)

        if event.type == pygame.KEYDOWN and self.selected:
            row, col = self.selected
            if event.key == pygame.K_1:
                self.sudoku.set_value(row, col, 1)
            elif event.key == pygame.K_2:
                self.sudoku.set_value(row, col, 2)
            elif event.key == pygame.K_3:
                self.sudoku.set_value(row, col, 3)
            elif event.key == pygame.K_4:
                self.sudoku.set_value(row, col, 4)
            elif event.key == pygame.K_5:
                self.sudoku.set_value(row, col, 5)
            elif event.key == pygame.K_6:
                self.sudoku.set_value(row, col, 6)
            elif event.key == pygame.K_7:
                self.sudoku.set_value(row, col, 7)
            elif event.key == pygame.K_8:
                self.sudoku.set_value(row, col, 8)
            elif event.key == pygame.K_9:
                self.sudoku.set_value(row, col, 9)

    # 求解
    def solve_grid(self):

        self.candidates = [[self.sudoku.get_inference(row, col) for col in range(self.sudoku.GRID_SIZE)]
                           for row in range(self.sudoku.GRID_SIZE)]

        # 检查是否无解
        for row in range(self.sudoku.GRID_SIZE):
            for col in range(self.sudoku.GRID_SIZE):
                if not self.candidates[row][col] and self.sudoku.grid[row][col] == 0:
                    self.show_error_dialog("No Solution available for cell: {}, {}".format(row, col))
                    return

    def show_error_dialog(self, message):
        error_font = pygame.font.SysFont(None, 30)
        error_surface = pygame.Surface((300, 150))
        error_surface.fill(RED)
        text_surface = error_font.render(message, True, WHITE)
        self.screen.blit(error_surface, (self.width // 2 - 150, self.height // 2 - 75))
        self.screen.blit(text_surface, (self.width // 2 - 140, self.height // 2 - 30))
        pygame.display.flip()
        pygame.time.delay(2000)  # 显示2秒后继续

    def run(self):
        while self.running:
            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_button()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__=="__main__":
    # 输入
    input_str = "300967001040302080020000070070000090000873000500010003004705100905000207800621004"

    # 创建实例
    sudoku = Sudoku(input_str)
    game = SudokuGame(sudoku)

    # 运行
    game.run()
