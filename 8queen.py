import datetime
import random


class Point:
    Row = None
    Col = None

    def __init__(self, row, col):
        self.Row = row
        self.Col = col


class Individual:
    Genes = None
    Fitness = None

    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness


def getPoint(rowGene, colGene, gene_set):
    rowIndex = gene_set.index(rowGene)
    if rowIndex == -1:
        raise ValueError("'" + rowGene + "' is an invalid gene")
    colIndex = gene_set.index(colGene)
    if colIndex == -1:
        raise ValueError("'" + colGene + "' is an invalid gene")
    return Point(rowIndex, colIndex)


def getBoard(candidate):
    board = [['.'] * 8 for i in range(8)]
    for index in range(0, len(candidate), 2):
        # print(candidate[index], type(candidate[index]))
        board[int(candidate[index])][int(candidate[index + 1])] = 'Q'
    return board


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    board = getBoard(candidate.Genes)
    for i in range(8):
        print(board[i][0],
              board[i][1],
              board[i][2],
              board[i][3],
              board[i][4],
              board[i][5],
              board[i][6],
              board[i][7]
              )
    print("%s\t%i\t%s" % (''.join(map(str, candidate.Genes)), candidate.Fitness, str(timeDiff)))


def getFitness(candidate):
    board = getBoard(candidate)
    rowsWithQueens = {}
    colsWithQueens = {}
    northEastDiagonalsWithQueens = {}
    southEastDiagonalsWithQueens = {}
    for row in range(8):
        for col in range(8):
            if board[row][col] == 'Q':
                rowsWithQueens[row] = 1
                colsWithQueens[col] = 1
                northEastDiagonalsWithQueens[row + col] = 1
                southEastDiagonalsWithQueens[8 - 1 - row + col] = 1

    return len(rowsWithQueens) \
           + len(colsWithQueens) \
           + len(northEastDiagonalsWithQueens) \
           + len(southEastDiagonalsWithQueens)


def generateParent(length, geneSet, get_fitness):
    genes = list("")
    for i in range(0, length):
        geneIndex = random.randint(0, len(geneSet) - 1)
        genes.append(geneSet[geneIndex])

    for i in range(len(genes)):
        genes[i] = str(genes[i])

    childGenes = (''.join(genes))
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness)


def mutate(parent, geneSet, get_fitness):
    geneIndex = random.randint(0, len(geneSet) - 1)
    index = random.randint(0, len(parent.Genes) - 1)
    genes = list(parent.Genes)
    genes[index] = geneSet[geneIndex]
    for i in range(len(genes)):
        genes[i] = str(genes[i])
    childGenes = (''.join(genes))
    fitness = get_fitness(childGenes)
    return Individual(childGenes, fitness)


def getBest(get_fitness, display, targetLen, optimalFitness, geneSet):
    random.seed()
    bestParent = generateParent(targetLen, geneSet, get_fitness)
    display(bestParent)

    while bestParent.Fitness < optimalFitness:
        parent = generateParent(targetLen, geneSet, get_fitness)
        attemptsSinceLastImprovement = 0
        while attemptsSinceLastImprovement < 128:
            child = mutate(parent, geneSet, get_fitness)
            if child.Fitness > parent.Fitness:
                parent = child
                attemptsSinceLastImprovement = 0
            attemptsSinceLastImprovement += 1

        if bestParent.Fitness < parent.Fitness:
            bestParent, parent = parent, bestParent
            display(bestParent)

    return bestParent


class EightQueensTests():
    def test(self):
        geneset = [a for a in range(0, 8)]
        optimalValue = 8 + 8 + 8 + 8
        startTime = datetime.datetime.now()
        fnDisplay = lambda candidate: display(candidate, startTime)
        fnGetFitness = lambda candidate: getFitness(candidate)
        getBest(fnGetFitness, fnDisplay, 16, optimalValue, geneset)


if __name__ == '__main__':
    eightQueen = EightQueensTests()
    eightQueen.test()
