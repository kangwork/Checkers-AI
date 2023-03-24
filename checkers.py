import sys
from queue import PriorityQueue, LifoQueue
from copy import deepcopy
import time
import heapq
from typing import Tuple

"""
In case it is not working for the best correctness,
please uncomment line 103 please, to use a given simple heuristic function.
"""

input_filename = sys.argv[1]
output_filename = sys.argv[2]
#
# input_filename = "input6.txt"
# output_filename = "output.txt"

start = time.time()
input_string = []

with open(input_filename, 'r') as input_file:
    for line in input_file:
        row_i = [x for x in line.rstrip()]
        input_string.extend(row_i)
# input_string = ['.', '.', '.', '.', '.', '.', '.', '.',
#                 '.', '.', '.', '.', 'b', '.', '.', '.',
#                 '.', '.', '.', '.', '.', '.', '.', 'R',
#                 '.', '.', 'b', '.', 'b', '.', '.', '.',
#                 '.', '.', '.', 'b', '.', '.', '.', 'r',
#                 '.', '.', '.', '.', '.', '.', '.', '.',
#                 '.', '.', '.', 'r', '.', '.', '.', '.',
#                 '.', '.', '.', '.', 'B', '.', '.', '.']
# input_string = "B.b.B.B.........b.B.B.B.........R.R.r.R.........R.R.r.R........r"
# input_string = ".....r...b................b.................b........R.........."
#
#
# def convert(string):
#     lis = []
#     for letter in string:
#         lis.append(letter)
#     return lis


# input_string = convert(input_string)
# debugging

# RED_WINS = 'red wins'
# RED_LOSES = 'red loses'
# NOT_END = 'ongoing game'
MAX = 1  # player red
MIN = -1  # player black
MAX_DEPTH = 8


# -------------------------------------------
def heuristic_function(state) -> int:
    score = 0
    for red_p in state.red:
        y, x = red_p
        if y == 7:
            score += 1  # keeping a black piece away from being a king
        if y == 3 or y == 4:
            if 2 <= x <= 5:
                score += 2
            else:
                score += 1.5
        if (y+1, x-1) in state.red and (y+1, x+1) in state.red:
            score += 10
            if 2 <= x <= 5:
                score += 2
            if 3 <= x <= 4:
                score += 4
        if state.red[red_p] == 'r':
            score += 4
        else:
            score += 8
    score += (state.stable_minus_risk_red()) * 3
    return score

# ------------ another heuristic -------------

def complex_heuristic_red(state) -> int:
    score = 0
    for red_p in state.red:
        if red_p[0] == 7:
            score += 1  # keeping a black piece away from being a king
        if red_p[0] == 3 or red_p[0] == 4:
            if 2 <= red_p[1] <= 5:
                score += 2
            else:
                score += 1.5
        if state.red[red_p] == 'r':
            score += 4
        else:
            score += 8
    score += (state.stable_minus_risk_red()) * 3
    return score


def complex_heuristic_black(state) -> int:
    score = 0
    for b in state.black:
        if b[0] == 0:
            score += 1  # keeping a black piece away from being a king
        if b[0] == 3 or b[0] == 4:
            if 2 <= b[1] <= 5:
                score += 2
            else:
                score += 1.5
        if state.black[b] == 'b':
            score += 4
        else:
            score += 8
    score += (state.stable_minus_risk_black()) * 3
    return score


def complex_heuristic(state) -> int:
    return complex_heuristic_red(state)-complex_heuristic_black(state)

# ------------------------------------------ah


def h_for_no(move) -> int:
    """Less score the best, as it will be picked first."""
    if move.captured_piece_pos is None:
        score = 0
    else:  # the longer, the better for min&max
        score = 2 * len(move.captured_piece_pos)
    y, x = move.new_pos
    if 2 < y < 5 and 1 < x < 6:
        score += 21
    if move.past_player == MAX:  # if sth only benefits MAX put under here
        if y == 7:
            score += 2
        if y == 0:
            score += 3
        if y < 4:
            score += 2
    else:  # MIN
        if y == 7:
            score += 3
        if y == 0:
            score += 2
        elif y > 3:
            score += 2
    return -score  # as it is minheap
    # MAX need the greatest h_for_no value to be explored first, but by the
    # property of (min)heap, we need to use the opposite signed values.



def terminal(state) -> bool:
    """
    Determine if the game is ended, i.e., no successor or no block
    :return: True if the game has ended, False otherwise
    """
    if not state.black or not state.red:
        return True
    elif not state.generate_possible_moves():
        return True
    return False


def get_player(state) -> int:
    if state.player is None:
        print("Oops, state player is None!!!")
    return state.player


def utility(state) -> int:
    """
    :return: a utility value of this state, i.e., Max's payoff
    """
    if not state.black or (state.player == MIN and not state.generate_possible_moves()):
        # state.utility = 250
        return 200  # upper bound
    elif not state.red or (state.player == MAX and not state.generate_possible_moves()):
        # state.utility = -250
        return -200
    utility_val = 0
    utility_val += complex_heuristic(state)
    # state.utility = utility_val
    return utility_val


def _simple_utility_function(state) -> int:
    """
    A simple utility function given on a quercus page
    :param state: State object that has a player, positions of red and black
                    pieces
    :return: the number of red pieces minus the number of pieces of the black,
                with each regular piece worth one point and each king worth 2.
    """
    utility = 0
    for red_p in state.red:
        if state.red[red_p] == 'R':  # if king, add one more
            utility += 1
        utility += 1
    for black_p in state.black:
        if state.black[black_p] == 'B':  # if king, add one more
            utility -= 1
        utility -= 1
    return utility


class Move(object):
    def __init__(self, past_board_state, old_pos, new_pos, captured_piece_pos=None, new_type=None):
        self.past_board_state = past_board_state
        self.past_player = past_board_state.player
        self.old_pos = old_pos
        self.new_pos = new_pos
        self.captured_piece_pos = captured_piece_pos
        self.new_type = new_type
        self.aftermove = None

    def __str__(self):
        string_rep = str(self.old_pos)
        if not self.captured_piece_pos:
            string_rep += " move to "
        else:
            string_rep += " jump to "
        string_rep += str(self.new_pos)
        return string_rep

    def __lt__(self, other):
        return h_for_no(self) < h_for_no(other)

    def set_aftermove(self):
        """
        :return: a state after the move
        """
        new_red = deepcopy(self.past_board_state.red)
        new_black = deepcopy(self.past_board_state.black)
        new_empty = deepcopy(self.past_board_state.empty)
        if self.past_player == MAX:
            if self.captured_piece_pos is not None:  # jump
                new_empty[self.old_pos] = '.'
                for cap_pos in self.captured_piece_pos:
                    new_black.pop(cap_pos)
                    new_empty[cap_pos] = '.'
            new_red.pop(self.old_pos)
            # new_red[self.new_pos] = new_red.pop(self.old_pos)
            new_empty[self.old_pos] = '.'
            new_red[self.new_pos] = self.new_type
            if new_red[self.new_pos] == 'r' and self.new_pos[0] == 0:
                new_red[self.new_pos] = 'R'
            new_empty.pop(self.new_pos)
        else:  # current player is MIN
            # new_black[self.new_pos] = new_black.pop(self.old_pos)
            new_black.pop(self.old_pos)
            new_empty[self.old_pos] = '.'
            new_black[self.new_pos] = self.new_type
            if new_black[self.new_pos] == 'b' and self.new_pos[0] == 7:
                new_red[self.new_pos] = 'B'
            new_empty.pop(self.new_pos)
            if self.captured_piece_pos is not None:
                for cap_pos in self.captured_piece_pos:
                    new_red.pop(cap_pos)
                    new_empty[cap_pos] = '.'
        new = State(self.past_board_state, new_red, new_black, new_empty)
        self.aftermove = new
        self.aftermove.set_player(-self.past_player)

    def __hash__(self):
        return int(str(self))

    def __eq__(self, other):  # may change this to str only, see if it is faster!!! 고쳐
        if str(self) == str(other):
            return True
        return False


class Board(object):
    """
    Precondition: If blocks is not given, red and black are not given.
                  If blocks is passed, then red and black are given, i.e.,
                  not None.  #고쳐 블락 안 쓰기로 함.

    -- instance variables --
    - self.blocks: a 8x8 nested list that has all the squares configuration
    - self.red: a dictionary that maps location tuple (y, x) of red piece to
                either 'r' or 'R' if exists.
    - self.black: a dictionary that maps location of red piece to either 'b' or
                'B' if exists.
    """
    def __init__(self, red=None, black=None, empty=None):
        if red is not None:
            self.red = red
            self.black = black
            self.empty = empty
        else:
            self.parent = None
            self.red = {}
            self.black = {}
            self.empty = {}

    def inverse_rep(self):
        inv = {'r': [], 'R': [], 'b': [], 'B': []}
        for red_p in self.red:
            if self.red[red_p] == 'R':
                inv['R'].append(red_p)
            else:
                inv['r'].append(red_p)
        for black_p in self.black:
            if self.black[black_p] == 'B':
                inv['B'].append(black_p)
            else:
                inv['b'].append(black_p)
        inv['r'] = sorted(inv['r'])
        inv['R'] = sorted(inv['R'])
        inv['b'] = sorted(inv['b'])
        inv['B'] = sorted(inv['B'])
        inv['r'] = [item for sublist in inv['r']  for item in sublist]
        inv['R'] = [item for sublist in inv['R']  for item in sublist]
        inv['b'] = [item for sublist in inv['b']  for item in sublist]
        inv['B'] = [item for sublist in inv['B']  for item in sublist]
        return inv

    def __str__(self):
        string_rep = ""
        inv = self.inverse_rep()
        for piece_type in inv:
            string_rep += ''.join(str(x) for x in inv[piece_type])
            string_rep += '8'
        return string_rep


class State(Board):
    def __init__(self, parent=None, red=None, black=None, empty=None):
        super().__init__(red, black, empty)
        self.parent = parent
        # self.utility = None
        self.player = None

    def __str__(self):
        if get_player(self) == MIN:
            return super().__str__()+"1"
        return super().__str__()

    def __hash__(self):
        return int(str(self))

    def set_player(self, player):
        self.player = player

    def is_stable(self, r_position) -> bool:
        """
        :param p: red piece position in tuple (y,x)
        :return: True if red is safe for all b and B, false otherwise
        """
        y, x = r_position
        if y == 7:  # ironmans(invincible)
            return True
        # even safe from B?
        if (y+1, x-1) in self.black and self.black[(y+1, x-1)] == 'B' and (y-1, x+1) in self.empty:
            return False
        if (y+1, x+1) in self.black and self.black[(y+1, x+1)] == 'B' and (y-1, x-1) in self.empty:
            return False
        # also safe from b?
        if (y+1, x+1) in self.empty and (y-1, x-1) in self.black:
            return False
        if (y+1, x-1) in self.empty and (y-1, x+1) in self.black:
            return False
        return True

    def is_stable(self, me, colour) -> bool:
        """
        Am I safe for now? i.e., no piece can kick me off in their single jump?
        :param self:
        :param me:
        :param colour:
        :return:
        """
        y, x = me
        if y == 0 or y == 7:
            return True
        if colour == 1:
            key = y+1
            O = 'B'
            opponents = self.black
        else:
            key = y-1
            O = 'R'
            opponents = self.red
        if (key, x-1) in self.empty:
            return False  # easily defeated by even pawns
        if (key, x+1) in self.empty:
            return False
        if (key, x-1) in opponents and opponents[((key, x-1))] == O:
            return False
        if (key, x+1) in opponents and opponents[((key, x+1))] == O:
            return False
        return True


    def can_be_beaten_by(self, me, colour) -> int:
        """
        'How many enemies can kick me?'
        :param self: state
        :param colour: my colour
        :return: number of enemies that can kick me off in a single jump
        """
        risk = 0
        y, x = me
        if y == 0 or y == 7:
            return False
        if colour == 1:
            key = y-1
            over_to = y+1
            opponents = self.black
        else:
            key = y+1
            over_to = y-1
            opponents = self.red
        if (key, x-1) in opponents and (over_to, x+1) in self.empty:
            return True
        if (key, x+1) in opponents and (over_to, x-1) in self.empty:
            return True
        return False

    def stable_minus_risk_red(self) -> int:
        stable_num = 0
        risk_score = 0
        for red_piece in self.red:
            stable_num += self.is_stable(red_piece, 1)
            risk_score += self.can_be_beaten_by(red_piece, 1)
        return stable_num - risk_score

    def stable_minus_risk_black(self) -> int:
        stable_num = 0
        risk_score = 0
        for black_p in self.black:
            stable_num += self.is_stable(black_p, -1)
            risk_score += self.can_be_beaten_by(black_p, -1)
        return stable_num - risk_score

    # Hints: Write a successors function which returns all the successive states
    # (which includes moves and successive board representations) for a given
    # player. Pay attention to which player should make a move for
    # min nodes and max nodes.
    def generate_possible_moves(self) -> heapq:
        """
        Generate available moves and return a list containing them.
        :return: list of possible moves
        """
        jump_moves = []
        heapq.heapify(jump_moves)
        non_jump_moves = []
        heapq.heapify(non_jump_moves)
        if self.player == MAX:  # if max, look at red
            for red_p in self.red:
                jumpablecont = self.red_piece_jumpable_to(red_p)
                if jumpablecont:  # not empty, i.e., is jumpable
                    for caps in jumpablecont:
                        old_pos, new_pos, piece_type = jumpablecont[caps]
                        new_move = Move(self, old_pos, new_pos, caps, piece_type)
                        # jump_moves.append(new_move)
                        heapq.heappush(jump_moves, new_move)
            if not jump_moves:
                for red_p in self.red:
                    movable_dic = self.red_piece_movable_to(red_p)
                    for new_pos in movable_dic:
                        old_pos = movable_dic[new_pos]
                        if self.red[old_pos] == 'R' or new_pos[0] == 0:
                            piece_type = 'R'
                        else:
                            piece_type = 'r'
                        new_move = Move(self, old_pos, new_pos, None, piece_type)
                        # non_jump_moves.append(new_move)
                        heapq.heappush(non_jump_moves, new_move)

        else:  # player is MIN, so we have to look at black pieces
            for black_p in self.black:
                # 44467780224466666801238001122246681
                jumpablecont = self.black_piece_jumpable_to(black_p)
                if jumpablecont:  # not empty, i.e., is jumpable
                    for caps in jumpablecont:
                        old_pos, new_pos, piece_type = jumpablecont[caps]
                        new_move = Move(self, old_pos, new_pos, caps, piece_type)
                        # jump_moves.append(new_move)
                        heapq.heappush(jump_moves, new_move)
            if not jump_moves:
                for black_p in self.black:
                    movable_dic = self.black_piece_movable_to(black_p)
                    for new_pos in movable_dic:
                        old_pos = movable_dic[new_pos]
                        if self.black[old_pos] == 'B' or new_pos[0] == 7:
                            piece_type = 'B'
                        else:
                            piece_type = 'b'
                        new_move = Move(self, old_pos, new_pos, None, piece_type)
                        # non_jump_moves.append(new_move)
                        heapq.heappush(non_jump_moves, new_move)

        if jump_moves:  # at least one jump available
            return jump_moves
        return non_jump_moves

    def red_piece_jumpable_to(self, pos=Tuple[int, int], king=None) -> dict[tuple, list]:
        """
        Precondition: 0 <= x, y <= 7, i.e., position pos is on the grid
        cont(CapturedtoOldposNewposType) maps captured positions to a list of
        old position, new position(the final desitination), and the type of the
        moving piece
        :param pos: position tuple(y, x) of the red piece
        :return: list of positions that the red tuple can jump to
        """
        cont = {}
        # jumpable_to = {}  # maps new position to current position and capturable opponent piece
        y, x = pos[0], pos[1]
        if king is None:
            king = self.red[pos]
        if king == 'R':  # if king: consider going down too
            if (y+1 <= 7 and x+1 <= 7 ) and (y+1, x+1) in self.black \
                    and (y+2, x+2) in self.empty:
                will_jump_to = (y+2, x+2)  # empty check 한 곳
                captured_pos = (y+1, x+1)  # black(opponent) check 한 곳
                cont[(captured_pos,)] = [pos, will_jump_to, 'R']
                # jumpable_to[will_jump_to]=[pos, [(y+1, x+1)], 'R']

                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.red.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.red[will_jump_to] = 'R'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.black.pop(captured_pos)  # 잡은 애 비우기 블랙인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 블랙인지 체크 한 애
                temp.player = MAX

                multi_capture = temp.red_piece_jumpable_to(will_jump_to, 'R')

                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))

            if (y+1 <= 7 and 0 <= x-1) and (y+1, x-1) in self.black and \
                    (y+2, x-2) in self.empty:

                will_jump_to = (y+2, x-2)  # empty check 한 곳
                captured_pos = (y+1, x-1)  # black(opponent) check 한 곳
                cont[(captured_pos,)] = [pos, will_jump_to, 'R']

                # jumpable_to[(y+2, x-2)] = [pos, [(y+1, x-1)], 'R']

                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.red.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.red[will_jump_to] = 'R'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.black.pop(captured_pos)  # 잡은 애 비우기 블랙인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 블랙인지 체크 한 애
                temp.player = MAX

                multi_capture = temp.red_piece_jumpable_to(will_jump_to, 'R')

                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))
        # pawn still needs to do:
        if (0 <= y-1 and 0 <= x-1) and (y-1, x-1) in self.black and \
                (y-2, x-2) in self.empty:

            will_jump_to = (y-2, x-2)  # empty check 한 곳
            captured_pos = (y-1, x-1)  # black(opponent) check 한 곳
            cont[(captured_pos,)] = [pos, will_jump_to, 'r']

            if y-2 == 0 or king == 'R':  # became king?
                cont[(captured_pos,)][2] = 'R'
                # stop looking at more multicap for just promoted king
            if king == 'R':
                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.red.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.red[will_jump_to] = 'R'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.black.pop(captured_pos)  # 잡은 애 비우기 블랙인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 블랙인지 체크 한 애
                temp.player = MAX

                multi_capture = temp.red_piece_jumpable_to(will_jump_to, 'R')

                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))

            else:

                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.red.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.red[will_jump_to] = 'r'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.black.pop(captured_pos)  # 잡은 애 비우기 블랙인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 블랙인지 체크 한 애
                temp.player = MAX

                multi_capture = temp.red_piece_jumpable_to(will_jump_to, 'r')

                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))

        if (0 <= y-1 and x+1 <= 7 ) and (y-1, x+1) in self.black and \
                (y-2, x+2) in self.empty:
            will_jump_to = (y-2, x+2)  # empty check 한 곳
            captured_pos = (y-1, x+1)  # black(opponent) check 한 곳
            cont[(captured_pos,)] = [pos, will_jump_to, 'r']
            if y-2 == 0 or king == 'R':  # became king?
                cont[(captured_pos,)][2] = 'R'
            if king == 'R':
                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.red.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.red[will_jump_to] = 'R'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.black.pop(captured_pos)  # 잡은 애 비우기 블랙인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 블랙인지 체크 한 애
                temp.player = MAX
                multi_capture = temp.red_piece_jumpable_to(will_jump_to, 'R')

                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))
            else:
                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.red.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.red[will_jump_to] = 'r'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.black.pop(captured_pos)  # 잡은 애 비우기 블랙인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 블랙인지 체크 한 애
                temp.player = MAX
                multi_capture = temp.red_piece_jumpable_to(will_jump_to, 'r')
                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))
        return cont

    def black_piece_jumpable_to(self, pos=Tuple[int, int], king=None) -> dict[tuple, list]:
        """
        Precondition: 0 <= x, y <= 7, i.e., position pos is on the grid
        :param pos: position tuple of the black piece
        :return: list of positions that the black piece can jump to
        """
        cont = {}
        # if str(self)=="44647782446606266813208040611222681" and pos == (1,3):
        #     print("here!")  # debugging
        # jumpable_to = {}  # maps new position to current position and capturable opponent piece
        y, x = pos[0], pos[1]
        if king is None:
            king = self.black[pos]
        if king == 'B':  # if king: consider going down too
            if (0 <= y-1 and 0 <= x-1 ) and (y-1, x-1) in self.red and \
                    (y-2, x-2) in self.empty:
                will_jump_to = (y-2, x-2)  # empty check 한 곳
                captured_pos = (y-1, x-1)  # red(opponent) check 한 곳
                cont[(captured_pos,)] = [pos, will_jump_to, 'B']

                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.black.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.black[will_jump_to] = 'B'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.red.pop(captured_pos)  # 잡은 애 비우기 레드인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 레드인지 체크 한 애
                temp.player = MIN
                multi_capture = temp.black_piece_jumpable_to(will_jump_to, 'B')
                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))

            if (0 <= y-1 and x+1 <= 7 ) and (y-1, x+1) in self.red and \
                    (y-2, x+2) in self.empty:
                will_jump_to = (y-2, x+2)  # empty check 한 곳
                captured_pos = (y-1, x+1)  # red(opponent) check 한 곳
                cont[(captured_pos,)] = [pos, will_jump_to, 'B']
                # jumpable_to[(y-2, x+2)] = [pos, [(y-1, x+1)], 'B']


                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.black.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.black[will_jump_to] = 'B'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.red.pop(captured_pos)  # 잡은 애 비우기 레드인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 레드인지 체크 한 애
                temp.player = MIN
                multi_capture = temp.black_piece_jumpable_to(will_jump_to, 'B')

                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))
        # if just pawn: BLACK
        if (y+1 <= 7 and x+1 <= 7 ) and (y+1, x+1) in self.red and \
                (y+2, x+2) in self.empty:
            will_jump_to = (y+2, x+2)  # empty check 한 곳
            captured_pos = (y+1, x+1)  # red(opponent) check 한 곳
            cont[(captured_pos,)] = [pos, will_jump_to, 'b']
            # jumpable_to[(y+2, x+2)] = [pos, [(y+1, x+1)], 'b']
            if y+2 == 7 or king == 'B':  # became king?
                cont[(captured_pos,)][2] = 'B'
            if king == 'B':
                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.black.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.black[will_jump_to] = 'B'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.red.pop(captured_pos)  # 잡은 애 비우기 레드인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 레드인지 체크 한 애
                temp.player = MIN
                multi_capture = temp.black_piece_jumpable_to(will_jump_to, 'B')

                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))
            else:  # still not king
                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.black.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.black[will_jump_to] = 'b'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.red.pop(captured_pos)  # 잡은 애 비우기 레드인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 레드인지 체크 한 애
                temp.player = MIN
                multi_capture = temp.black_piece_jumpable_to(will_jump_to, 'b')

                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))

        if (y+1 <= 7 and 0 <= x-1) and (y+1, x-1) in self.red and \
                (y+2, x-2) in self.empty:
            will_jump_to = (y+2, x-2) # empty check 한 곳
            captured_pos = (y+1, x-1)  # red(opponent) check 한 곳
            cont[(captured_pos,)] = [pos, will_jump_to, 'b']
            # jumpable_to[(y+2, x-2)] = [pos, [(y+1, x-1)], 'b']
            if y+2 == 7 or king == 'B':  # became king?
                cont[(captured_pos,)][2] = 'B'
            if king == 'B':
                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.black.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.black[will_jump_to] = 'B'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.red.pop(captured_pos)  # 잡은 애 비우기 레드인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 레드인지 체크 한 애
                temp.player = MIN
                multi_capture = temp.black_piece_jumpable_to(will_jump_to, 'B')

                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))
            else:

                temp = State(self, deepcopy(self.red), deepcopy(self.black), deepcopy(self.empty))
                temp.black.pop(pos)  # 원래 자리 비우기
                temp.empty[pos] = '.'  # 원래 자리 채우기

                temp.empty.pop(will_jump_to)  # 뉴 자리 비우기 점퍼블 투 의 키
                temp.black[will_jump_to] = 'b'  # 뉴 자리 채우기 점퍼블 투 의 키

                temp.red.pop(captured_pos)  # 잡은 애 비우기 레드인지 체크한 애
                temp.empty[captured_pos] = '.'  # 잡은 자리 채우기 레드인지 체크 한 애
                temp.player = MIN
                multi_capture = temp.black_piece_jumpable_to(will_jump_to, 'b')

                if multi_capture:
                    for another_caps in multi_capture:
                        new_captures = (captured_pos,) + another_caps
                        cont[new_captures] = deepcopy(cont[(captured_pos,)])
                        cont[new_captures][1] = multi_capture[another_caps][1]
                    cont.pop((captured_pos,))
        return cont

    def red_piece_movable_to(self, pos=Tuple[int, int]) -> dict[tuple, tuple]:
        """
        Precondition: 0 <= x, y <= 7, i.e., position pos is on the grid
        :param pos: position tuple of the red piece
        :return: list of positions that the red piece can move to, excluding
                    jump moves
        """
        movable_to = {}  # map new pos to old pos
        y, x = pos[0], pos[1]
        if self.red[pos] == 'R':  # if king: consider going down too
            if (y+1 <= 7 and x+1 <= 7 ) and (y+1, x+1) in self.empty:
                movable_to[(y+1, x+1)] = pos
            if (y+1 <= 7 and 0 <= x-1) and (y+1, x-1) in self.empty:
                movable_to[(y+1, x-1)] = pos
        # if just pawn: go up only
        if (0 <= y-1 and 0 <= x-1 ) and (y-1, x-1) in self.empty:
            movable_to[(y-1, x-1)] = pos
        if (0 <= y-1 and x+1 <= 7 ) and (y-1, x+1) in self.empty:
            movable_to[(y-1, x+1)] = pos
        return movable_to

    def black_piece_movable_to(self, pos=Tuple[int, int]) -> dict[tuple, list]:
        """
        Precondition: 0 <= x, y <= 7, i.e., position pos is on the grid
        :param pos: position tuple of the black piece
        :return: list of positions that the black piece can move to, excluding
                    jump moves
        """
        movable_to = {}
        y, x = pos[0], pos[1]
        if self.black[pos] == 'B':  # if king: consider going up too
            # if just pawn: go down only
            if (0 <= y-1 and 0 <= x-1 ) and (y-1, x-1) in self.empty:
                movable_to[(y-1, x-1)] = pos
            if (0 <= y-1 and x+1 <= 7 ) and (y-1, x+1) in self.empty:
                movable_to[(y-1, x+1)] = pos
        if (y+1 <= 7 and x+1 <= 7 ) and (y+1, x+1) in self.empty:
            movable_to[(y+1, x+1)] = pos
        if (y+1 <= 7 and 0 <= x-1) and (y+1, x-1) in self.empty:
            movable_to[(y+1, x-1)] = pos
        return movable_to


caching = {}


def AlphaBeta(state, depth=0, alpha=float('-inf'), beta=float('inf')):
    """
    :param state: current state
    :param depth: current depth, depth limit = MAX_DEPTH
    :param alpha: the highest value found so far
    :param beta: the lowest valye found so far
    :return: Best move and the Max's payoff for player(pos)
    """
    depth = depth
    best_move = None
    player = get_player(state)
    string_state = str(state)
    if string_state in caching:
        cached_depth, cached_alpha, cached_beta, cached_move, cached_value = caching[string_state]
        if cached_depth <= depth:
            if alpha == cached_alpha and beta == cached_beta:
                return cached_move, cached_value
            if player == MAX and beta <= cached_beta:
                return cached_move, cached_value
            if player == MIN and alpha >= cached_alpha:
                return cached_move, cached_value
    # if state in caching:
    #     # return caching[state]
    #     cached_depth, cached_alpha, cached_beta, cached_move, cached_value = caching[state]
    #     if depth < cached_depth:  # You cannot use a cached value if it was evaluated at a deeper level
    #         return cached_move, cached_value
    #     if cached_alpha > alpha:
    #         return cached_move, cached_value
    #     if cached_beta < beta:
    #         return cached_move, cached_value
    # depth <= cached_depth:
    # alpha = max(cached_alpha, alpha)
    # beta = min(cached_beta, beta)
    # continue searching, but with 더 조여진 알파 베타
    # if state in caching:
    #     cached_depth, cached_alpha, cached_beta, cached_move, cached_value = caching[state]
    #     if cached_depth > depth:
    #         if player == MAX and cached_alpha == cached_value:
    #             그냥 뉴 스테이트 계속 서치 하세요
    #         elif player == MIN and cached_beta == cached_value:
    #             그냥 뉴 스테이트 계속 서치 하세요
    #     else:
    if terminal(state) or depth > MAX_DEPTH:
        return best_move, utility(state)
    if player == MAX:
        value = float('-inf')
    elif player == MIN:
        value = float('inf')
    else:
        print("No player! This can't be!!")
    moves = state.generate_possible_moves()
    # heapq.heapify(moves)
    while len(moves) > 0:
        move = heapq.heappop(moves)
        if move.aftermove is None:
            move.set_aftermove()
        nxt_state = move.aftermove
        nxt_move, nxt_val = AlphaBeta(nxt_state, depth+1, alpha, beta)
        if player == MAX:
            if value < nxt_val:
                best_move, value = move, nxt_val
            if value >= beta:
                # caching[state] = best_move, value
                caching[string_state] = depth, alpha, beta, best_move, value
                return best_move, value
            alpha = max(alpha, value)
        if player == MIN:
            if value > nxt_val:
                best_move, value = move, nxt_val
            if value <= alpha:
                # caching[state] = best_move, value
                caching[string_state] = depth, alpha, beta, best_move, value
                return best_move, value
            beta = min(beta, value)
    # caching[state] = best_move, value
    caching[string_state] = depth, alpha, beta, best_move, value
    return best_move, value


initial_state = State(parent=None)
initial_state.set_player(MAX)

for i in range(len(input_string)):
    if input_string[i] == '.':
        initial_state.empty[(i//8, i%8)] = '.'
    elif input_string[i] == 'r':
        initial_state.red[(i//8, i%8)] = 'r'
    elif input_string[i] == 'R':
        initial_state.red[(i//8, i%8)] = 'R'
    elif input_string[i] == 'b':
        initial_state.black[(i//8, i%8)] = 'b'
    else:  # input_string[i] == 'B':
        initial_state.black[(i//8, i%8)] = 'B'

bestmove, _ = AlphaBeta(initial_state)
nextState = bestmove.aftermove
lis = [['.'] * 8 for i in range(8)]
for red_piece in nextState.red:
    lis[red_piece[0]][red_piece[1]] = nextState.red[red_piece]
for black_piece in nextState.black:
    lis[black_piece[0]][black_piece[1]] = nextState.black[black_piece]
lisToString = ""
for i in range(len(lis)):
    lisToString += ''.join(lis[i]) + '\n'

with open(output_filename, 'w') as output_file:
    # write the outputs in exact format
    output_file.writelines(lisToString.rstrip())
    # slicing to get rid of the last new line.

