import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if count == number of item in set, all cells must be mines
        if self.count == len(self.cells):
            return self.cells
        
        #TODO possibly more options
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if mine count = 0, all cells must be safe
        if self.count == 0:
            return self.cells

        #TODO possible more options

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # check if cell is in the sentence
        if cell in self.cells:
            self.cells.remove(cell)
            # update the count to reflect the fact that a mine is gone
            self.count = self.count - 1

        #TODO possible more options
        
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

        #TODO possible more options


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of the number value inside clicked cells

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Create a new sentence and add it to the knowledge base
        # Get every adjacent cell
        row = cell[0]
        column = cell[1]
        potential_cells = [
            (row - 1, column - 1),
            (row - 1, column),
            (row - 1, column + 1),

            (row, column - 1),
            (row, column + 1),

            (row + 1, column - 1),
            (row + 1, column ),
            (row + 1, column + 1),
        ]
        
        cells_to_be_removed = []
        for cell in potential_cells:
            if cell[0] < 0 or cell[0] > 7:
                cells_to_be_removed.append(cell)
                continue

            if cell[1] < 0 or cell[1] > 7:
                cells_to_be_removed.append(cell)
                
        for cell in cells_to_be_removed:
            potential_cells.remove(cell)

        # only include cells whose state is undetermined
        final_cell_set = set()
        for cell in potential_cells:
            if cell in self.safes or cell in self.mines:
                continue
            else:
                final_cell_set.add(cell)

        new_sentence = Sentence(
            cells = final_cell_set,
            count = count
        )

        # add the new sentence to the knowledgebase
        self.knowledge.append(new_sentence)
        

        # If, based on any of the sentences in self.knowledge,
        # new cells can be marked as safe or as mines, then the function should do so.

        # add to the list of mines and safes, cells that are guaranteed to be so
        for sentence in self.knowledge:
            known_mines = copy.deepcopy(sentence.known_mines()) 
            known_safes = copy.deepcopy(sentence.known_safes())
            if known_mines != None:
                for cell in known_mines:
                    self.mark_mine(cell)
            if known_safes != None:
                for cell in known_safes:
                    self.mark_safe(cell)

        # if a cell is surrounded by non zero cells, it is guaranteed to be a mine
        # if every adjacent cell is in moves made, and non of them are 

        # If, based on any of the sentences in self.knowledge, new sentences can be inferred 
        # (using the subset method described in the Background), then those sentences should be added to the knowledge base as well.
        
        # Compare the new sentence to existing sentences to see if it is a subset of the others and vice versa
        sentences_to_be_added = []
        for sentence in self.knowledge:
            if sentence.__eq__(new_sentence) == True:
                continue
            a_subset_of_b = sentence.cells.issubset(new_sentence.cells)
            b_subset_of_a = new_sentence.cells.issubset(sentence.cells)

          


            if a_subset_of_b == True:
                new_count = new_sentence.count - sentence.count
                copy_of_b_cells = copy.deepcopy(new_sentence.cells)
                for cell in sentence.cells:
                    copy_of_b_cells.remove(cell)
                
                subset_sentence = Sentence(
                    cells = copy_of_b_cells,
                    count = new_count
                )
                print("##############NEW SENTENCE################")
                print("Sentence A: ", sentence)
                print("Sentence B: ", new_sentence)
                print("New Sentence: ", subset_sentence)
                print("\n")
                sentences_to_be_added.append(subset_sentence)

            if b_subset_of_a == True:
                new_count = sentence.count - new_sentence.count
                copy_of_a_cells = copy.deepcopy(sentence.cells)
                for cell in new_sentence.cells:
                    copy_of_a_cells.remove(cell)

                subset_sentence = Sentence(
                    cells = copy_of_a_cells,
                    count = new_count
                )
                print("##############NEW SENTENCE################")
                print("Sentence A: ", sentence)
                print("Sentence B: ", new_sentence)
                print("New Sentence: ", subset_sentence)
                print("\n")
                sentences_to_be_added.append(subset_sentence)

        for sentence in sentences_to_be_added:
            self.knowledge.append(sentence)
        
        
        ##################################################
        # Check each sentence in self.knowledge again to see if it is possible to mark more cells and safes/mines:




        ##################################################
        # check every sentence in self.knowledge and delete set() = 0 to avoid slowdown
        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

            
        print("Final knowledgebase: ")
        for sentence in self.knowledge:
            print(sentence)
                    

        


        

        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        try:
            for move in self.safes:
                if move not in self.moves_made:
                    return move
        except:
            print("Exception")
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            random_row = random.randint(0, 7)
            random_column = random.randint(0, 7)

            random_move = (random_row, random_column)
            if random_move not in self.mines and random_move not in self.moves_made:
                return random_move
    
    
                
                