import copy

class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self.info]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):
        l = self.obtineDrum()
        for inod, nod in enumerate(l):
            print("Tura " + str(inod+1) +": " + str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisLung:
            print("Lungime: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        # return infoNodNou in self.obtineDrum()
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    # def __repr__(self):
    #     sir = ""
    #     sir += str(self.info)
    #     return (sir)




class Graph:  # graful problemei
    def __init__(self, nume_fisier):

        with open(nume_fisier) as f:
            continutFisier = f.read()

        self.inititalSplit = continutFisier.split("turnuri")

        self.dateInvadatori = self.inititalSplit[0].strip().split(" ")
        # print (self.dateInvadatori)
        self.NS = int(self.dateInvadatori[0]) #Enemy Hitpoints
        self.N_INV = int(self.dateInvadatori[1]) #Number of enemies
        self.PT_TURA = int(self.dateInvadatori[2]) #Points gained every turn
        self.PT_INIT = int(self.dateInvadatori[3]) #Points available at the start of the game
        self.PT_INAMIC = int(self.dateInvadatori[4]) #Points gained on enemy kill
        # print(self.NS, self.N_INV, self.PT_TURA, self.PT_INIT, self.PT_INAMIC)

        self.secondSplit = self.inititalSplit[1].split("harta")

        self.dateTurnuri = []
        self.dateTurnuri_str = self.secondSplit[0].strip().split("\n")
        for date in self.dateTurnuri_str:
            self.dateTurnuri.append(list(date.split(" ")))
        for turn in self.dateTurnuri:
            for i in range(1, len(turn)):
                turn[i] = int(turn[i])
        # print(self.dateTurnuri)

        # identificator_turn = self.dateTurnuri[][0] #tower type
        # T_COST = int(self.dateTurnuri[][1])        #tower cost
        # T_VIATA = int(self.dateTurnuri[][2])       #tower life (in turns)
        # POC_POC = self.dateTurnuri[][3]            #tower dmg
        # T_RAZA = int(self.dateTurnuri[][4])        #tower range
        # T_PAUZA = int(self.dateTurnuri[][5])       #tower firing cooldown

        self.lastSplit = self.secondSplit[1].strip().split("\n")
        # print(*lastSplit, sep='\n')

        self.endPoint = self.lastSplit.pop().split(" ")
        self.endPoint[0] = int(self.endPoint[0])
        self.endPoint[1] = int(self.endPoint[1])
        self.startPoint = self.lastSplit.pop().split(" ")
        self.startPoint[0] = int(self.startPoint[0])
        self.startPoint[1] = int(self.startPoint[1])
        # print(self.startPoint)
        # print(self.endPoint)

        labyrinthMatrix = []
        for line in self.lastSplit:
            labyrinthMatrix.append(list(line))
        # print(*labyrinthMatrix, sep='\n')

        self.enemySpots = []
        for i in range(len(labyrinthMatrix)):
            for j in range(len(labyrinthMatrix[i])):
                if labyrinthMatrix[i][j] == '*':
                    self.enemySpots.append([i, j])
        # print(self.enemySpots)

        self.enemyPath = []
        point = self.startPoint
        self.enemyPath.append([point[0], point[1]])
        while point != self.endPoint:
            if [point[0], point[1]-1] in self.enemySpots and [point[0], point[1]-1] not in self.enemyPath:
                point[1] -= 1
                self.enemyPath.append([point[0], point[1]])
            elif [point[0]-1, point[1]] in self.enemySpots and [point[0]-1, point[1]] not in self.enemyPath:
                point[0] -= 1
                self.enemyPath.append([point[0], point[1]])
            elif [point[0], point[1]+1] in self.enemySpots and [point[0], point[1]+1] not in self.enemyPath:
                point[1] += 1
                self.enemyPath.append([point[0], point[1]])
            elif [point[0]+1, point[1]] in self.enemySpots and [point[0]+1, point[1]] not in self.enemyPath:
                point[0] += 1
                self.enemyPath.append([point[0], point[1]])
        # print(self.enemyPath == self. enemySpots)

        # enemySpots contine coordonatele fiecarei unitati de drum

        self.towerSpots = []
        for i in range(len(labyrinthMatrix)):
            for j in range(len(labyrinthMatrix[i])):
                if labyrinthMatrix[i][j] == '#' and i in range(1,len(labyrinthMatrix)-1)\
                        and j in range(1,len(labyrinthMatrix[i])-1):
                    self.towerSpots.append([i,j])
        # print(*self.towerSpots, sep='\n')

        # towerSpots contine coordonatele fiecarei unitati unde putem pune un turn

        self.enemies = [0]*(len(self.enemyPath))
        self.placedTowers = [[] for _ in range(len(self.towerSpots))]
        # print(self.placedTowers)

        self.scop = [0]*(len(self.enemyPath))
        # print(self.scop)

        self.start = [self.N_INV, self.PT_INIT, self.enemies, self.placedTowers]
        # print(self.start)

    def findTowerIndexByIdentifier(self, identifier):
        for i in range(len(self.dateTurnuri)):
            if self.dateTurnuri[i][0] == identifier:
                return i

    def testeaza_scop(self, nodCurent):
        if nodCurent.info[0] == 0:  # daca nu mai sunt inamici
            return nodCurent.info[2] == self.scop
        return False

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        if self.testeaza_scop(nodCurent):
            return listaSuccesori
        copie_nod = copy.deepcopy(nodCurent.info)
        if copie_nod[0] > 0:
            copie_nod[2] = [self.NS] + copie_nod[2][:-1]
            # adaug un inamic pe drum si ii mut pe restul cu un spatiu
            copie_nod[0] = copie_nod[0] - 1         # scad numarul de inamici ce mai pot aparea
        elif copie_nod[0] == 0:
            # doar mut toti inamicii cu un spatiu
            copie_nod[2] = [0] + copie_nod[2][:-1]

        if copie_nod[0] == 0 and copie_nod[2][-1] != 0:
            return []

        for i in range(len(copie_nod[3])):         # pentru fiecare locatie unde se pot construi turnuri
            if len(copie_nod[3][i]) != 0:          # verific daca exista turn pe acea pozitie

                # verific daca poate trage (daca are T_PAUZA == 0)
                if copie_nod[3][i][5] == 0:
                    for x in range(self.towerSpots[i][0] - copie_nod[3][i][4],
                                    self.towerSpots[i][0] + copie_nod[3][i][4]):
                        for y in range(self.towerSpots[i][1] - copie_nod[3][i][4],
                                       self.towerSpots[i][1] + copie_nod[3][i][4]):
                            # print([x, y])
                            # verific daca exista inamici  in raza de actiune a turnului
                            for enemySpot in self.enemyPath:
                                if enemySpot == [x, y] and copie_nod[2][self.enemyPath.index([x, y])] != 0:

                                    # le scad din viata in functie de cat dmg are turnul (POC_POC)
                                    copie_nod[2][self.enemyPath.index([x, y])] -= copie_nod[3][i][3]

                                    # daca inamicul moare, se adauga PT_INAMIC puncte
                                    if copie_nod[2][self.enemyPath.index([x, y])] <= 0:
                                        copie_nod[1] += self.PT_INAMIC

                                    # si pun turnul pe cooldown (daca este cazul)
                                    copie_nod[3][i][5] = self.dateTurnuri[self.findTowerIndexByIdentifier(copie_nod[3][i][0])][5]
                else:
                    copie_nod[3][i][5] -= 1    # daca are T_PAUZA > 0 ii micsoram cooldown-ul cu o tura

                # daca are viata 0 eliminam turnul
                if copie_nod[3][i][2] == 0:
                    copie_nod[3][i] = []
                # daca are viata finita (care nu e 999) i-o scadem cu o tura
                else:
                # if nodCurent.info[3][i][2] != 999:
                    copie_nod[3][i][2] -= 1

        PT_curente = copie_nod[1] + self.PT_TURA      # PT dupa ce trece tura
        nodeCopy = copy.deepcopy(copie_nod)

        for i in range(len(nodCurent.info[3])):    # pe fiecare locatie de turn
            if len(nodCurent.info[3][i]) == 0:      # verifica daca exista deja turn
                for turn in self.dateTurnuri:       # ia la rand fiecare tip de turn
                    PT = PT_curente
                    if PT >= turn[1]:               # daca avem destule puncte
                        copieInterm = copy.deepcopy(nodeCopy)
                        copieInterm[3][i] = turn   # il construieste
                        PT -= turn[1]           # si scade pretul turnului din punctele curente
                        copieInterm[1] = PT
                        costMutare = 1 + turn[1]
                        if not nodCurent.contineInDrum(copieInterm):
                            nod_nou = NodParcurgere(copieInterm, nodCurent, cost=nodCurent.g + costMutare,
                                                    h=self.calculeaza_h((copieInterm, tip_euristica)))

                            listaSuccesori.append(nod_nou)
                            # print(copieInterm, '\n')
            # daca exista deja turn, il vindem daca va disparea tura urmatoare
            elif nodCurent.info[3][i][2] == 1:
                copieInterm = copy.deepcopy(nodeCopy)
                copieInterm[1] += int(nodCurent.info[3][i][1]/2)
                copieInterm[3][i] = []
                costMutare = 1 + int(nodCurent.info[3][i][1]/2)
                nod_nou = NodParcurgere(copieInterm, nodCurent, cost=nodCurent.g + costMutare,
                                        h=self.calculeaza_h((copieInterm, tip_euristica)))
                listaSuccesori.append(nod_nou)

        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            if infoNod[0] != 0 or infoNod[2] != self.scop:
                return 1
            return 0
        elif tip_euristica == "euristica admisibila 1":
            # calculez numarul de pasi necesari pentru un inamic de a ajunge la un turn
            euristici = []
            pass


def breadth_first(gr, nrSolutiiCautate):

    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None)]

    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        # print('\n')
        # print(nodCurent.info)
        # print('\n')
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        # print(lSuccesori, sep='\n')
        c.extend(lSuccesori)


def depth_first(gr, nrSolutiiCautate=1):
    # vom simula o stiva prin relatia de parinte a nodului curent
    df(NodParcurgere(gr.start, None), nrSolutiiCautate)


def df(nodCurent, nrSolutiiCautate):
    if nrSolutiiCautate <= 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
        return nrSolutiiCautate
    if gr.testeaza_scop(nodCurent):
        nodCurent.afisDrum(afisCost=True, afisLung=True)
        print("\n----------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    for sc in lSuccesori:
        if nrSolutiiCautate != 0:
            nrSolutiiCautate = df(sc, nrSolutiiCautate)

    return nrSolutiiCautate


def dfi(nodCurent, adancime, nrSolutiiCautate):

    if adancime == 1 and gr.testeaza_scop(nodCurent):
        nodCurent.afisDrum(afisCost=True, afisLung=True)
        print("\n----------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                nrSolutiiCautate = dfi(sc, adancime - 1, nrSolutiiCautate)
    return nrSolutiiCautate


def depth_first_iterativ(gr, nrSolutiiCautate=1):
    for i in range(1, gr.N_INV + len(gr.enemyPath)):
        if nrSolutiiCautate == 0:
            return
        nrSolutiiCautate = dfi(NodParcurgere(gr.start, None), i, nrSolutiiCautate)



def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)



def a_star_optimizat(gr):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    # l_open contine nodurile candidate pentru expandare (este echivalentul lui c din A* varianta neoptimizata)
    # l_closed contine nodurile expandate
    l_closed = []
    while len(l_open) > 0:
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent):
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                # diferenta fata de UCS e ca ordonez crescator dupa f
                # daca f-urile sunt egale ordonez descrescator dupa g
                if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)


gr = Graph("input_mic.txt")
# gr = Graph("input_imposibil.txt")
# gr = Graph("input.txt")
# gr = Graph("start_egal_scop.txt")


NSOL = 2

print("Solutii cu BF: \n")
breadth_first(gr, nrSolutiiCautate=NSOL)

print("Solutii cu DF: \n")
depth_first(gr, nrSolutiiCautate=NSOL)

print("Solutii cu DFI: \n")
depth_first_iterativ(gr, nrSolutiiCautate=NSOL)

print("Solutii cu A*: \n")
a_star(gr, nrSolutiiCautate=NSOL, tip_euristica="euristica banala")

print("Solutie cu A* optimizat: \n")
a_star_optimizat(gr)
