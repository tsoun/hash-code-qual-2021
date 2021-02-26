# Von diesen Straßen wird bleiben: der durch sie hindurchging, der Wind!
howManyIntersectionsWithSchedule = 0
intersectionsWithSchedule = []


class Street:

    def __init__(self, streetID, beginPoint, endPoint, streetName, timeNeeded):
        self.carQueue = []
        self.carsToPass = 0
        self.streetID = streetID
        self.beginPoint = beginPoint
        self.endPoint = endPoint
        self.streetName = streetName
        self.timeNeeded = timeNeeded

    def enqueueCar(self, car):
        self.carQueue.append(car)

    def dequeueCar(self):
        return self.carQueue.pop(0)

    def setCarsToPass(self, carsToPass):
        self.carsToPass = carsToPass

    def addTrafficLight(self, trf):
        self.trafficLight = trf


class trafficLight:  # important shit
    def __init__(self, adjStreet):
        # object street (street of the end, id for the traffic light (?))
        self.adjStreet = adjStreet

    def setTiming(self, timing):
        self.timing = timing


class Intersection:

    def __init__(self, intersectionID):
        self.intersectionID = intersectionID
        self.totalDistance = 0
        self.junctions = 0
        self.incomingStreets = []
        self.outgoingStreets = []
        self.totalcars = 0
        # schedule[0] is the name of the incoming street, schedule[1] is the duration of the green light
        self.scheduling = []

    def setJunctions(self, junctions):
        self.junctions = junctions
    
    def setTotalCars(self, totalcars):
        self.totalcars = totalcars

    def addIncomingStreet(self, street):
        self.incomingStreets.append(street)

    def addOutgoingStreet(self, street):
        self.outgoingStreets.append(street)

    def addStreetWithGreenLight(self, schedule):
        self.scheduling.append(schedule)


class Car:

    def __init__(self, howManyStreets):
        self.streetsToCross = []
        self.distance = 0  # int
        self.howManyStreets = howManyStreets

    def addStreetToCross(self, street):
        self.streetsToCross.append(street)
        self.distance += street.timeNeeded


def inputData(carsList, streetsList, intersectionsList, howManyIntersections, howManyStreets, howManyCars):
    for i in range(howManyIntersections):  # initialize intersections
        intersectionsList.append(Intersection(i))
    for i in range(howManyStreets):  # initialize streets
        currentStreetLine = inputFile.readline().split(" ")
        beginPoint = intersectionsList[int(currentStreetLine[0])]
        endPoint = intersectionsList[int(currentStreetLine[1])]
        streetName = currentStreetLine[2]
        timeNeeded = int(currentStreetLine[3])
        currentStreet = Street(i, beginPoint, endPoint, streetName, timeNeeded)
        intersectionsList[int(currentStreetLine[0])
                          ].addOutgoingStreet(currentStreet)
        intersectionsList[int(currentStreetLine[1])
                          ].addIncomingStreet(currentStreet)
        streetsList.append(currentStreet)  # street created

    for i in range(howManyCars):  # initialize cars
        currentCarLine = inputFile.readline().split(" ")
        currentCar = Car(int(currentCarLine[0]))
        for j in range(currentCar.howManyStreets):  # add streets to cross
            for street in streetsList:
                if street.streetName == currentCarLine[j+1]:
                    currentCar.addStreetToCross(street)
                    break
        carsList.append(currentCar)


def calcCarsToPass(cars):       # regarding the streets
    for car in cars:
        for street in car.streetsToCross:
            street.carsToPass += 1


def calcJunctions(streets):
    for street in streets:
        street.endPoint.junctions += 1

def calcIntersectionCars(intersection):
    for street in intersection.incomingStreets:
        intersection.totalcars += street.carsToPass

def createTrafficLights(trafficLightsList, streets):
    for street in streets:
        trf = trafficLight(street)
        trafficLightsList.append(trf)
        street.addTrafficLight(trf)


def saveData(howManyReadyIntersections, readyIntersections):
    outputFile.write(str(howManyReadyIntersections) + "\n")
    for readyIntersection in readyIntersections:
        outputFile.write(str(readyIntersection.intersectionID) + "\n")
        howManySchedules = len(readyIntersection.scheduling)
        outputFile.write(str(howManySchedules) + "\n")
        for schedule in readyIntersection.scheduling:
            outputFile.write(schedule[0] + " " + str(schedule[1]) + "\n")


if __name__ == "__main__":
    inputFile = open("a.txt", "rt")  # IMPORTANT
    outputFile = open("aa.txt", "wt")
    carsList = []  # IMPORTANT
    streetsList = []
    intersectionsList = []
    trafficLightsList = []

    firstLineOfData = inputFile.readline().split(" ")

    simulationDuration = int(firstLineOfData[0])
    howManyIntersections = int(firstLineOfData[1])
    howManyStreets = int(firstLineOfData[2])
    howManyCars = int(firstLineOfData[3])
    scoreForReachingInTime = int(firstLineOfData[4])

    inputData(carsList, streetsList, intersectionsList, howManyIntersections,
              howManyStreets, howManyCars)
    inputFile.close()

    calcCarsToPass(carsList)
    calcJunctions(streetsList)
    createTrafficLights(trafficLightsList, streetsList)

    timeForEachIntersection = simulationDuration//howManyCars
    for intersection in intersectionsList:
        calcIntersectionCars(intersection)
        for incomingStreet in intersection.incomingStreets:
            #time = int(incomingStreet.carsToPass)*int(timeForEachIntersection)//(int(intersection.junctions)*int(totalcars))
            #print(timeForEachIntersection)
            x = incomingStreet.carsToPass
            incomingStreet.trafficLight.setTiming(
                1+incomingStreet.carsToPass*timeForEachIntersection//(1+intersection.junctions*intersection.totalcars))
            cycleList = [incomingStreet.streetName,
                         incomingStreet.trafficLight.timing]

            intersection.scheduling.append(cycleList)

        intersectionsWithSchedule.append(intersection)
        howManyIntersectionsWithSchedule += 1

    saveData(howManyIntersectionsWithSchedule, intersectionsWithSchedule)
    outputFile.close()
