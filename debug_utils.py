class DebugTurnHandler:
    
    def next(self):
        return 0
    

class MatrixPrinter:

    @staticmethod
    def print(matrix):
        if len(matrix) != 3 or not all(len(row) == 3 for row in matrix):
            raise ValueError("Input must be a 3x3 matrix.")
        
        for i, row in enumerate(matrix):
            print(" | ".join(map(str, row)))
            if i < 2:
                print("-" * 9)
