import itertools
import json
from copy import deepcopy
import random
import pandas
import re
from natsort import natsorted
import math
from PyQt5.QtWidgets import QPushButton,QTextEdit, QApplication,QLineEdit,QWidget,QHBoxLayout,QGridLayout,QFileDialog, QLabel, QPushButton
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from PyQt5.QtCore import Qt, QDir
from pyqtspinner import WaitingSpinner
import sys
from threading import Thread
# Opening JSON file
#f = open('assetControls.json')

# returns JSON object as
# a dictionary
#data = json.load(f)

class FileBrowser(QWidget):
    OpenFile = 0
    OpenFiles = 1
    OpenDirectory = 2
    SaveFile = 3

    def __init__(self, title, mode=OpenFile):
        QWidget.__init__(self)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.browser_mode = mode
        self.filter_name = 'All files (*.*)'
        self.dirpath = QDir.currentPath()

        # self.label = QLabel()
        # self.label.setText(title)
        # self.label.setFixedWidth(65)
        # self.label.setFont(QFont("Arial", weight=QFont.Bold))
        # self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # layout.addWidget(self.label)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFixedWidth(400)

        layout.addWidget(self.lineEdit)

        self.button = QPushButton('Search')
        self.button.clicked.connect(self.getFile)
        layout.addWidget(self.button)
        layout.addStretch()

    # --------------------------------------------------------------------
    # For example,
    #    setMode(FileBrowser.OpenFile)
    #    setMode(FileBrowser.OpenFiles)
    #    setMode(FileBrowser.OpenDirectory)
    #    setMode(FileBrowser.SaveFile)
    def setMode(mode):
        self.mode = mode

    # --------------------------------------------------------------------
    # For example,
    #    setFileFilter('Images (*.png *.xpm *.jpg)')
    def setFileFilter(text):
        self.filter_name = text
        # --------------------------------------------------------------------

    def setDefaultDir(path):
        self.dirpath = path

    # --------------------------------------------------------------------
    def getFile(self):
        self.filepaths = []

        if self.browser_mode == FileBrowser.OpenFile:
            self.filepaths.append(QFileDialog.getOpenFileName(self, caption='Choose File',
                                                              directory=self.dirpath,
                                                              filter=self.filter_name)[0])
        elif self.browser_mode == FileBrowser.OpenFiles:
            self.filepaths.extend(QFileDialog.getOpenFileNames(self, caption='Choose Files',
                                                               directory=self.dirpath,
                                                               filter=self.filter_name)[0])
        elif self.browser_mode == FileBrowser.OpenDirectory:
            self.filepaths.append(QFileDialog.getExistingDirectory(self, caption='Choose Directory',
                                                                   directory=self.dirpath))
        else:
            options = QFileDialog.Options()
            if sys.platform == 'darwin':
                options |= QFileDialog.DontUseNativeDialog
            self.filepaths.append(QFileDialog.getSaveFileName(self, caption='Save/Save As',
                                                              directory=self.dirpath,
                                                              filter=self.filter_name,
                                                              options=options)[0])
        if len(self.filepaths) == 0:
            return
        elif len(self.filepaths) == 1:
            self.lineEdit.setText(self.filepaths[0])
        else:
            self.lineEdit.setText(",".join(self.filepaths))
            # --------------------------------------------------------------------

    def setLabelWidth(self, width):
        self.label.setFixedWidth(width)
        # --------------------------------------------------------------------

    def setlineEditWidth(self, width):
        self.lineEdit.setFixedWidth(width)

    # --------------------------------------------------------------------
    def getPaths(self):
        return self.filepaths

class lineEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # e1 = QLineEdit()
        # e1.setValidator(QIntValidator())
        # e1.setMaxLength(4)
        # e1.setAlignment(Qt.AlignRight)
        # e1.setFont(QFont("Arial", 20))
        #
        # e2 = QLineEdit()
        # e2.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.e3 = QLineEdit()
        self.e3.setInputMask("9999999")
        self.objectiveBox = QLineEdit()
        self.button = QPushButton("Submit")
        self.resultBox = QTextEdit()
        #self.resultBox.setDisabled(True)
        #self.resultBox.resize(400, 300)

        fileDialog = QFileDialog()

        self.fileFB = FileBrowser('Open File', FileBrowser.OpenFile)


        # e5 = QLineEdit()
        # e5.setEchoMode(QLineEdit.Password)
        #
        # e6 = QLineEdit("Hello PyQt5")
        # e6.setReadOnly(True)
        # e5.editingFinished.connect(self.enterPress)
        controlFileLabel = QLabel("Specification File")
        budgetLabel = QLabel("Budget")
        self.objectiveLabel = QLabel("Objectives")
        flo = QGridLayout()
        # flo.addRow("integer validator", e1)
        # flo.addRow("Double validator", e2)
        flo.addWidget(controlFileLabel, 0, 0)
        flo.addWidget(self.fileFB, 0, 1)
        flo.addWidget(budgetLabel, 1, 0)
        flo.addWidget(self.e3, 1, 1)
        flo.addWidget(self.objectiveLabel,2,0)
        flo.addWidget(self.objectiveBox,2,1)
        flo.addWidget(self.button, 3, 0)
        flo.addWidget(self.resultBox, 4, 0, 2, 2)

        self.button.clicked.connect(self.runProgram)
        #flo.addWidget(fileDialog, 0, 2)
        # flo.addRow("Text changed", e4)
        # flo.addRow("Password", e5)
        # flo.addRow("Read Only", e6)

        self.setLayout(flo)
        self.setWindowTitle("Game Tool")

    def runProgram(self, text):
        def discoverBestStrategies(objectives, allControls, budget):
            # for each asset in the objectives
            # remove those not in asset objectives

            totalObjectives = len(objectives)
            objectiveIndex = 0
            bestSolutions = [list(range(0, len(allControls)))]
            for objective in objectives:
                print('objective index')
                print(str(objectiveIndex))
                objectiveIndex += 1
                importantIndexes = []
                for subGoal in objective[0]:
                    print("subgoal")
                    print(subGoal)
                    index = assets[subGoal[0]]
                    for attackGoal in subGoal[1]:
                        if attackGoal == "C":
                            importantIndexes.append(index + 0)
                        elif attackGoal == "I":
                            importantIndexes.append(index + 1)
                        else:  # A
                            importantIndexes.append(index + 2)
                solutions = []
                print('important index')
                print(importantIndexes)
                for bestSolution in bestSolutions:
                    currStrategies = bestSolution
                    solutions += Impl_discoverBestStrategies(importantIndexes, currStrategies, allControls, budget)
                print('solutions')
                print(solutions)
                bestSolutions = []
                bestEff = 0
                for solution in solutions:
                    currEff = extractEffectivenessOfSolution(solution, allControls, importantIndexes)
                    print(currEff)
                    if (currEff > bestEff):
                        bestSolutions = []
                        bestEff = currEff
                        bestSolutions.append(solution)
                    elif (currEff == bestEff):
                        if solution not in bestSolutions:
                            bestSolutions.append(solution)

                if objectiveIndex == totalObjectives:  # done
                    print("returning")
                    return bestSolutions
                else:
                    print('not done yet')
                    bestSolutions = bestSolutions

        def Impl_discoverBestStrategies(importantIndexes, currStrategies, allControls, budget):

            # print("Set Of Startegies")
            # print(currStrategies)
            # find most expensive
            # Also check if feasible, if so, return
            print('round')
            print(currStrategies)
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
                print("Cost of solution: " + str(costOfSolution))
                return [currStrategies]

            # find least effective
            leastEffective = currStrategies[0]
            leastEffectiveIndexes = set()
            for i in currStrategies:
                # if leastEffective == None:
                #     leastEffective = currStrategies[i]
                #     leastEffectiveIndexes.add(i)
                if extractEffectiveness(allControls, leastEffective, importantIndexes) > extractEffectiveness(allControls,
                                                                                                              i,
                                                                                                              importantIndexes):
                    leastEffective = i
                    leastEffectiveIndexes = set()
                    leastEffectiveIndexes.add(i)
                elif extractEffectiveness(allControls, leastEffective, importantIndexes) == extractEffectiveness(
                        allControls, i, importantIndexes):
                    # leastEffective = currStrategies[i]
                    leastEffectiveIndexes.add(i)
            # print("Most Expensive")
            # print(mostExpensive)
            # print("Most Expensive Index")
            # print(mostExpensiveIndex)
            # print("Least Effective")
            # print(leastEffective)
            # print("Least Effective Index")
            # print(leastEffectiveIndex)

            intersectionOfWorstControls = mostExpensiveIndexes.intersection(leastEffectiveIndexes)

            copy1 = deepcopy(currStrategies)
            if len(intersectionOfWorstControls) != 0:
                print("pretty bad control")
                controlToRemove = random.choice(
                    tuple(intersectionOfWorstControls))  # could be more than one, so pick randomly
                # print(copy1)
                for c in findDependencies(controlToRemove):
                    if c in copy1:
                        copy1.remove(c)
                return Impl_discoverBestStrategies(importantIndexes, copy1, allControls, budget)
            else:  # must evaluate with most expensive and least effective
                copy2 = deepcopy(currStrategies)
                leastEffective = leastEffectiveIndexes.pop()
                mostExpensive = mostExpensiveIndexes.pop()

                for index in leastEffectiveIndexes:
                    if allControls[index][2] > allControls[leastEffective][2]:
                        leastEffective = index

                for index in mostExpensiveIndexes:
                    if extractEffectiveness(allControls, index, importantIndexes) < extractEffectiveness(allControls,
                                                                                                         mostExpensive,
                                                                                                         importantIndexes):
                        mostExpensive = index

                for c in findDependencies(leastEffective):
                    if c in copy1:  # might have been removed earlier
                        copy1.remove(c)
                # print(copy2)
                for c in findDependencies(mostExpensive):
                    if c in copy2:
                        copy2.remove(c)

                result = list()

                result += Impl_discoverBestStrategies(importantIndexes, copy1, allControls, budget)
                result += Impl_discoverBestStrategies(importantIndexes, copy2, allControls, budget)

                return result

        def extractEffectiveness(controls, controlIndex, importantIndexes):
            indexesToCombine = findDependencies(controlIndex)

            eff = 0
            print("hi")
            print(importantIndexes)
            print(controlIndex)
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
                print('combine')
                print(indexesToCombine)
                sizeChanged = (oldSize != len(indexesToCombine))

            return indexesToCombine

        def combineEffectiveness(controlIndexes, controls, index):
            tempEff = 1
            for i in controlIndexes:
                tempEff = tempEff * (1 - controls[i][index])
            return 1 - tempEff

        def extractEffectivenessOfSolution(solution, allControls, importantIndexes):
            eff = 0
            print('here we go')
            for i in importantIndexes:
                tempEff = 1
                for c in solution:
                    tempEff = tempEff * (1 - allControls[c][i])
                eff += (1 - tempEff)
            return eff

        # def threaded_function():


        data = pandas.read_excel(self.fileFB.lineEdit.text())

        # thread = Thread(target=threaded_function, args=())
        # thread.start()
        # thread.join()
        self.resultBox.clear()
        self.button.setEnabled(False)

        #spinner = WaitingSpinner(self, True, True, Qt.ApplicationModal)
        #spinner.start()
        self.update()
        QApplication.processEvents()

        assets = {}
        dependencies = dict()

        i = 4
        while (i < len(data.columns)):
            assets[data.columns[i]] = i
            i += 3

        # Iterating through the json
        # list

        # results = open("results.txt", "w")

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

        print(dependenciesTemp)
        for dependency in dependenciesTemp.keys():
            # dependencyAsIndexes = []
            for specificDependency in dependenciesTemp[dependency]:
                for i in range(len(optionalControls)):  # find index of each specific dependency
                    if optionalControls[i][0] == specificDependency:  # means it is the index it is dependent on
                        if i in dependencies:  # entry exists
                            dependencies[i].append(dependency)
                        else:
                            dependencies[i] = [dependency]

        print(dependencies)

        objectivePriorities = "Sensor{C,I}>Sensor{A}&Database{C}" # "Sensor{C,I}>Sensor{A}&Database{C}"
        objectivePriorities = self.objectiveBox.text().strip()
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

        #objectivesToPass = [([("Sensor", ["C"])],)]
        #print(objectivesToPass)

        totalBudget = float(self.e3.text()) #100
        budgetLeft = totalBudget - costOfSolution
        print("Money Left: " + str(budgetLeft))
        # currOptionalStrategies = []
        # for each objective priority

        results = discoverBestStrategies(objectivesToPass, optionalControls, budgetLeft)
        print('result')
        # result.sort()
        print(results)  # TODO: make sure to not show as index
        resultNum = 1
        for result in results:
            self.resultBox.append('result '+ str(resultNum))
            #print()
            controlNames = []
            for control in mandatoryControls:
                controlNames.append(control[0])

            for optIndex in result:
                controlNames.append(optionalControls[optIndex][0])
            for x in natsorted(controlNames):
                #print(x)
                self.resultBox.append("\t" + x)
            resultNum += 1
            #print(controlNames)

        self.button.setEnabled(True)
        print('Done!')
        #spinner.stop()
        # Closing file
        # f.close()
        # --------------------






    def enterPress(self):
        print("Enter pressed")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = lineEditDemo()
    win.show()
    sys.exit(app.exec_())