import random

# Houston, Dallas, Austin, Abilene, Waco
dist =[[0,241,162,351,183],
 [241,0,202,186,97],
 [162,202,0,216,106],
 [351,186,216,0,186],
 [183,97,106,186,0]]

def genPop(numIndividuals, lenChromo):
    population = []
    for i in range(numIndividuals):
        new=[1,2,3,4]
        random.shuffle(new)
        new.insert(0,0)
        new.append(0)
        population.append(new)
    #print(population)
    return population

def fitness(chromo):
    #print(chromo)
    total=0
    for i in range(len(chromo)-1):
        total=total+dist[chromo[i]][chromo[i+1]]
    return total

def naryTournament(pop,fitnessList,n=2):
    mating_pool=[]
    for i in range(len(pop)):
        indexes=[]
        for j in range(n):
            ind = random.randint(0,len(pop)-1)
            indexes.append(ind)
        fit_scores = []
        for item in indexes:
            #print(item)
            fit_scores.append(fitnessList[item])
        max_fit=min(fit_scores)
        idx_max=fitnessList.index(max_fit)
        mating_pool.append(pop[idx_max])
    return mating_pool

def crossover(mate,crossRate):
    pop=[]
    while len(pop)<len(mate):
        for i in range(0,len(mate)-1,2):
            parent1 = mate[i]
            parent2 = mate[i+1]
            if random.random()<crossRate:
                ind1 = random.randint(1,len(parent1)-2)
                ind2 = random.randint(1,len(parent1)-2)
                while ind1==ind2:
                    ind2 = random.randint(1,len(parent1)-2)
                child = [0,-1,-1,-1,-1,0]
                if ind2>ind1:
                    child[ind1:ind2]=parent1[ind1:ind2]
                else:
                    child[ind2:ind1]=parent1[ind2:ind1]

                for item in parent2:
                    if item not in child:
                        for i in range(len(child)):
                            if child[i]==-1:
                                child[i]=item
                                break
                pop.append(child)
                if len(pop) >= len(mate):
                    break
            else:
                parent = random.randint(1,2)
                if parent == 1:
                    child = parent1
                else:
                    child = parent2
                pop.append(child)
                if len(pop) >= len(mate):  
                    break
            #pop.append(child)
    return pop[:len(mate)]

def mutate(pop,mutRate):
    mutated=[]
    for i in range(0,len(pop)):
        child = pop[i]
        if random.random()<mutRate:
            ind1 = random.randint(1,len(child)-2)
            ind2 = random.randint(1,len(child)-2)
            while ind1==ind2:
                ind2 = random.randint(1,len(child)-2)
            first = child[ind1]
            child[ind1]=child[ind2]
            child[ind2]=first
        mutated.append(child)
    return mutated

def main(popSize,chromoSize,geneBoundaries,mutRate,crossRate,maxGens):
    pop = genPop(popSize,chromoSize)
    min_dist = 1000000000000000
    path = []
    for z in range(maxGens):
        fit_score=[]
        for item in pop:
            fit = fitness(item)
            fit_score.append(fit)
        max_fit = min(fit_score)
        idx_max=fit_score.index(max_fit)
        print(f'{z} {pop[idx_max]} {min(fit_score):20}')
        if max_fit<min_dist:
            min_dist=max_fit
            path=pop[idx_max]
        mate = naryTournament(pop,fit_score)
        pop=crossover(mate,crossRate)
        pop=mutate(pop,mutRate)
    print(f' Minimum distance: {min_dist}, Optimal Path: {path}')
    
main(popSize=500,chromoSize=32,geneBoundaries=dist,mutRate=.001,crossRate=.6,maxGens=100)

