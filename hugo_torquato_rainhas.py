# coding: utf-8
import win32com.client
import csv
from pylab import *
from random import *

class Population():

    def __init__(self):
        self.ID = []
        self.Genotypes = []
        self.Phenotype = []
        self.nota = []
        self.ID1 = 1

        ############### Aux Variables Definitions

        # Conversão da lista para string -> Para fazer a distribuição por permutação depois
        col = []
        for num in range(AG.N):
            col.append(num + 1)
        self.col = ''.join(str(e) for e in col)

    def Start_Population(self):

        # Defines The Old Population with a defined amont of Genotypes
        for index in range(AG.Population_Lenth):
            Gen = []
            Old_Pop.Genotypes.append(Old_Pop.Start_Gen(Gen))
            Old_Pop.ID.append(index)

        Old_Pop.Loop2CreatePhe(Old_Pop.Genotypes)

        # Generates the Phenotype from a givem Genotype
    def Loop2CreatePhe(self, GenVet):
        Old_Pop.Phenotype = []
        for Gen in GenVet:
            #Board.Introduce_Queen(Gen)
            Old_Pop.Phenotype.append(Board.Introduce_Queen(Gen))

    def Start_Gen(self, Gen):

        Temp_Col = Old_Pop.col
        interval = len(Temp_Col)
        for Try in (range(AG.N)):
            Num = randrange(0, interval)
            Gen.append(int(Temp_Col[Num]))
            Temp_Col = Temp_Col.replace(Temp_Col[Num], '')
            interval -= 1

        return Gen

class BoardTemplate():

    def Introduce_Queen(self, Genotype):
        Temp_Board = zeros((AG.N, AG.N))
        column_number = 0
        for Position in Genotype:
            Temp_Board[int(Position) - 1, column_number] = 1 # Fixa coluna e varia linha
            column_number += 1
        return Temp_Board

    def Print_Board(self, Print_Board):
        for row in Print_Board:
            print row

class Func_AG():

    def __init__(self):

        # Initial Definitions
        self.N = 8                     # Nth of Queens
        self.Population_Lenth = 10      # Population Length
        self.Ite = 100                 # Iterations for the Loop in the GA
        self.Mutation_Rate = 0.051      # TAXA DE MUTAÇÃO
        self.NumWorseToRemove = 2

        # Tournament Settings
        self.LengthTorPopulation = 5
        self.SelectedParants = 2

    def Fitness(self):
        Old_Pop.ID = []
        for index in range(len(Old_Pop.Genotypes)):
            Old_Pop.ID.append(index)

        Old_Pop.nota = []
        for Gen in Old_Pop.Phenotype:
            N1 = AG.First_Verification(Gen)
            #N2 = AG.Second_Verification(Gen)
            N3 = AG.Third_Verification(Gen)

            #Old_Pop.nota.append(N1 + N2 + N3)
            Old_Pop.nota.append(N1 + N3)

            #print Old_Pop.nota

        # First Verification - Casas Proximas

    def First_Verification(self, Gen):  # Posições laterais

        #Board.Print_Board(Gen)
        Valid = []
        for row in range(len(Gen)):
            for col in range(len(Gen)):
                if Gen[row][col] == 1:
                    if   (row != AG.N -1 and Gen[row + 1][col] == 1)                        : Valid.append(0)
                    elif (row != AG.N -1 and col != AG.N -1 and Gen[row + 1][col + 1] == 1) : Valid.append(0)
                    elif (col != AG.N -1 and Gen[row][col + 1] == 1)                        : Valid.append(0)
                    elif (row != 0 and col != AG.N -1 and Gen[row -1][col + 1] == 1)        : Valid.append(0)
                    elif (row != 0 and Gen[row - 1][col] == 1)                              : Valid.append(0)
                    elif (row != 0 and col != 0 and Gen[row - 1][col - 1] == 1)             : Valid.append(0)
                    elif (col != 0 and Gen[row ][col -1] == 1)                              : Valid.append(0)
                    elif (row != AG.N -1 and col != 0 and Gen[row + 1][col - 1] == 1)       : Valid.append(0)
                    else                                                                    : Valid.append(1)
        VAL = 0
        for val in Valid:
            VAL = VAL + val
        return float(VAL)/4

    def Second_Verification(self, Gen): # Conferir Linha e Colunas

        #Gen = [[0, 1, 0, 0],
        #       [1, 0, 0, 0],
        #       [0, 0, 1, 1],
        #       [0, 0, 0, 0]]
        #Board.Print_Board(Gen)

        ## Counts the number of queens per row and column,
        ## if that number is greater than 1 the Genotype suffers a penalty

        ContRow = 0
        ContCol = 0
        ValidRow = []#zeros(AG.N)
        ValidCol = []#zeros(AG.N)
        for row in range(len(Gen)):
            for col in range(len(Gen)):
                if Gen[row][col] == 1:
                    # Testa linhas
                    for VarRow in range(AG.N):
                        if Gen[VarRow][col] == 1:
                            ContRow += 1
                    if ContRow > 1:
                        ValidRow.append(0)
                        ContRow = 0
                    else:
                        ValidRow.append(1)
                        ContRow = 0
                    # Testa Colunas
                    for VarCol in range(AG.N):
                        if Gen[row][VarCol] == 1:
                            ContCol += 1
                    if ContCol > 1:
                        ValidCol.append(0)
                        ContCol = 0
                    else:
                        ValidCol.append(1)
                        ContCol = 0

        print
        print ValidRow
        print ValidCol
        VALRow = 0
        for val in ValidRow:
            VALRow = VALRow + val
        VALCol = 0
        for val in ValidCol:
            VALCol = VALCol + val

        #print float(VALCol)/4 + float(VALRow)/4
        return float(VALCol) + float(VALRow)

    def Third_Verification(self, Gen):

        #Gen = [[0, 0, 1, 0],
        #       [1, 0, 0, 0],
        #       [0, 0, 0, 1],
        #       [0, 1, 0, 0]]
        #Board.Print_Board(Gen)

        # Diagonais
        Control = 0
        ValidUR = []
        ValidUL = []
        ValidDR = []
        ValidDL = []

        for row in range(len(Gen)):
            for col in range(len(Gen)):
                if Gen[row][col] == 1:

                    # Down-Right
                    for Var in range(AG.N):
                        TempRow = row + Var
                        TempCol = col + Var
                        if TempRow < AG.N and TempCol < AG.N:
                            if Gen[TempRow][TempCol] == 1:
                                Control += 1
                    if Control > 1:
                        ValidDR.append(0)
                        Control = 0
                    else:
                        ValidDR.append(1)
                        Control = 0

                    # Down-Left
                    for Var in range(AG.N):
                        TempRow = row + Var
                        TempCol = col - Var
                        if TempRow < AG.N and TempCol >= 0:
                            if Gen[TempRow][TempCol] == 1:
                                Control += 1
                    if Control > 1:
                        ValidDL.append(0)
                        Control = 0
                    else:
                        ValidDL.append(1)
                        Control = 0

                    # Up-Right
                    for Var in range(AG.N):
                        TempRow = row - Var
                        TempCol = col + Var
                        if TempRow > 0 and TempCol < AG.N:
                            if Gen[TempRow][TempCol] == 1:
                                Control += 1
                    if Control > 1:
                        ValidUR.append(0)
                        Control = 0
                    else:
                        ValidUR.append(1)
                        Control = 0

                    # UP-Left
                    for Var in range(AG.N):
                        TempRow = row - Var
                        TempCol = col - Var
                        if TempRow >= 0 and TempCol >= 0:
                            if Gen[TempRow][TempCol] == 1:
                                Control += 1
                    if Control > 1:
                        ValidUL.append(0)
                        Control = 0
                    else:
                        ValidUL.append(1)
                        Control = 0

        #print
        #print ValidDR
        #print ValidDL
        #print ValidUR
        #print ValidUL

        VALDR = 0
        for val in ValidDR:
            VALDR = VALDR + val
        VALDL = 0
        for val in ValidDL:
            VALDL = VALDL + val
        VALUR = 0
        for val in ValidUR:
            VALUR = VALUR + val
        VALU = 0
        for val in ValidUL:
            VALU = VALU + val

        #print float(VALDR) / 4 + float(VALDL) / 4 + float(VALUR) / 4 + float(VALU) / 4
        return float(float(VALDR)/4 + float(VALDL)/4 + float(VALUR)/4 + float(VALU)/4)/4

    def ParantSelector(self):

        Tor.IDs = []
        Tor.SelectedIDs = []

        # Select the towo worst genotype and set thers grade to zero
        count = 0
        Selected_IDs = []
        while count < AG.NumWorseToRemove:
            Smaller = 1000
            Selected_ID = 0

            # problema com o tamnho dinamico do vetor
            for ID in Old_Pop.ID:
                if Old_Pop.nota[ID] < Smaller:
                    Smaller = Old_Pop.nota[ID]
                    Selected_ID = ID
            Selected_IDs.append(Selected_ID)
            Old_Pop.nota[Selected_ID] = 1000
            count += 1

        a = Old_Pop.nota
        for ID in Selected_IDs:
            Old_Pop.nota[ID] = 0
        b = Old_Pop.nota

        count = 0
        while count < AG.LengthTorPopulation:
            for ID in range(AG.LengthTorPopulation):
                Possible_ID = randrange(0, len(Old_Pop.ID))
                if Possible_ID != 0:
                    Tor.IDs.append(Possible_ID)
                    count += 1

        Tor.TournamentFunction()

    def CrossOver(self):

        Son_1 = []
        Son_2 = []

        cut = randrange(0, len(Old_Pop.Genotypes[0]))
        #print cut

        Son_1 = Old_Pop.Genotypes[Tor.SelectedIDs[0]][0:cut]
        Son_2 = Old_Pop.Genotypes[Tor.SelectedIDs[1]][0:cut]

        New_Scroll_1 = Old_Pop.Genotypes[Tor.SelectedIDs[0]][cut:] + Son_1
        New_Scroll_2 = Old_Pop.Genotypes[Tor.SelectedIDs[1]][cut:] + Son_2

        while len(Son_2) < AG.N:
            for Gen1 in New_Scroll_1:
                Verify = 0
                for Gen2 in Son_2:
                    if Gen1 == Gen2:
                        Verify = 1
                if Verify != 1:
                    Son_2.append(Gen1)

        while len(Son_1) < AG.N:
            for Gen1 in New_Scroll_2:
                Verify = 0
                for Gen2 in Son_1:
                    if Gen1 == Gen2:
                        Verify = 1
                if Verify != 1:
                    Son_1.append(Gen1)

        #print "Pai"
        #print Old_Pop.Genotypes[Tor.SelectedIDs[0]]
        #print Old_Pop.Genotypes[Tor.SelectedIDs[1]]
        #print " Filhos"
        #print Son_1
        #print Son_2
        #print

        New_Pop.Genotypes.append(Son_1)
        New_Pop.Genotypes.append(Son_2)

    def SWAP(self):

        end = len(New_Pop.Genotypes)
        i = 0
        for Gen in New_Pop.Genotypes[end-2:end]:
            #print New_Pop.Genotypes[end - 2], New_Pop.Genotypes[end - 1]
            if randint(0, 100)/100 < AG.Mutation_Rate:
                # Select the positions
                a = randint(0, len(Gen)-1)
                b = randint(0, len(Gen)-1)
                while b == a: b = randint(0, len(Gen)-1)
                # Change positions
                Temp_Value_A = Gen[a]
                Gen[a] = Gen[b]
                Gen[b] = Temp_Value_A
                #
                if i==0: New_Pop.Genotypes[end-2] = Gen
                else : New_Pop.Genotypes[end-1] = Gen
                #print New_Pop.Genotypes[end - 2], New_Pop.Genotypes[end-1]
                i += 1

class Tournament():

    def __init__(self):
        self.IDs = []
        self.SelectedIDs = []

    def TournamentFunction(self):

        # Não seleciona pais iguais
        Selected = 0

        for i in range(AG.SelectedParants):                    # loppa quantos pais serão selecionados
            if len(Tor.SelectedIDs) < AG.SelectedParants:      # Seleciona os dois que serão pais
                Nota = 0
                for ID in Tor.IDs:
                    if Old_Pop.nota[ID] >= Nota:
                            Selected = ID
                            Nota = Old_Pop.nota[Selected]
                Tor.SelectedIDs.append(Selected)
                a = Tor.IDs
                b = Old_Pop.nota
                del(Tor.IDs[Tor.IDs.index(Selected)])
        #print Tor.SelectedIDs

class Best():

    def __init__(self):
        self.ID = []
        self.Genotypes = []
        self.Phenotype = []
        self.nota = []
        self.Generation = []

        self.BID = []
        self.BGenotypes = []
        self.BPhenotype = []
        self.Bnota = []
        self.BGeneration = []

    def BestPerGeneration(self, Ite):

        nota = 0
        SelectedID = 0

        for ID in Old_Pop.ID:
            if Old_Pop.nota[ID] > nota:
                nota = Old_Pop.nota[ID]
                SelectedID = ID

        Best.Genotypes.append(Old_Pop.Genotypes[SelectedID])
        Best.Phenotype.append(Old_Pop.Phenotype[SelectedID])
        Best.nota.append(Old_Pop.nota[SelectedID])
        Best.ID.append(len(Best.Genotypes))
        Best.Generation.append(Ite)

    def GlobalBest(self):

        nota = 0
        SelectedID = 0

        for ID in Best.ID:
            if Best.nota[ID-1] > nota:
                nota = Best.nota[ID -1]
                SelectedID = ID

        Best.BGenotypes.append(Best.Genotypes[SelectedID-1])
        Best.BPhenotype.append(Best.Phenotype[SelectedID-1])
        Best.Bnota.append(Best.nota[SelectedID-1])
        Best.BID.append(len(Best.BGenotypes))




if __name__ == "__main__":
    print u"""Autor: Hugo Torquato \nData: 11/08/2020 \nE-mail: hugortorquato@gmail.com \n"""

    AG = Func_AG()
    Board = BoardTemplate()
    Old_Pop = Population()
    #New_Pop = Population()
    Tor = Tournament()
    Best = Best()

    # Inicialization
    Old_Pop.Start_Population() # Cria as Genotipos  e gera o fenotipo

    # Initial Fitnes
    AG.Fitness()

    # Loop
    for Ite in range(AG.Ite):
        print " Ite : " + str(Ite)

        Best.BestPerGeneration(Ite)
        Best.GlobalBest()
        New_Pop = Population()
        while len(New_Pop.Genotypes) < AG.Population_Lenth:
            AG.ParantSelector()
            AG.CrossOver()
            AG.SWAP()

        Old_Pop.Genotypes = New_Pop.Genotypes
        Old_Pop.Loop2CreatePhe(Old_Pop.Genotypes)
        AG.Fitness()

        #print Old_Pop.nota

    subplot(211)
    plot(Best.nota)
    subplot(212)
    plot(Best.Bnota)
    plt.show()


