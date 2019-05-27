from graphics import *
import sys
import math
import os
import copy

nodes = {}
links = {}
redLinks = []
greenCircle = ""
roundTxt = ""
roundNum = 0
win = ""
routing = {}
tables = []
neighbors = {}
windowOpen = True
circles = {}
colorTrack = {}


def erase_routing():
    for r in tables:
        r.setText("")

def display_routing():
    global routing
    global win
    global tables
    erase_routing()
    yCoord = 12*len(routing)
    yAdd = 20*len(routing)
    xCoord = 780
    if (len(routing)<4):
        yCoord = 80
        yAdd = 80
    for name in sorted(routing.keys()):
        routeString = name+"\n Dest.     Next     Cost \n"
        for other in sorted(routing[name].keys()):
            routeString+=other+"           "+routing[name][other][0]+"           "
            cost = routing[name][other][1]
            if (len(routing[name][other][1]) == 1):
                routeString+=" "+routing[name][other][1]+"\n"
            else:
                routeString+=routing[name][other][1]+"\n"
        routeString+="\n"
        entry = Text(Point(xCoord,yCoord), routeString).draw(win)
        # entry.setFace('arial')
        tables.append(entry)
        yCoord+=yAdd
        if yCoord >=550:
            xCoord +=135
            yCoord = 12*len(routing)

def advance():
    global routing
    routingC = copy.deepcopy(routing)
    for n in routingC:
        for nbr in neighbors[n]:
            linkWeight = int(neighbors[n][nbr])
            if routing[n][nbr][1]=="inf" or linkWeight<int(routing[n][nbr][1]):
                routing[n][nbr] = (nbr,str(linkWeight))
            if routing[n][nbr][1]!="inf" and routing[n][nbr][0]!=nbr and routingC[routing[n][nbr][0]][nbr][1]=="inf": #poison
                routing[n][nbr] = (nbr,str(linkWeight))
            for other in routingC[nbr]:
                if other!=n:
                    newCost = routingC[nbr][other][1]
                    oldCost = routing[n][other][1]
                    if oldCost!="inf":
                        nextHop = routing[n][other][0]
                        nextHopWeight = neighbors[n][nextHop]
                        if (nextHop!=other and routingC[nextHop][other][1]=="inf"):
                            routing[n][other] = ("--","inf")
                        elif (nextHop!=other and 
                            int(routingC[nextHop][other][1])+int(nextHopWeight)!=int(oldCost)):
                            routing[n][other] = (nextHop,str(int(nextHopWeight)+int(routingC[nextHop][other][1])))

                    if (routing[n][other][0]== nbr  and newCost=="inf"):        #poison
                        routing[n][other] = ("--","inf")
                    elif newCost !="inf" and (oldCost=="inf" or 
                        int(newCost)+linkWeight<int(oldCost)):
                        if not routingC[nbr][other][0]==n:
                            routing[n][other] = (nbr,str(linkWeight+int(newCost)))
    display_routing()
    if greenCircle!="":
        for l in links:
            if not l in redLinks:
                l.setFill('black')
        highlightPaths(greenCircle)


def in_circle(center, radius, x, y):
    square_dist = (center.x - x) ** 2 + (center.y - y) ** 2
    return square_dist <= radius ** 2

def distance(a,b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def is_between(a,c,b):
    tmp = distance(a,c) + distance(c,b)
    if (tmp + 1 >= distance(a,b) and tmp - 1 <= distance(a,b) ):
        return True
    else:
        return False

def failLink(l):
    a = links[l][0]
    b = links[l][1]
    weight = links[l][2]
    del neighbors[a][b]
    del neighbors[b][a]
    for cons in routing[a]:
        nextHop = routing[a][cons][0]
        if nextHop==b:
            if cons in neighbors[a]:
                newW = neighbors[a][cons]
                routing[a][cons] = (cons,newW)
            else:
                routing[a][cons] = ("--","inf")
    for cons in routing[b]:
        nextHop = routing[b][cons][0]
        if nextHop==a:
            if cons in neighbors[b]:
                newW = neighbors[b][cons]
                routing[b][cons] = (cons,newW)
            else:
                routing[b][cons] = ("--","inf")
    display_routing()
    if greenCircle!="":
        for l in links:
            if not l in redLinks:
                l.setFill('black')
        highlightPaths(greenCircle)

def recoverLink(l):
    a = links[l][0]
    b = links[l][1]
    weight = links[l][2]
    neighbors[a][b] = weight
    neighbors[b][a] = weight
    if (routing[a][b][1]=="inf" or int(routing[a][b][1]) > int(weight)):
        routing[a][b] = (b, weight)
    if (routing[b][a][1]=="inf" or int(routing[b][a][1]) > int(weight)):
        routing[b][a] = (a, weight)
    display_routing()
    if greenCircle!="":
        for l in links:
            if not l in redLinks:
                l.setFill('black')
        highlightPaths(greenCircle)

def highlightPaths(c):
    global routing
    for r in routing:
        if not r==c:
            nextHop = routing[r][c][0]
            for l in links:
                if ((links[l][0]==r and links[l][1]==nextHop) or 
                    (links[l][1]==r and links[l][0]==nextHop)):
                    l.setFill('green')
                    l.setArrow("both")

def click(e):
    global links
    global nodes
    global roundTxt
    global roundNum
    global win
    global windowOpen
    global greenCircle
    global circles 
    global colorTrack

    x, y = e.x, e.y
    if (x <= 680 and x >=600 and y<=580 and y>=550):
        roundNum+=1
        roundTxt.setText("Round: "+str(roundNum))
        advance()
        return
    if (x <= 580 and x >= 500 and y <=580 and y>=550):
        refresh()
        return
    if (x <= 480 and x >= 400 and y <=580 and y>=550):
        win.close()
        return
    for c in circles:
        circ = circles[c]
        if in_circle(circ.getCenter(),20,x,y):
            if greenCircle == "":
                greenCircle = c
                for c2 in circles:
                    if c2==c:
                        circ.setFill('green')
                    else:
                        circles[c2].setFill('white')
                highlightPaths(c)
            elif not c == greenCircle:
                greenCircle = c
                for c2 in circles:
                    if c2==c:
                        circ.setFill('green')
                    else:
                        circles[c2].setFill('white')
                for l in links:
                    if not l in redLinks:
                        l.setFill('black')
                highlightPaths(c)
            else:
                greenCircle = ""
                for c2 in circles:
                    circles[c2].setFill(colorTrack[c2])
                for l in links:
                    if not l in redLinks:
                        l.setFill('black')
            return
    for l in links:
        start, end = l.getP1(),l.getP2()
        if is_between(start,Point(x,y),end):
            if not l in redLinks:
                l.setFill('red')
                redLinks.append(l)
                failLink(l)
            else:
                try:
                    redLinks.remove(l)
                    l.setFill('black')
                    recoverLink(l)
                except:
                    return

def refresh():
    global greenCircle
    global nodes
    global neighbors
    global routing
    global redLinks
    global circles
    global links 
    global roundTxt
    global roundNum
    for l in redLinks:
        a = links[l][0]
        b = links[l][1]
        weight = links[l][2]
        neighbors[a][b] = weight
        neighbors[b][a] = weight
    for name in nodes:
        for n2 in nodes:
            if n2 in neighbors[name]:
                routing[name][n2] = (n2,neighbors[name][n2])
            elif not n2==name:
                routing[name][n2] = ("--","inf")
    greenCircle = ""
    for c2 in circles:
        circles[c2].setFill(colorTrack[c2])
    for li in links:
            li.setFill('black')
    redLinks = []
    roundTxt.setText("Round: 0")
    roundNum = 0
    display_routing()

def main(coordFile,linkFile):
    global nodes
    global win
    global links
    global routing
    global neighbors
    global colorTrack
    cLines = open(coordFile, "r").readlines()
    lLines = open(linkFile, "r").readlines()

    win = GraphWin(width = 1250, height = 600) # create a window
    neighbors = {}
    for x in cLines:
        n = [s.strip() for s in x.split(',')]
        nodes[n[0]] = Point(n[1],n[2])
        neighbors[n[0]] = {}

    for x in lLines:
        link = [s.strip() for s in x.split(',')]
        start = nodes[link[0]]
        end = nodes[link[1]]
        weight = link[2]
        line = Line(start, end).draw(win)
        line.setWidth(7)
        if (start.x-end.x < 50 and start.x-end.x > -50):
            lineLabel = Text(Point(line.getCenter().x-20,line.getCenter().y), weight).draw(win)
        else:
            lineLabel = Text(Point(line.getCenter().x,line.getCenter().y -20), weight).draw(win)
        links[line] = (link[0],link[1], weight)

        neighbors[link[0]][link[1]] = weight
        neighbors[link[1]][link[0]] = weight
    c = 7
    colors = ["#f78a8a","#74d190", "#e07816", "#bcb7b3", "#c765d8", "#5395e0", "#eadd2c", "#a7c8ce",
                "#9e8091","#7c897a", "#bc9597", "#6f7696"]
    global circles
    for name in nodes:
        cir = Circle(nodes[name],20)
        circles[name] = cir
        colorTrack[name] = colors[c%12]
        cir.setFill(colors[c%12])
        cir.draw(win)
        message = Text(nodes[name], name).draw(win)
        routing[name] = {}
        for n2 in nodes:
            if n2 in neighbors[name]:
                routing[name][n2] = (n2,neighbors[name][n2])
            elif not n2==name:
                routing[name][n2] = ("--","inf")
        c+=1

    divider = Line(Point(700,0), Point(700,600)).draw(win)
    display_routing()

    forwardButton = Rectangle(Point(680,580),Point(600,550)).draw(win)
    forwardButton.setFill('#4286f4')
    advanceTxt = Text(Point(640,565), "Advance").draw(win)
    # Image(Point(580,565),"refresh1.gif").draw(win)
    refreshButton = Rectangle(Point(580,580),Point(500,550)).draw(win)
    refreshButton.setFill('#91d8d8')
    Text(Point(540,565), "Restart").draw(win)

    quitButton = Rectangle(Point(480,580),Point(400,550)).draw(win)
    quitButton.setFill('#a03b30')
    Text(Point(440,565), "Quit").draw(win)

    global roundTxt
    roundTxt = Text(Point(620,30), "Round 0").draw(win)
    roundTxt.setSize(20)
    roundTxt.setStyle("bold")
    win.bind("<Button-1>", click)
    while True:
        win.getMouse()
    # global windowOpen
    # while windowOpen:
    #   pass
    # print("closing")
    # win.close()

if __name__ == "__main__":
   cF = sys.argv[1]
   lF = sys.argv[2]
   main(cF,lF)

