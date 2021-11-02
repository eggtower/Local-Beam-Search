from function import func
import random;
import threading;
import sys;
import time;


class Ans:

    # constructor
    def __init__(self, x, y):
        # Minimum
        self.Min = func(x, y);
        # Array for recording minimum coordinate
        self.XY = [];
        self.XY.append([x, y]);

    # Methods
    # Check whether the output of input x,y is min or not
    def checkMin(self, Ans):
        if(Ans.Min < self.Min):
            self.Min = Ans.Min;
            self.XY = Ans.XY;
        elif(Ans.Min == self.Min):
            self.XY.extend(Ans.XY);
    
    # Print result
    def printResult(self):
        for XY in self.XY:
            print(format(XY[0], '.0f'));
            print(format(XY[1], '.0f'));
        print(format(self.Min, '.3f'));


class Point:

    # constructor
    def __init__(self, x, y):
        global XYRange;
        self.X = x;
        self.Y = y;
        self.MapX = x - XYRange[0][0] if(XYRange[0][0] != 0) else x;
        self.MapY = y - XYRange[1][0] if(XYRange[1][0] != 0) else y;        


def readData(): # Read input.txt for define upper/lower limits
    XYRange = [];
    with open("input.txt", "r") as file:
        for line in file.readlines():
            tmp = line.strip().split(",");
            num1 = int(tmp[0]);
            num2 = int(tmp[1]);
            if(num1 < num2):
                coordinate = [num1, num2];
            else:
                coordinate = [num2, num1];
            XYRange.append(coordinate);
    return XYRange;


def randomPoint():  # Determine the random point + Normalize the point for map
    global XYRange;
    x = random.randint(XYRange[0][0], XYRange[0][1]);
    y = random.randint(XYRange[1][0], XYRange[1][1]);
    point = Point(x, y);
    return point;


def thread(point, recursion=False):  # sub-thread for checking random point
    global Map;
    global LBS_ResultList;
    if(not Map[point.MapX][point.MapY]):
        Map[point.MapX][point.MapY] = 1;
        pointVal = Ans(point.X, point.Y);
        # add the local min point to list
        LBS_ResultList.append(pointVal);
    if(recursion):
        aroundMinRes = checkAround(point);
        if(aroundMinRes is not None):
            LBS_ResultList.append(aroundMinRes);
            aroundMinPoint = Point(aroundMinRes.XY[0][0], aroundMinRes.XY[0][1]);
            threading.Thread(target=thread(aroundMinPoint, True));

        
def checkAround(point):  # check the target point's neighbors
    global XYRange;
    global Map;
    global Arounds;
    aroundMin = None;
    for around in Arounds:
        aroundPoint = Point(point.X + around[0], point.Y + around[1]);
        # check whether the neighbor point out of the XYrange
        if(aroundPoint.X >= XYRange[0][0] and aroundPoint.X <= XYRange[0][1] 
            and aroundPoint.Y >= XYRange[1][0] and aroundPoint.Y <= XYRange[1][1]):
            # if the point hasn't checked, compare with the neighbor(local) minimum
            if(not Map[aroundPoint.MapX][aroundPoint.MapY]):
                Map[aroundPoint.MapX][aroundPoint.MapY] = 1; # sign the coordinate on Map as true
                if(aroundMin is None):
                    aroundMin = Ans(aroundPoint.X, aroundPoint.Y);
                else:
                    tmp = Ans(aroundPoint.X, aroundPoint.Y);
                    aroundMin.checkMin(tmp);
    if(aroundMin is not None):
        return aroundMin;
    else:
        return None;


def LocalBeamSearch(k, Map):
    global LBS_ResultList;
    threads = [];  # sub-threads
    for i in range(k):
        # generate random points
        point = randomPoint();
        while(Map[point.MapX][point.MapY]):
            point = randomPoint();
        # put the random point into sub-threads
        threads.append(threading.Thread(target=thread(point, True)));
        threads[i].start();
    
    for i in range(k):
        threads[i].join();
    
    # setting the first Local Beam Search result as Ans, and start to compare each result in the list
    LBS_Result = Ans(LBS_ResultList[0].XY[0][0], LBS_ResultList[0].XY[0][1]);
    for result in LBS_ResultList:
        LBS_Result.checkMin(result);
    LBS_Result.printResult();
    

if __name__ == '__main__':
    XYRange = readData();
    time_start = time.time();  # start to time
    # a
    Map = [];  # Declare a map for record each coordinate(x, y) which is arrive or not
    for i in range(XYRange[0][1] - XYRange[0][0] + 1):
        tmp = [];
        for j in range(XYRange[1][1] - XYRange[1][0] + 1):
            tmp.append(0);
        Map.append(tmp);
    
    Arounds = [];  # Around coordinate
    radius = 2;  # setting the neighbor radius ( radius >= 2, radius <= Y range )
    for i in range(-1, radius + 1):
        for j in range(-1, radius + 1):
            tmp = [];
            if(i != 0 or j != 0):
                tmp.extend([i, j]);
                Arounds.append(tmp);
                
    k = 30;  # parallel    
    # records of each local minimum
    # [ Ans, Ans, ...]
    LBS_ResultList = [];  
    LocalBeamSearch(k, Map);
    
    time_end = time.time();  # end time
    time_c = time_end - time_start;  # the spending time of LBS
    print('LBS time cost', time_c, 's')
