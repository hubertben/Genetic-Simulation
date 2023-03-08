
import random

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

allowedChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*.<>?,/;:[]()_+-= "


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class Unit:

    def __init__(self, ID, genome = [], genomeDimentions = []):
        self.ID = ID
        self.genome = genome

        if genome == []:
            self.genome = self.generateGenome(genomeDimentions)
    
    def generateGenome(self, genomeDimentions):
        genome = []
        for dimention in genomeDimentions:
            strand = []
            for i in range(dimention):
                strand.append(random.choice(allowedChars))
            genome.append(strand)
        return genome
    
    def compressedGenome(self):
        return "".join(["".join(strand) for strand in self.genome])

    def __str__(self):
        return str(self.compressedGenome())
    
    def __repr__(self):
        return str(self.compressedGenome())
    
    def mutate(self, mutationRate):
        for strand in self.genome:
            for i in range(len(strand)):
                if random.random() < mutationRate:
                    
                    if random.random() < 0.5:
                        strand[i] = chr(ord(strand[i]) + 1)
                    else:
                        strand[i] = chr(ord(strand[i]) - 1)
                    
                    if strand[i] not in allowedChars:
                        strand[i] = random.choice(allowedChars)
                    



    def crossover(self, other):
        childGenome = []
        for i in range(len(self.genome)):
            childStrand = []
            for j in range(len(self.genome[i])):
                if random.random() < 0.5:
                    childStrand.append(self.genome[i][j])
                else:
                    childStrand.append(other.genome[i][j])
            childGenome.append(childStrand)
        return Unit("", childGenome)
    



class GeneticAlgorithm:

    def __init__(self, units, target, mutationRate = 0.05):
        self.units = units
        self.target = target
        self.mutationRate = mutationRate
    
    def fitness(self, unit):
        score = 0
        for i in range(len(self.target)):
            dist = abs(ord(unit.compressedGenome()[i]) - ord(self.target[i]))
            if dist == 0:
                score += 1
            else:
                score += 1 / (dist * 10)

        return map(score ** 2, 0, len(self.target) ** 2, 0, 1)
    
    def getTotalFitness(self, getBest = False):
        totalFitness = 0
        bestFitness = 0
        for unit in self.units:
            
            F = self.fitness(unit)
            totalFitness += F
            if F > bestFitness:
                bestFitness = F

        if getBest:
            return totalFitness, bestFitness
        return totalFitness
    
    def getAverageFitness(self):
        return self.getTotalFitness() / len(self.units)
    
    def selection(self, chooseTopPercent = 0.2):
        TF = self.getTotalFitness()
        probabilities = [self.fitness(unit) / TF for unit in self.units]

        bestUnit = self.units[probabilities.index(max(probabilities))]
        
        chosen = [bestUnit]

        for i in range((int(len(self.units) * chooseTopPercent)) - 1):
            chosen.append(self.units[probabilities.index(max(probabilities))])
            probabilities[probabilities.index(max(probabilities))] = 0

        return chosen
    
    def displayUnits(self, TB = .1):
        if(TB == 0):
            for unit in self.units:
                print(unit)
        elif(TB < 1):
            
            for unit in range(int(len(self.units) * TB)):
                print(self.units[unit])

            print("...")

            for unit in range(int(len(self.units) * (1 - TB)), len(self.units)):
                print(self.units[unit])
        else:
            for unit in range(int(TB)):
                print(self.units[unit])

    
    def unitAgainstTarget(self, unit):
        newStr = ""
        for i in range(len(self.target)):
            if unit.compressedGenome()[i] == self.target[i]:
                newStr += OKGREEN + unit.compressedGenome()[i] + ENDC
            else:
                newStr += unit.compressedGenome()[i]
        return newStr

    
    def performEvolution(self, rounds = 100, displayRate = 1):

        for i in range(rounds):

            self.mutationRate = 0.001

            newUnits = []
            selec = self.selection(0.5)

            bestUnit = self.units[0]
            
            if i % displayRate == 0 and self.fitness(bestUnit) != 1.0:
                L = 5
                print(
                    " Best:" + self.unitAgainstTarget(bestUnit) +
                    " Best Fitness " + str(round(self.fitness(bestUnit), 3)).rjust(L, "0")
                )

            if self.fitness(bestUnit) == 1.0:
                return bestUnit, self.fitness(bestUnit), self.unitAgainstTarget(bestUnit)

            for i in range(len(self.units)):
                newUnits.append(self.units[i].crossover(random.choice(selec)))
            
            self.units = newUnits

            for unit in self.units:
                unit.mutate(self.mutationRate)


numOfUnits = 1000

# targetLength = 100
# maxOrd = max([ord(c) for c in targetLength])
# target = chr(maxOrd) * len(targetLength)

# target = "Hello World!"
# targetLength = len(target)

target = "Hello World!"
targetLength = len(target)

GA = GeneticAlgorithm([Unit(i, genomeDimentions = [targetLength]) for i in range(numOfUnits)], target)
best, bestFit, coloring = GA.performEvolution(rounds = 999, displayRate = 5)

L = 5
print(
    " Best:" + coloring +
    " Best Fitness " + str(round(bestFit, 3)).rjust(L, "0")
)