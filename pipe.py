# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 49:
# 103368 Vasco Pereira
# 96843 Bernardo Nunes

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):

        depth = (
            len(self.board.get_pieces_to_be_considered()) - len(other.board.get_pieces_to_be_considered())
        )

        if depth != 0:
            return depth < 0

        return self.id < other.id

    def place(self, row, col, piece) -> "PipeManiaState":
        return PipeManiaState(self.board.change_piece_value(row, col, piece))

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, board) -> None:
        self.board = board
        self.size = len(board)
        self.possible_moves_per_piece = {}
        self.pieces_to_be_considered = []
        self.actions_num = 0

    # debug
    def print(self) -> str:
        return "\n".join(["\t".join(row) for row in self.board])

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0:
            return (
                None,
                self.board[1][col],
            )

        if row == self.size - 1:
            return (
                self.board[row - 1][col],
                None,
            )

        return (self.board[row - 1][col], self.board[row + 1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            return (
                None,
                self.board[row][1],
            )

        if col == self.size - 1:
            return (
                self.board[row][col - 1],
                None,
            )

        return (self.board[row][col - 1], self.board[row][col + 1])

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        data = [line.strip("\n\r").split("\t") for line in sys.stdin]

        return Board(data).calculate_state()
    
    def calculate_state(self):
        
        for row in range(self.size):
            for col in range(self.size):
                possibilities = self.calculate_possibilities(row, col)
                self.board[row][col] =  possibilities[0]
                length = len(possibilities)
                self.actions_num += length

                if length == 1:
                    self.possible_moves_per_piece[(row,col)] = ()
                    self.actions_num -= 1

                elif length < 4:
                    self.possible_moves_per_piece[(row, col)] = possibilities
                    self.pieces_to_be_considered.insert(0, (row, col))

                else:
                    self.possible_moves_per_piece[(row, col)] = possibilities
                    self.pieces_to_be_considered.append((row, col))

        
        for row in range(self.size):
            for col in range(self.size):
                if self.possible_moves_per_piece[(row, col)] == ():
                    self.filter_possibilities(row, col)
                        
        
        
        return self
    
    def has_up_pipe(self, piece):
        if piece in ("FC", "BC", "BE", "BD", "VC", "VD", "LV"):
            return 1
        return 0
    
    def has_right_pipe(self, piece):
        if piece in ("FD", "BC", "BD", "BB", "VB", "VD", "LH"):
            return 1
        return 0
    
    def has_down_pipe(self, piece):
        if piece in ("FB", "BB", "BE", "BD", "VB", "VE", "LV"):
            return 1
        return 0
        
    def has_left_pipe(self, piece):
        if piece in ("FE", "BC", "BE", "BB", "VC", "VE", "LH"):
            return 1
        return 0
    
    def filter_possibilities(self, row, col):

        piece = self.get_value(row, col)
        aux = ()
        
        if (row - 1, col) in self.pieces_to_be_considered and self.possible_moves_per_piece[(row - 1, col)] != ():
            if self.has_up_pipe(piece):
            
                    possibilities = self.possible_moves_per_piece[(row - 1, col)]

                    for action in possibilities:
                        if self.has_down_pipe(action):
                            aux = aux + (action,)
            else:
                for possibility in self.possible_moves_per_piece[(row - 1, col)]:
                     if possibility not in ("FB", "BB", "BE", "BD", "VB", "VE", "LV"):
                          aux = aux + (possibility,)
        
            old_length = len(self.possible_moves_per_piece[(row - 1, col)])
            new_length = len(aux)

            self.possible_moves_per_piece[(row - 1, col)] = aux

            if (old_length != new_length and new_length != 0) or new_length == 1:
                    
                    
                self.actions_num -= old_length - new_length
                if new_length == 1:
                    self.board[row - 1][col] = self.possible_moves_per_piece[(row - 1, col)][0]
                    self.possible_moves_per_piece[(row - 1, col)] = ()
                    self.pieces_to_be_considered.remove((row - 1, col))
                    self.filter_possibilities(row - 1, col)
                    
                            
        aux = ()

        if (row , col + 1) in self.pieces_to_be_considered and self.possible_moves_per_piece[(row , col + 1)] != ():

            if self.has_right_pipe(piece):
            
                    possibilities = self.possible_moves_per_piece[(row, col + 1)]

                    for action in possibilities:
                        if self.has_left_pipe(action):
                            aux = aux + (action,)

            else:
                for possibility in self.possible_moves_per_piece[(row, col + 1)]:
                    if possibility not in ("FE", "BC", "BE", "BB", "VC", "VE", "LH"):
                        aux = aux + (possibility,)
        
            old_length = len(self.possible_moves_per_piece[(row, col + 1)])
            new_length = len(aux)

            self.possible_moves_per_piece[(row, col + 1)] = aux

            if (old_length != new_length and new_length != 0) or new_length == 1:
                    
                    
                self.actions_num -= old_length - new_length
                if new_length == 1:
                    self.board[row][col + 1] = self.possible_moves_per_piece[(row, col + 1)][0]
                    self.possible_moves_per_piece[(row, col + 1)] = ()
                    self.pieces_to_be_considered.remove((row, col + 1))
                    self.filter_possibilities(row, col + 1)

        
        aux = ()

        if (row + 1 , col) in self.pieces_to_be_considered and self.possible_moves_per_piece[(row + 1, col)] != ():
            if self.has_down_pipe(piece):
           
                    possibilities = self.possible_moves_per_piece[(row + 1, col)]

                    for action in possibilities:
                        if self.has_up_pipe(action):
                            aux = aux + (action,)
            else:
                for possibility in self.possible_moves_per_piece[(row + 1, col)]:
                    if possibility not in ("FC", "BC", "BE", "BD", "VC", "VD", "LV"):
                        aux = aux + (possibility,)
        
            old_length = len(self.possible_moves_per_piece[(row + 1, col)])
            new_length = len(aux)

            self.possible_moves_per_piece[(row + 1, col)] = aux

            if (old_length != new_length and new_length != 0) or new_length == 1:
                    
                    
                self.actions_num -= old_length - new_length
                if new_length == 1:
                    self.board[row + 1][col] = self.possible_moves_per_piece[(row + 1, col)][0]
                    self.possible_moves_per_piece[(row + 1, col)] = ()
                    self.pieces_to_be_considered.remove((row + 1, col))
                    self.filter_possibilities(row + 1, col)
                

                
       
        aux = ()

        if (row, col - 1) in self.pieces_to_be_considered and self.possible_moves_per_piece[(row, col - 1)] != ():
            if self.has_left_pipe(piece):
           
                    possibilities = self.possible_moves_per_piece[(row, col - 1)]

                    for action in possibilities:
                        if self.has_right_pipe(action):
                            aux = aux + (action,)
            else:
                for possibility in self.possible_moves_per_piece[(row, col - 1)]:
                    if possibility not in ("FD", "BC", "BD", "BB", "VB", "VD", "LH"):
                        aux = aux + (possibility,)
        
            old_length = len(self.possible_moves_per_piece[(row, col - 1)])
            new_length = len(aux)

            self.possible_moves_per_piece[(row, col - 1)] = aux

            if (old_length != new_length and new_length != 0) or new_length == 1:
                    
                    
                self.actions_num -= old_length - new_length
                if new_length == 1:
                    self.board[row][col - 1] = self.possible_moves_per_piece[(row, col - 1)][0]
                    self.possible_moves_per_piece[(row, col - 1)] = ()
                    self.pieces_to_be_considered.remove((row, col - 1))
                    self.filter_possibilities(row, col - 1)
       
    def change_piece_value(self, row, col, piece):

        aux = [row[:] for row in self.board]
        aux[row][col] = piece
        
        new_board = Board(aux)
        new_board.possible_moves_per_piece = self.possible_moves_per_piece
        new_board.actions_num = self.actions_num
        
        if len(new_board.possible_moves_per_piece[(row, col)])  ==  1:
                new_board.pieces_to_be_considered = self.pieces_to_be_considered[1:]
                new_board.possible_moves_per_piece[(row, col)] = ()
                new_board.actions_num -= 1
                new_board.filter_possibilities(row, col)
        
        elif self.possible_moves_per_piece[(row, col)][-1] == piece:
                new_board.pieces_to_be_considered = self.pieces_to_be_considered[1:]
                new_board.possible_moves_per_piece[(row, col)] = ()
                new_board.actions_num -= 1
                new_board.filter_possibilities(row, col)
        
        return new_board

    def get_size(self):
        return self.size

    #Da return a todos os valores possiveis que um tipo de peca pode tomar
    def get_all_possibilities(self, row, col):
        type = self.get_value(row, col)[0]
        possibilities = {
            "F": ("FC", "FB", "FE", "FD"),
            "B": ("BC", "BB", "BE", "BD"),
            "V": ("VC", "VB", "VE", "VD"),
            "L": ("LH", "LV")
        }
        return possibilities.get(type, ())
      
    #Verifica a posicao da peca e da return aos valores que a peca pode tomar
    def calculate_possibilities(self, row, col):
        type = self.board[row][col][0]
        #Cantos
        corners = ((0,0), (0,  self.size - 1), (self.size - 1, 0), (self.size - 1, self.size - 1))

        if (row, col) in corners:
            if row == 0 and col == 0:
                if type == "F":
                    return ("FD","FB")
                if type == "V":
                    return ("VB",)
            elif row == 0 and col == self.size - 1:
                if type == "F":
                    return ("FB","FE")
                if type == "V":
                    return ("VE",)
            elif row == self.size - 1 and col == 0:
                if type == "F":
                    return ("FC","FD")
                if type == "V":
                    return ("VD",)
            elif row == self.size - 1 and col == self.size - 1:
                if type == "F":
                    return ("FC","FE")
                if type == "V":
                    return ("VC",)
        #Primeira coluna        
        elif col == 0:
            if type == "F":
                return ("FB","FC","FD")
            elif type == "V":
                return ("VB","VD")
            elif type == "L":
                return ("LV",)
            elif type == "B":
                return ("BD",)
        #Ultima coluna
        elif col == self.size - 1:
            if type == "F":
                return ("FB","FC","FE")
            elif type == "V":
                return ("VC","VE")
            elif type == "L":
                return ("LV",)
            elif type == "B":
                return ("BE",)
        #Primeira linha
        elif row == 0:
            if type == "F":
                return ("FB","FE","FD")
            elif type == "V":
                return ("VB","VE")
            elif type == "L":
                return ("LH",)
            elif type == "B":
                return ("BB",)
        #Ultima linha
        elif row == self.size - 1:
            if type == "F":
                return ("FC","FE","FD")
            elif type == "V":
                return ("VC","VD")
            elif type == "L":
                return ("LH",)
            elif type == "B":
                return ("BC",)
        else:
            #Casos restantes
            return self.get_all_possibilities(row, col)
        
    def get_pieces_to_be_considered(self):
        return self.pieces_to_be_considered
    
    def pieces_with_2_or_more_options(self):
        ret = 0
        for possibilities in self.possible_moves_per_piece:
            if len(self.possible_moves_per_piece[possibilities]) > 1:
                ret += 1
        
        return ret

    def get_possible_moves_per_piece(self):
        return self.possible_moves_per_piece
    
    def get_possible_moves_for_piece(self, row, col):
        return self.possible_moves_per_piece[(row, col)]
    
    def get_next_piece(self):
            return self.pieces_to_be_considered[0]
    
    def get_actions_num(self):
        return self.actions_num

    # TODO: outros metodos da classe

class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = PipeManiaState(board)
        super().__init__(state)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if len(state.board.get_pieces_to_be_considered()) == 0:
            return []
        
        row, col = state.board.get_next_piece()

        possibilities = state.board.get_possible_moves_for_piece(row, col)

        return map(lambda piece: (row, col, piece), possibilities)
    
        
    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        row, col, new_piece = action
        
        return state.place(row, col, new_piece)
        
    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        return len(state.board.get_pieces_to_be_considered()) == 0

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
    
        return node.state.board.get_actions_num()

    # TODO: outros metodos da classe


if __name__ == "__main__":

    # Ler grelha do figura 1a:
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem) #ou greedy
    # Verificar se foi atingida a solução
    print(goal_node.state.board.print(), sep="")
