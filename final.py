import tkinter as tk
import random
from tkinter import messagebox
import time

specified_cells = [
    (0, 0), (0, 1), (0, 2), (0, 6), (0, 7), (0, 8),
    (1, 0), (1, 1), (1, 2), (1, 6), (1, 7), (1, 8),
    (2, 0), (2, 1), (2, 2), (2, 6), (2, 7), (2, 8),
    (3, 3), (3, 4), (3, 5),
    (4, 3), (4, 4), (4, 5),
    (5, 3), (5, 4), (5, 5),
    (6, 0), (6, 1), (6, 2), (6, 6), (6, 7), (6, 8),
    (7, 0), (7, 1), (7, 2), (7, 6), (7, 7), (7, 8),
    (8, 0), (8, 1), (8, 2), (8, 6), (8, 7), (8, 8)
]

class SudokuSolver:
    def __init__(self):
        self.variables = {(i, j): list(range(1, 10)) for i in range(9) for j in range(9)}
        self.arcs = []
        self.create_arcs()

    def add_arc(self, var1, var2):
        self.arcs.append((var1, var2))
        self.arcs.append((var2, var1))

    def create_arcs(self):
        for i in range(9):
            for j in range(9):
                # Add arcs for rows
                for k in range(9):
                    if k != j:
                        self.add_arc((i, j), (i, k))
                # Add arcs for columns
                for k in range(9):
                    if k != i:
                        self.add_arc((i, j), (k, j))
                # Add arcs for 3x3 subgrids
                row_start, col_start = (i // 3) * 3, (j // 3) * 3
                for k in range(row_start, row_start + 3):
                    for l in range(col_start, col_start + 3):
                        if k != i and l != j:
                            self.add_arc((i, j), (k, l))

    def revise(self, var1, var2):
        revised = False
        domain_var1 = self.variables[var1][:]
        for val1 in domain_var1:
            if not any(self.is_consistent(val1, val2) for val2 in self.variables[var2]):
                self.variables[var1].remove(val1)
                revised = True
        return revised

    def is_consistent(self, val1, val2):
        return val1 != val2
    
    def print_domains(self):
     for i in range(9):
        for j in range(9):
            print(f"Cell ({i}, {j}) Domain:", self.variables[(i, j)])


    def apply_arc_consistency(self,entries):
        
        solver = SudokuSolver()
        initial_board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = entries[i][j].get()
                if val.isdigit() and 0 < int(val) < 10:
                    row.append(int(val))
                else:
                    row.append(-1)
            initial_board.append(row)

        if not is_valid_initial_board(initial_board):
            messagebox.showinfo("Sudoku Solver", "Enter a valid initial board!")
            return

        for _ in range(9):
            solver.variables = {(i, j): list(range(1, 10)) for i in range(9) for j in range(9)}
            for i in range(9):
                for j in range(9):
                    if initial_board[i][j] != -1:
                        solver.variables[(i, j)] = [initial_board[i][j]]
            if solver.apply_arc_consistency():
                solver.print_domains() 
                break

        for i in range(9):
            for j in range(9):
                if initial_board[i][j] == -1:
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, str(solver.variables[(i, j)][0]))
                    entries[i][j].config(state="readonly")
        
         

        def update_domain(self, var):
            updated_domain = []
            for val in self.variables[var]:
                if self.is_consistent_assignment(var, val):
                    updated_domain.append(val)
            self.variables[var] = updated_domain

        def is_consistent_assignment(self, var, val):
            for neighbor in self.arcs:
                if neighbor[1] == var:
                    if len(self.variables[neighbor[0]]) == 1 and self.variables[neighbor[0]][0] == val:
                        return False
            return True

    def solve_sudoku_backtracking(self):
        if all(len(domain) == 1 for domain in self.variables.values()):
            return True  # Puzzle solved

        var = min((var for var, domain in self.variables.items() if len(domain) > 1), key=lambda x: len(self.variables[x]))
        for value in self.variables[var]:
            if self.is_consistent_assignment(var, value):
                self.variables[var] = [value]
                if self.apply_arc_consistency():
                    if self.solve_sudoku_backtracking():
                        return True
                self.variables[var] = [value]  # Reset the variable if the solution fails
        return False  # No solution found

#########################################################################################################################################
def open_mode_window():
    mode_window = tk.Toplevel(root)
    mode_window.title("Select Mode")

    mode_label = tk.Label(mode_window, text="Please select a mode:")
    mode_label.pack()

    mode1_button = tk.Button(mode_window, text="Mode 1", bg="blue", fg="white", command=lambda: start_game(1))
    mode1_button.pack(pady=10)

    mode2_button = tk.Button(mode_window, text="Mode 2", bg="blue", fg="white", command=lambda: start_game(2))
    mode2_button.pack(pady=10)

    mode2_button = tk.Button(mode_window, text="Interactive Mode", bg="blue", fg="white", command=lambda: start_game(3))
    mode2_button.pack(pady=10)



def open_mode2_window(show_difficulty=True):
    mode2_window = tk.Toplevel(root)
    mode2_window.title("Select Difficulty")

    mode2_label = tk.Label(mode2_window, text="Select Difficulty Level:")
    mode2_label.pack()

    easy_button = tk.Button(mode2_window, text="Easy", bg="green", fg="white", command=lambda: start_game(2, "easy"))
    easy_button.pack(pady=5)

    medium_button = tk.Button(mode2_window, text="Medium", bg="yellow", fg="black", command=lambda: start_game(2, "medium"))
    medium_button.pack(pady=5)

    hard_button = tk.Button(mode2_window, text="Hard", bg="red", fg="white", command=lambda: start_game(2, "hard"))
    hard_button.pack(pady=5)

    extra_hard_button = tk.Button(mode2_window, text="Extra Hard", bg="purple", fg="white", command=lambda: start_game(2, "extra_hard"))
    extra_hard_button.pack(pady=5)

    if not show_difficulty:
        mode2_window.after(10000, mode2_window.destroy)  # Close the window after 100ms if show_difficulty is False


def open_mode3_window(show_difficulty=False):
    mode3_window = tk.Toplevel(root)
    mode3_window.title("Select Difficulty")

    mode3_label = tk.Label(mode3_window, text="Select Difficulty Level:")
    mode3_label.pack()

    easy_button = tk.Button(mode3_window, text="Easy", bg="green", fg="white", command=lambda: start_game(3, "easy"))
    easy_button.pack(pady=5)

    medium_button = tk.Button(mode3_window, text="Medium", bg="yellow", fg="black", command=lambda: start_game(3, "medium"))
    medium_button.pack(pady=5)

    hard_button = tk.Button(mode3_window, text="Hard", bg="red", fg="white", command=lambda: start_game(3, "hard"))
    hard_button.pack(pady=5)

    extra_hard_button = tk.Button(mode3_window, text="Extra Hard", bg="purple", fg="white", command=lambda: start_game(3, "extra_hard"))
    extra_hard_button.pack(pady=5)

    if not show_difficulty:
        mode3_window.after(10000, mode3_window.destroy)  # Close the window after 100ms if show_difficulty is False


def start_game(mode, difficulty=None):
    if mode == 1:
        start_mode_1()
    elif mode == 2:
        open_mode2_window(show_difficulty=False)  # Show the difficulty window initially
        if difficulty == "easy":
            start_mode_2(30)  # You can adjust the number of empty places for each difficulty level
        elif difficulty == "medium":
            start_mode_2(40)
        elif difficulty == "hard":
            start_mode_2(50)
        elif difficulty == "extra_hard":
            start_mode_2(60)
    elif mode == 3:
        open_mode3_window(show_difficulty=False)  # Show the difficulty window initially
        if difficulty == "easy":
            start_mode_3(30)  # You can adjust the number of empty places for each difficulty level
        elif difficulty == "medium":
            start_mode_3(40)
        elif difficulty == "hard":
            start_mode_3(50)
        elif difficulty == "extra_hard":
            start_mode_3(60)

##############################################################################################################################

#mode 1 is working by solve sudoku with csp validations (no arc consistency)

def start_mode_1():
    global entries
    mode1_window = tk.Toplevel(root)
    mode1_window.title("Sudoku Solver")

    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = tk.Entry(mode1_window, width=3, justify="center", font=("Arial", 14))
            entry.grid(row=i, column=j)
            row_entries.append(entry)
        entries.append(row_entries)

    for i, j in specified_cells:
        entries[i][j].config(borderwidth=2, relief="solid")

    solve_button = tk.Button(mode1_window, text="Solve", command=lambda: solve_sudoku_gui(entries))
    solve_button.grid(row=9, columnspan=9)


##############################################################################################################################

#mode 2 is working by arc consistency

def start_mode_2(num_empty):
    global entries
    mode2_window = tk.Toplevel(root)
    mode2_window.title("Sudoku Solver - Mode 2")
    solver=SudokuSolver()
    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = tk.Entry(mode2_window, width=3, justify="center", font=("Arial", 14))
            entry.grid(row=i, column=j)
            row_entries.append(entry)
        entries.append(row_entries)

    for i, j in specified_cells:
        entries[i][j].config(borderwidth=2, relief="solid")

    initial_board = generate_initial_board(num_empty)

    for i in range(9):
        for j in range(9):
            if initial_board[i][j] != -1:
                entries[i][j].insert(0, str(initial_board[i][j]))
                entries[i][j].config(state="readonly")

    solve_button = tk.Button(mode2_window, text="Solve", command=lambda: solve_sudoku_gui(entries))
    solve_button.grid(row=9, columnspan=9)

    solver.apply_arc_consistency(entries)  # Apply arc consistency after generating the initial board

##############################################################################################################################

#mode 3 is working by solve sudoku with csp validations (no arc consistency)

def start_mode_3(num_empty):
    global entries
    mode3_window = tk.Toplevel(root)
    mode3_window.title("Sudoku Game - Mode 3")

    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = tk.Entry(mode3_window, width=3, justify="center", font=("Arial", 14))
            entry.grid(row=i, column=j)
            row_entries.append(entry)
        entries.append(row_entries)

    for i, j in specified_cells:
        entries[i][j].config(borderwidth=2, relief="solid")

    initial_board = generate_initial_board(num_empty)
    
    for i in range(9):
        for j in range(9):
            if initial_board[i][j] != -1:
                entries[i][j].insert(0, str(initial_board[i][j]))
                entries[i][j].config(state="readonly")

    solved_sudoku=solve_sudoku_mode3(entries)
    print(solved_sudoku)


    check_button = tk.Button(mode3_window, text="Check", command=lambda: check_board(entries, solved_sudoku))
    check_button.grid(row=9, columnspan=9)
##############################################################################################################################

def check_board(entries, agent_solution):
    user_solution = []
    for i in range(9):
        row = []
        for j in range(9):
            val = entries[i][j].get()
            if val.isdigit() and 0 < int(val) < 10:
                row.append(int(val))
            else:
                row.append(-1)  # Use -1 for empty cells
        user_solution.append(row)

    valid = True
    for i in range(9):
        for j in range(9):
            if user_solution[i][j] != agent_solution[i][j]:
                valid = False
                entries[i][j].config(bg="red")
            else:
                entries[i][j].config(bg="light green")

    if valid:
        messagebox.showinfo("Sudoku Game", "Congratulations! Your solution is correct.")
    else:
        messagebox.showerror("Sudoku Game", "Oops! Your solution is not correct. Keep trying!")


##############################################################################################################################


def generate_initial_board(num_empty):
    while True:
        solved_board = [[(i * 3 + (i // 3) + j + 1) % 9 + 1 for j in range(9)] for i in range(9)]
        random.shuffle(solved_board)

        initial_board = [row[:] for row in solved_board]
        for _ in range(num_empty):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while initial_board[row][col] == -1:
                row, col = random.randint(0, 8), random.randint(0, 8)
            initial_board[row][col] = -1

        if is_valid_initial_board(initial_board):
            return initial_board

##############################################################################################################################

def solve_sudoku_mode3(entries):
    global solved
    solved = False  # Reset the global variable

    def find_next_empty(puzzle):
        for r in range(9):
            for c in range(9):
                if puzzle[r][c] == -1:
                    return r, c
        return None, None

    def is_valid(puzzle, guess, row, col):
        row_vals = puzzle[row]
        if guess in row_vals:
            return False

        col_vals = [puzzle[i][col] for i in range(9)]
        if guess in col_vals:
            return False

        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if puzzle[r][c] == guess:
                    return False

        return True

    def is_complete(puzzle):
        for row in puzzle:
            if -1 in row:
                return False
        return True
    
    def solve(puzzle):
        if is_complete(puzzle):
            return True
        row, col = find_next_empty(puzzle)
        if row is None:
            return True
        
        for guess in range(1, 10):
            if is_valid(puzzle, guess, row, col):
                puzzle[row][col] = guess
                if solve(puzzle):
                    return True
                puzzle[row][col] = -1
        return False
    
    puzzle = []
    for i in range(9):
        row = []
        for j in range(9):
            val = entries[i][j].get()
            if val.isdigit() and 0 < int(val) < 10:
                row.append(int(val))
            else:
                row.append(-1)
        puzzle.append(row)

    if not is_valid_initial_board(puzzle):
        messagebox.showinfo("Sudoku Solver", "Enter a valid initial board!")
        return None

    solve(puzzle)

    if not solved:
        messagebox.showinfo("Sudoku Solver", "No solution exists!")

    return puzzle

##############################################################################################################################

def solve_sudoku_gui(entries):
    global solved
    solved = False
    solve_sudoku(entries)

def solve_sudoku(entries):
    global solved
    solved = False  # Reset the global variable

    def find_next_empty(puzzle):
        for r in range(9):
            for c in range(9):
                if puzzle[r][c] == -1:
                    return r, c
        return None, None

    def is_valid(puzzle, guess, row, col):
        row_vals = puzzle[row]
        if guess in row_vals:
            return False

        col_vals = [puzzle[i][col] for i in range(9)]
        if guess in col_vals:
            return False

        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if puzzle[r][c] == guess:
                    return False

        return True

    def is_complete(puzzle):
        for row in puzzle:
            if -1 in row:
                return False
        return True
    
    

    def print_domains(puzzle):
     for row in range(9):
        for col in range(9):
            if puzzle[row][col] == -1:
                domain = [guess for guess in range(1, 10) if is_valid(puzzle, guess, row, col)]
                print(f"Cell ({row}, {col}) Domain:", domain)

    def solve(entries):
     def solve_helper(puzzle):
        if is_complete(puzzle):
            return True
        row, col = find_next_empty(puzzle)
        if row is None:
            solved = True
            return True 

        for guess in range(1, 10):
            if is_valid(puzzle, guess, row, col):
                puzzle[row][col] = guess
                entries[row][col].delete(0, tk.END)
                entries[row][col].insert(0, str(guess))
                entries[row][col].update()
                entries[row][col].config(bg="lightgreen")
                root.update()
                time.sleep(0.1)  # Delay for visualization

                print(f"Removing domain for cell ({row}, {col}): {guess}")
                print_domains(puzzle)

                if solve_helper(puzzle):
                    return True
                puzzle[row][col] = -1
                entries[row][col].delete(0, tk.END)
                entries[row][col].config(bg="white")
                root.update()
                time.sleep(0.1)  # Delay for visualization
        return False

     print("Initial Domains:")
     print_domains(puzzle)
    
     return solve_helper(puzzle)


    puzzle = []
    for i in range(9):
        row = []
        for j in range(9):
            val = entries[i][j].get()
            if val.isdigit() and 0 < int(val) < 10:
                row.append(int(val))
            else:
                row.append(-1)
        puzzle.append(row)

    if not is_valid_initial_board(puzzle):
        messagebox.showinfo("Sudoku Solver", "Enter a valid initial board!")
        return

    solve(entries)

    if not solved:
        messagebox.showinfo("Sudoku Solver", "No solution exists!")
##############################################################################################################################

def is_valid_initial_board(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != -1:
                guess = puzzle[i][j]
                puzzle[i][j] = -1
                if not is_valid(puzzle, guess, i, j):
                    return False
                puzzle[i][j] = guess
    return True

def is_valid(puzzle, guess, row, col):
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    return True
####################################################################################################
root = tk.Tk()
root.title("Sudoku Game")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Select Mode", command=open_mode_window)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

root.mainloop()










# unsolvable board:
# 1   2   3      x   x   x        x   x   x   
# x   x   x      x   4   x        x   x   x
# x   x   x      x   x   x        x   x   4