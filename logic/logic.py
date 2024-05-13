from copy import deepcopy
from natsort import natsorted
import pandas
import re
import sys
import time
import datetime

metrics = {'none':0, 'low':0.2, 'medium':0.5, 'high':0.8, 'veryhigh':0.9} #global dict containing the metric to numeric conversions

def discoverCases(objectives, allControls, budget):
    cases = [deepcopy(allControls)] # list of cells with comma separated effectiveness
    casesAsIndex = [list()] #to keep track of which case as index (e.g., change Control1 Confidentiality to 0.2)

    for rowIndex in range(0, len(allControls)):
        for columnIndex in range(4, len(allControls[rowIndex])):
            #print(allControls[rowIndex][columnIndex])
            if "," in str(allControls[rowIndex][columnIndex]):
                currCasesLen = len(cases)
                possibleValues = allControls[rowIndex][columnIndex].split(",")
                counter = 0
                for i in range(0, currCasesLen):
                    cases[i][rowIndex][columnIndex] = possibleValues[counter]
                    casesAsIndex[i].append( (rowIndex, columnIndex, possibleValues[counter]) )
                    counter = (counter + 1) % len(possibleValues)
                    for j in range(0, len(possibleValues) - 1):
                        cases.append( deepcopy(cases[i]) )
                        cases[len(cases) - 1][rowIndex][columnIndex] = possibleValues[counter]
                        atIndexCopy = deepcopy(casesAsIndex[i])
                        atIndexCopy[len(atIndexCopy) - 1] = ( atIndexCopy[len(atIndexCopy) - 1][0],
                                                                atIndexCopy[len(atIndexCopy) - 1][1],
                                                                possibleValues[counter] )
                        casesAsIndex.append(atIndexCopy)
                        counter = (counter + 1) % len(possibleValues)
    #print(len(cases))
    #print(casesAsIndex)

    resultByCases = dict() # stores results as keys (frozen list of frozen sets) and the values as the cases (as index)
                            # helps map which cases have same results

    #iterate through cases and discover best strategies for each case
    for i in range(0, len(cases)):
        caseResults = discoverBestStrategies(objectives, cases[i], budget)
        caseResultsToBeFrozen = []
        for result in caseResults: #freeze each case result
            caseResultsToBeFrozen.append(frozenset(result))

        caseResultsFrozen = frozenset(caseResultsToBeFrozen)
        if caseResultsFrozen in resultByCases: #means these results were obtained by a previous case
            resultByCases[caseResultsFrozen].append(casesAsIndex[i])
        else: #means results obtained not obtained by previous cases
            resultByCases[caseResultsFrozen] = [casesAsIndex[i]]
    #print("result by cases")
    #print(resultByCases)
    return resultByCases

def discoverBestStrategies(objectives, allControls, budget):
    # for each asset in the objectives
    # remove those not in asset objectives

    totalObjectives = len(objectives)
    objectiveIndex = 0
    bestSolutions = [list(range(0, len(allControls)))]
    for objective in objectives:
        #print('objective index')
        #print(str(objectiveIndex))
        objectiveIndex += 1
        importantIndexes = []
        for subGoal in objective[0]:
            #print("subgoal")
            #print(subGoal)
            index = assets[subGoal[0]]
            for attackGoal in subGoal[1]:
                if attackGoal == "C":
                    importantIndexes.append(index + 0)
                elif attackGoal == "I":
                    importantIndexes.append(index + 1)
                else:  # A
                    importantIndexes.append(index + 2)
        solutions = []
        #print('important index')
        #print(importantIndexes)
        for bestSolution in bestSolutions:
            currStrategies = bestSolution
            solutions += Impl_discoverBestStrategies(importantIndexes, currStrategies, allControls, budget)
        #print('solutions')
        #print(solutions)
        bestSolutions = []
        bestEff = 0
        for solution in solutions:
            currEff = extractEffectivenessOfSolution(solution, allControls, importantIndexes)
            #print(currEff)
            if (currEff > bestEff):
                bestSolutions = []
                bestEff = currEff
                bestSolutions.append(solution)
            elif (currEff == bestEff):
                if solution not in bestSolutions:
                    bestSolutions.append(solution)

        if objectiveIndex == totalObjectives:  # done
            #print("returning")
            return bestSolutions
        else:
            #print('not done yet')
            bestSolutions = bestSolutions

def Impl_discoverBestStrategies(importantIndexes, currStrategies, allControls, budget):
    #if empty, just return that
    if len(currStrategies) == 0:
        return [currStrategies]
    # print("Set Of Startegies")
    # print(currStrategies)
    # find most expensive
    # Also check if feasible, if so, return
    #print('round')
    #print(currStrategies)
    mostExpensive = currStrategies[0]
    mostExpensiveIndexes = set()
    costOfSolution = 0
    for i in currStrategies:
        costOfSolution += allControls[i][2]
        # if mostExpensive == None:
        #     mostExpensive = currStrategies[i]
        #     mostExpensiveIndexes.add(i)
        if allControls[mostExpensive][2] < allControls[i][2]:
            mostExpensive = i
            mostExpensiveIndexes = set()
            mostExpensiveIndexes.add(i)
        elif allControls[mostExpensive][2] == allControls[i][2]:
            # mostExpensive = currStrategies[i]
            mostExpensiveIndexes.add(i)

    if (costOfSolution <= budget):
        #print("Cost of solution: " + str(costOfSolution))
        return [currStrategies]

    #find those with no dependents which are also most expensive
    #if has dependents, replace with leaf node dependents

    # leafNodesDependents = set()
    # for valueDeps in dependencies.values():
    #     for value in valueDeps:
    #         if value not in dependencies.keys():
    #             leafNodesDependents.add(value)
    highestCost = 0
    mostExpensiveIndexesNoDeps = set()
    for c in mostExpensiveIndexes:
        nodes = set()
        nodes.add(c)
        nodesSeen = set()
        nodesSeen.add(c)

        substitutionHappened = True
        while(substitutionHappened):
            substitutionHappened = False
            nodesCopy = deepcopy(nodes)
            for node in nodes:
                if node in dependencies: #implies could replace this control
                    for dep in dependencies[node]:
                        if dep in currStrategies: #means we should replace the node by its dependents
                            if node in nodesCopy:
                                nodesCopy.remove(node)

                            if dep not in nodesSeen: #to prevent circular dependencies
                            #     if dep in nodesCopy:
                            #         nodesCopy.remove(dep)
                            # else:

                                nodesCopy.add(dep)
                                nodesSeen.add(dep)
                                substitutionHappened = True

            nodes = nodesCopy



        # depsCopy = deepcopy(deps)
        #
        # for d in deps: #filter deps by controls which are in currStrategies
        #     if d not in currStrategies:
        #         depsCopy.remove(d)
        # mostExpensiveIndexesLeafs = depsCopy.intersection(leafNodesDependents) #could return empty of circular dependencies
        for leaf in nodes:
            if allControls[leaf][2] == highestCost:
                mostExpensiveIndexesNoDeps.add(leaf)
            elif allControls[leaf][2] > highestCost:
                highestCost = allControls[leaf][2]
                mostExpensiveIndexesNoDeps = set()
                mostExpensiveIndexesNoDeps.add(leaf)

    #check for circular dependencies
    if len(mostExpensiveIndexesNoDeps) != 0:
        mostExpensiveIndexes = mostExpensiveIndexesNoDeps
    #else: just stick with most expensive indexes

    # find least effective
    leastEffective = currStrategies[0]
    leastEffectiveIndexes = set()
    for i in currStrategies:

        if extractEffectiveness(allControls, leastEffective, importantIndexes, currStrategies) > extractEffectiveness(allControls,
                                                                                                        i,
                                                                                                        importantIndexes,
                                                                                                        currStrategies):

            leastEffective = i
            leastEffectiveIndexes = set()
            leastEffectiveIndexes.add(i)
        elif extractEffectiveness(allControls, leastEffective, importantIndexes, currStrategies) == extractEffectiveness(
                allControls, i, importantIndexes, currStrategies):
            # leastEffective = currStrategies[i]
            leastEffectiveIndexes.add(i)

    #remove controls that are parent nodes (i.e., have controls that depend on them)
    leastEffectiveIndexesNoDeps = set()
    for c in leastEffectiveIndexes:
        if not (c in dependencies and dependencies[c] in currStrategies): #means is not parent node
            leastEffectiveIndexesNoDeps.add(c)

    if len(leastEffectiveIndexesNoDeps) != 0: #means we did not only have circular dependencies
        leastEffectiveIndexes = leastEffectiveIndexesNoDeps
    #else: means we only had circular dependencies, stick with leasteffectiveindexes

    intersectionOfWorstControls = mostExpensiveIndexes.intersection(leastEffectiveIndexes)

    if len(intersectionOfWorstControls) != 0:
        #print("pretty bad control")

        copy = deepcopy(currStrategies)
        controlToRemove = intersectionOfWorstControls.pop()  # could be more than one, so pick randomly
        controlToRemoveDep = [] #keep track of dependents removed too
        # print(copy1)
        for c in findDependencies(controlToRemove):
            if c in copy:
                copy.remove(c)
                controlToRemoveDep.append(c)
        controlToRemoveDep.remove(controlToRemove)
        result = Impl_discoverBestStrategies(importantIndexes, copy, allControls, budget)

        return replaceResultsWithEquivControls( result, intersectionOfWorstControls, controlToRemove, controlToRemoveDep)
    else:  # must evaluate with most expensive and least effective
        leastEffective = [leastEffectiveIndexes.pop()] #find least0 effective that are also most expensive
        mostExpensive = [mostExpensiveIndexes.pop()] #find most expensive that are also least effective

        for index in leastEffectiveIndexes: #will not currently work with circ dependencies
            if allControls[index][2] > allControls[leastEffective[0]][2]: #check costs of least effective indexes
                leastEffective = [index] #if found one more expensive, reset list
            elif allControls[index][2] == allControls[leastEffective[0]][2]: #equal cost, add it to list
                leastEffective.append(index)

        for index in mostExpensiveIndexes:
            #if found one of lesser effectiveness, reset list
            if extractEffectiveness(allControls, index, importantIndexes, currStrategies) < extractEffectiveness(allControls,
                                                                                                    mostExpensive[0],
                                                                                                    importantIndexes,
                                                                                                    currStrategies):
                mostExpensive = [index]

            # equal effectiveness, add it to list
            elif extractEffectiveness(allControls, index, importantIndexes, currStrategies) == extractEffectiveness(allControls,
                                                                                                    mostExpensive[0],
                                                                                                    importantIndexes,
                                                                                                    currStrategies):
                mostExpensive.append(index)

        #at this point, we have indices of leastEffective controls with highest cost,
        #and mostExpensive controls with lowest effectiveness.
        result = list()

        #remove just one of the worst effective controls
        copy1 = deepcopy(currStrategies)
        toRemove1 = leastEffective.pop()
        controlToRemoveDep1 = [] #keep track of dependents removed too
        for c in findDependencies(toRemove1):
            if c in copy1:  # might have been removed earlier
                copy1.remove(c)
                controlToRemoveDep1.append(c)
        controlToRemoveDep1.remove(toRemove1)
        results1 = Impl_discoverBestStrategies(importantIndexes, copy1, allControls, budget)
        #we now have results, replace with equivalent controls
        result += replaceResultsWithEquivControls(results1, leastEffective, toRemove1, controlToRemoveDep1)

        haveEffNone = ( extractEffectiveness(allControls, toRemove1, importantIndexes, currStrategies) == 0 ) #check if least effective control was None

        # if the least effective has no effectiveness, we can still say this is the worst control 
        # as it does not contribute to our security goals in any way. We do this to help
        # optimize this logic (more efficient).
        if not haveEffNone: 
            # remove just one of the most costly controls
            copy2 = deepcopy(currStrategies)
            toRemove2 = mostExpensive.pop()
            controlToRemoveDep2 = [] #keep track of dependents removed too
            for c in findDependencies(toRemove2):
                if c in copy2:  # might have been removed earlier
                    copy2.remove(c)
                    controlToRemoveDep2.append(c)
            controlToRemoveDep2.remove(toRemove2)
            results2 = Impl_discoverBestStrategies(importantIndexes, copy2, allControls, budget)
            #we now have results, replace with equivalent controls
            result += replaceResultsWithEquivControls(results2, mostExpensive, toRemove2, controlToRemoveDep2)

        return result

        # for toRemove in mostExpensive: #for each most expensive found (that have lowest effectiveness)
        #     copy = deepcopy(currStrategies)
        #
        #     for c in findDependencies(toRemove):
        #         if c in copy:  # might have been removed earlier
        #             copy.remove(c)

        #   result += Impl_discoverBestStrategies(importantIndexes, copy, allControls, budget)

        #result += Impl_discoverBestStrategies(importantIndexes, copy1, allControls, budget)
        #result += Impl_discoverBestStrategies(importantIndexes, copy2, allControls, budget)

        #return result

def replaceResultsWithEquivControls( result, equivalentControls, controlRemoved, controlRemovedDep ):
    equivResults = []
    for combo in result:
        for control in equivalentControls:
            if control in combo:
                copy = deepcopy(combo)
                copy.remove(control)
                copy.append(controlRemoved)
                for dep in controlRemovedDep: #must add dependents that were removed with the control
                    copy.append(dep)
                # if by replacing with equivalent controls the dependencies are not respected, then this is not a solution
                if dependenciesHold(copy, controlRemoved, controlRemovedDep):
                    equivResults.append(copy)
    result += equivResults
    return result

def dependenciesHold(combo, controlRemoved, dependents):
    if controlRemoved in dependenciesInv:
        for c in dependenciesInv[controlRemoved]:
            if c not in combo:
                return False

    for dep in dependents:
        if dep in dependenciesInv:
            for c in dependenciesInv[dep]:
                if c not in combo:
                    return False

    return True

def extractEffectiveness(controls, controlIndex, importantIndexes, currStrategies):
    indexesToCombineFresh = findDependencies(controlIndex)

    indexesToCombine = set()
    for i in indexesToCombineFresh:
        if i in currStrategies:
            indexesToCombine.add(i)

    eff = 0
    #print("hi")
    #print(importantIndexes)
    #print(controlIndex)
    for i in importantIndexes:
        eff += combineEffectiveness(indexesToCombine, controls, i)
    return eff

def findDependencies(controlIndex):
    indexesToCombine = set()
    indexesToCombine.add(controlIndex)
    sizeChanged = True
    while (sizeChanged):
        oldSize = len(indexesToCombine)
        indexesToAdd = set()
        for c in indexesToCombine:
            if c in dependencies:
                indexesToAdd.update(dependencies[c])
        indexesToCombine.update(indexesToAdd)
        #print('combine')
        #print(indexesToCombine)
        sizeChanged = (oldSize != len(indexesToCombine))

    return indexesToCombine

def combineEffectiveness(controlIndexes, controls, index):
    tempEff = 1
    for i in controlIndexes:
        tempEff = tempEff * (1 - extractMetricValue(controls[i][index]))
    return 1 - tempEff

def extractMetricValue(metric):
    return metrics[metric.lower()]


def extractEffectivenessOfSolution(solution, allControls, importantIndexes):
    eff = 0
    #print('here we go')
    for i in importantIndexes:
        tempEff = 1
        for c in solution:
            tempEff = tempEff * (1 - extractMetricValue(allControls[c][i]))
        eff += (1 - tempEff)
    return eff


def getResults(data, assetsParam, objectivePriorities, budget):
    global assets
    global dependencies
    global dependenciesInv

    assets = assetsParam

    dependencies = dict()
    dependenciesInv = dict()

    costOfSolution = 0
    strategy = []
    optionalControls = []
    mandatoryControls = []

    dependenciesTemp = dict()
    for index, row in data.iloc[1:].iterrows():
        if row["Required?"].upper() == "Y":
            mandatoryControls.append(row)
            costOfSolution += row["Cost"]
        else:
            dependentData = row["Dependencies"]
            try:
                if str(dependentData).strip() != '':  # there are dependencies
                    dependents = []
                    for dependent in dependentData.split(","):
                        dependents.append(dependent.strip())
                    dependenciesTemp[len(optionalControls)] = dependents
            except Exception:
                print("No Dependencies")
            optionalControls.append(row)
    print('dependenciesTemp')
    print(dependenciesTemp)

    for dependency in dependenciesTemp.keys():
        # dependencyAsIndexes = []
        for specificDependency in dependenciesTemp[dependency]:
            for i in range(len(optionalControls)):  # find index of each specific dependency
                if optionalControls[i][0] == specificDependency:  # means it is the index it is dependent on
                    #the dependencies dict
                    if i in dependencies:  # entry exists
                        dependencies[i].append(dependency)
                    else:
                        dependencies[i] = [dependency]

                    #the dependenciesInv dict
                    if dependency in dependenciesInv:
                        dependenciesInv[dependency].append(i)
                    else:
                        dependenciesInv[dependency] = [i]

    print(dependencies)

    objectivesToPass = []
    for order in objectivePriorities.split(">"):
        orderedObjectives = []
        for assetDef in order.split("&"):
            assetName = assetDef.split("{")[0]
            objectives = re.findall(r'\{.*?\}', assetDef)
            objectivesList = []
            for objective in objectives[0].split(","):
                objectivesList.append(objective.replace('{','').replace('}',''))
            orderedObjectives.append(  (assetName, objectivesList, ) )
        objectivesToPass.append( ( orderedObjectives, )  )
    print(objectivesToPass)

    totalBudget = int(budget) #passed in as parameter
    budgetLeft = totalBudget - costOfSolution
    print("Money Left: " + str(budgetLeft))
    # currOptionalStrategies = []
    # for each objective priority
    start = time.time()
    resultByCases = discoverCases(objectivesToPass, optionalControls, budgetLeft) #= discoverBestStrategies(objectivesToPass, optionalControls, budgetLeft)
    end = time.time()
    print('result')
    # result.sort()
    print(resultByCases)

    convert = str(datetime.timedelta(seconds = (end - start)))
    print("time")
    print(convert)

    return resultByCases, optionalControls, mandatoryControls