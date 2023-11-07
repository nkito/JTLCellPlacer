import re
import sys


class WireSet:
    def __init__(self, wireList):
        self.set(wireList)

    def set(self, wireList):
        self.lWire = []
        for elem in wireList:
            self.lWire.append(elem)

        while True:
            removeList = []
            appendList = []
            for elem in self.lWire:
                for elem2 in self.lWire:
                    if elem == elem2:
                        continue

                    xs, ys = elem.startPoint()
                    l = elem2.getDistanceListFromSource(xs,ys)
                    if len(l) > 0 and l[0] > 0:
                        print(l)
                        nw = Wire(Wire.concat(elem2, elem))
                        elem.print()
                        print("->")
                        nw.print()
                        appendList.append( nw )
                        removeList.append( elem )
                        break

            if len(appendList) == 0:
                break
            self.lWire.extend(appendList)
            for de in removeList:
                self.lWire.remove(de)
        for elem in self.lWire:
            elem.print()



    def isOnRoute(self, x,y):
        for w in self.lWire:
            result = w.getDirectionOnPoint(x,y)
            if result != 0:
                return True
        return False

    def isEndPoint(self, x,y):
        for w in self.lWire:
            (xs,ys) = w.startPoint()
            (xe,ye) = w.endPoint()

            if x == xs and y == ys:
                return True
            if x == xe and y == ye:
                return True
        return False

    def getDistanceListFromSource(self, x,y):
        result = []
        for w in self.lWire:
            result.extend( w.getDistanceListFromSource(x,y) )
        return list(set(result))
    
    def checkDistance(self, xs,ys, xd,yd, distance):
        for w in self.lWire:
            if w.checkDistance(xs,ys, xd,yd, distance):
                return True
        return False

    # count the number of paths within (x,y) (x+size_x, y+size_y)
    def countNumThrough(self, x,y, size_x, size_y):
        result = []
        for w in self.lWire:
            result += w.countNumThroughList(x,y, size_x, size_y)
        return len( set(result) )


    def isAdjacent(self, xs,ys, xd,yd):
        for w in self.lWire:
            if w.isAdjacent(xs,ys, xd,yd):
                return True
        return False


class Wire:
    WIRE_NONE  = 0
    WIRE_X_POS = 1
    WIRE_X_NEG = 2
    WIRE_Y_POS = 4
    WIRE_Y_NEG = 8

    def __init__(self):
        self.lCorner = []

    def __init__(self, cornerList):
        self.set(cornerList)

    def set(self, cornerList):
        self.lCorner = []
        for elem in cornerList:
            self.lCorner.append(elem)

    def appendCoener(self, posx, posy):
        self.lCorner.append( (posx, posy) )
    
    def startPoint(self):
        return self.lCorner[0]
    
    def endPoint(self):
        return self.lCorner[-1]
    
    def getCorner(self, n):
        return self.lCorner[n]

    def print(self):
        print("Wire(" +str(self.lCorner) +")")

    def concat(w1, w2):
        lResult = []
        prevCorner = w1.lCorner[0]
        lResult.append(w1.lCorner[0])
        x,y = w2.startPoint()
        for e in w1.lCorner[1:]:
            if (x == e[0] and x == prevCorner[0] and 
                min(e[1], prevCorner[1]) <= y and
                max(e[1], prevCorner[1]) >= y):
                lResult.extend(w2.lCorner)
                return lResult
            if (y == e[1] and y == prevCorner[1] and 
                min(e[0], prevCorner[0]) <= x and
                max(e[0], prevCorner[0]) >= x):
                lResult.extend(w2.lCorner)
                return lResult
            prevCorner = e
            lResult.append(e)
        return lResult

    def isEndPoint(self, x,y):
        (xs,ys) = self.startPoint()
        (xe,ye) = self.endPoint()

        if (x == xs) and (y == ys):
            return True
        if (x == xe) and (y == ye):
            return True
        return False

    def isOnRoute(self, x,y):
        if self.getDirectionOnPoint(x,y) == 0:
            return False
        return True

    def getDirectionOnPoint(self, x,y):
        result = 0
        prevCorner = self.lCorner[0]
        for e in self.lCorner[1:]:
            if (x == e[0] and x == prevCorner[0] and 
                min(e[1], prevCorner[1]) <= y and
                max(e[1], prevCorner[1]) >= y):
                if e[1] > prevCorner[1]:
                    result = result | self.WIRE_Y_POS
                else:
                    result = result | self.WIRE_Y_NEG  
            if (y == e[1] and y == prevCorner[1] and 
                min(e[0], prevCorner[0]) <= x and
                max(e[0], prevCorner[0]) >= x):
                if e[0] > prevCorner[0]:
                    result = result |self.WIRE_X_POS
                else:
                    result = result |self.WIRE_X_NEG  
            prevCorner = e
        return result

    def getDistanceFromSource(self, x,y):
        result = 0
        prevCorner = self.lCorner[0]
        for e in self.lCorner[1:]:
            if (x == e[0] and x == prevCorner[0] and 
                min(e[1], prevCorner[1]) <= y and
                max(e[1], prevCorner[1]) >= y):
                return result + abs(y - prevCorner[1])
            if (y == e[1] and y == prevCorner[1] and 
                min(e[0], prevCorner[0]) <= x and
                max(e[0], prevCorner[0]) >= x):
                return result + abs(x - prevCorner[0])
            result += abs(prevCorner[1]-e[1]) + abs(prevCorner[0]-e[0])
            prevCorner = e
        return -1

    def getDistanceListFromSource(self, x,y):
        result = set()
        curDist = 0
        prevCorner = self.lCorner[0]
        for e in self.lCorner[1:]:
            if (x == e[0] and x == prevCorner[0] and 
                min(e[1], prevCorner[1]) <= y and
                max(e[1], prevCorner[1]) >= y):
                result.add( curDist + abs(y - prevCorner[1]) )
            if (y == e[1] and y == prevCorner[1] and 
                min(e[0], prevCorner[0]) <= x and
                max(e[0], prevCorner[0]) >= x):
                result.add( curDist + abs(x - prevCorner[0]) )
            curDist += abs(prevCorner[1]-e[1]) + abs(prevCorner[0]-e[0])
            prevCorner = e
        return list(result)

    def isAdjacent(self, xs,ys, xd,yd):
        lDist_s = self.getDistanceListFromSource(xs, ys)
        lDist_d = self.getDistanceListFromSource(xd, yd)
        if len(lDist_s) == 0 or len(lDist_d) == 0:
            return False
        for ds in lDist_s:
            if ds+1 in lDist_d:
                return True
        return False

    def checkDistance(self, xs,ys, xd,yd, distance):
        lDist_s = self.getDistanceListFromSource(xs, ys)
        lDist_d = self.getDistanceListFromSource(xd, yd)
        if len(lDist_s) == 0 or len(lDist_d) == 0:
            return False
        for ds in lDist_s:
            if ds+distance in lDist_d:
                return True
        return False

    def countNumThrough(self, x,y, size_x, size_y):
        result = 0
        insideMod = False
        prevCorner = self.lCorner[0]
        for e in self.lCorner[1:]:
            if e[0] == prevCorner[0]:
                if e[1] < prevCorner[1]:
                    for i in range(prevCorner[1], e[1]-1, -1):
                        if (e[0] >= x and e[0] < x+size_x) and (i >= y and i < y+size_y):
                            insideMod = True
                        else:
                            if insideMod:
                                result += 1
                            insideMod = False
                else:
                    for i in range(prevCorner[1], e[1]+1):
                        if (e[0] >= x and e[0] < x+size_x) and (i >= y and i < y+size_y):
                            insideMod = True
                        else:
                            if insideMod:
                                result += 1
                            insideMod = False
            if e[1] == prevCorner[1]:
                if e[0] < prevCorner[0]:
                    for i in range(prevCorner[0], e[0]-1, -1):
                        if (i >= x and i < x+size_x) and (e[1] >= y and e[1] < y+size_y):
                            insideMod = True
                        else:
                            if insideMod:
                                result += 1
                            insideMod = False
                else:
                    for i in range(prevCorner[0], e[0]+1):
                        if (i >= x and i < x+size_x) and (e[1] >= y and e[1] < y+size_y):
                            insideMod = True
                        else:
                            if insideMod:
                                result += 1
                            insideMod = False
            prevCorner = e
        return result

    def countNumThroughList(self, x,y, size_x, size_y):
        result = []
        insideMod = False
        prevCorner = self.lCorner[0]
        for e in self.lCorner[1:]:
            if e[0] == prevCorner[0]:
                if e[1] < prevCorner[1]:
                    for i in range(prevCorner[1], e[1]-1, -1):
                        if (e[0] >= x and e[0] < x+size_x) and (i >= y and i < y+size_y):
                            insideMod = True
                            xs = e[0]
                            ys = i
                        else:
                            if insideMod:
                                xe = e[0]
                                ye = i
                                result.append( ((xs,ys),(xe,ye)) )
                            insideMod = False
                else:
                    for i in range(prevCorner[1], e[1]+1):
                        if (e[0] >= x and e[0] < x+size_x) and (i >= y and i < y+size_y):
                            insideMod = True
                            xs = e[0]
                            ys = i
                        else:
                            if insideMod:
                                xe = e[0]
                                ye = i
                                result.append( ((xs,ys),(xe,ye)) )
                            insideMod = False
            if e[1] == prevCorner[1]:
                if e[0] < prevCorner[0]:
                    for i in range(prevCorner[0], e[0]-1, -1):
                        if (i >= x and i < x+size_x) and (e[1] >= y and e[1] < y+size_y):
                            insideMod = True
                            xs = i
                            ys = e[1]
                        else:
                            if insideMod:
                                xe = i
                                ye = e[1]
                                result.append( ((xs,ys),(xe,ye)) )
                            insideMod = False
                else:
                    for i in range(prevCorner[0], e[0]+1):
                        if (i >= x and i < x+size_x) and (e[1] >= y and e[1] < y+size_y):
                            insideMod = True
                            xs = i
                            ys = e[1]
                        else:
                            if insideMod:
                                xe = i
                                ye = e[1]
                                result.append( ((xs,ys),(xe,ye)) )
                            insideMod = False
            prevCorner = e
        return result
    def checkWireDirection(self, src_x, src_y, dest_x, dest_y):

        cx = self.lCorner[0][0]
        cy = self.lCorner[0][1]
        for c in self.lCorner:
            new_cx = c[0]
            new_cy = c[1]



class Grid:
    GRID_FREE   = 0
    GRID_IN_USE = 1

    def __init__(self, sizex, sizey):
        self.llGrid = []
        for x in range(sizex):
            yline = []
            for y in range(sizey):
                yline.append( self.GRID_FREE )
            self.llGrid.append( yline )
    
    def get(self, x, y):
        return self.llGrid[x][y]

    def set_emptylist(self):
        size = self.get_size()
        for x in range(size[0]):
            for y in range(size[1]):
                self.llGrid[x][y] = []

    def set(self, x, y, val):
        self.llGrid[x][y] = val

    def get_size(self):
        return (len(self.llGrid), len(self.llGrid[0]))

    def get_sizeX(self):
        return len(self.llGrid)

    def get_sizeY(self):
        return len(self.llGrid[0])

    def print(self):
        sSize = self.get_size()
        for y in range(sSize[1]):
            for x in range(sSize[0]):
                print(str(self.get(x,y)), end='')
            print("")
        print("")

    def isWirePlaced(self, lwireset):
        gridsize = self.get_size()

        for x in range( gridsize[0] ):
            for y in range( gridsize[1] ):
                for ws in lwireset:
                    if (ws.isOnRoute(x,y) and 
                        not( ws.isEndPoint(x,y)) and
                        len(self.get(x,y)) == 0 ):
                        return False
        return True

    def genILP(self, lwire, lwireset):
        gridsize = self.get_size()
        result = ""
        svar = set()


        ####################################################
        ##### This part generates a objective function #####
        ####################################################

        # result += "max: "
        # for i in range(len(lwire)):
        #     if i < len(lwireset[0].lWire):
        #         result += " - delay"+ str(i)
        #     else:
        #         result += " + delay"+ str(i)
        # result += ";\n\n"

        result += "min: "
#        result += "max: "
        for i in range(len(lwire)):
            if i < len(lwireset[0].lWire):
                result += " + delay"+ str(i)
            else:
                result += " - delay"+ str(i)
        result += " + ncell0;\n\n"

#        result += "min: + ncell0 "
#        for i in range(1, len(lwireset[1:])+1):
#            result += " - ncell"+ str(i)
#        result += ";\n\n"

#        result += "min: "
#        for i in range(len(lwire)):
#            result += " + delay"+ str(i)
#        result += ";\n\n"

        ####################################################

        sUsedGrid = set()

        wireidx = 0
        for w in lwire:
            scells_on_wire = set()
            for x in range( gridsize[0] ):
                for y in range( gridsize[1] ):
                    if (w.isOnRoute(x,y) and 
                        not(w.isEndPoint(x,y)) and
                        len(self.get(x,y)) != 0 ):
                        for c in self.get(x,y):
                            scells_on_wire.add(c)
                            sUsedGrid.add((x,y))
            if len(scells_on_wire) == 0 :
                result += " 0 "
            else:
                for c in scells_on_wire:
                    result += " + " + c
            result += " = delay" + str(wireidx) + ";\n"
            wireidx+=1

        wireidx = 0
        for ws in lwireset:
            scells_on_wire = set()
            for x in range( gridsize[0] ):
                for y in range( gridsize[1] ):
                    if (ws.isOnRoute(x,y) and 
                        not(ws.isEndPoint(x,y)) and
                        len(self.get(x,y)) != 0 ):
                        for c in self.get(x,y):
                            scells_on_wire.add(c)
            for c in scells_on_wire:
                result += " + " + c
            result += " = ncell" + str(wireidx) + ";\n"
            wireidx+=1

        result += "\n"
        for x in range( gridsize[0] ):
            for y in range( gridsize[1] ):
                if len( self.get(x,y) ) == 0:
#                if len( self.get(x,y) ) == 0 or not( (x,y) in sUsedGrid):
                    continue
                for c in self.get(x,y):
                    result += " + " + c
                    svar.add(c)
                result += " = 1;\n"

        # cnt = 0
        # result += "\n\nbin "
        # for v in svar:
        #     cnt += 1
        #     result += v
        #     result += ", " if cnt != len(svar) else ";"
        return result

class WCell:
    def __init__ (self, cell_name, lInOut, size_x, size_y):
        self.cell_name = cell_name
        self.linout = lInOut
        self.size_x = size_x
        self.size_y = size_y

    def copy (self):
        copy_linout = []

        for i in self.linout:
            copy_linout.append( ((i[0][0],i[0][1]),(i[1][0],i[1][1])) )
        
        return WCell(self.cell_name, copy_linout, self.size_x, self.size_y)

    def get_string_xy(self, x, y):
        return self.cell_name + "_" + str(x) + "_" + str(y)

    def mark_placeable_possition(self, grid, lWireSet):
        gridsize = grid.get_size()

        for x in range( gridsize[0] ):
            for y in range( gridsize[1] ):
                flip_rot = self.is_placeable_at(lWireSet, x,y)
                if len(flip_rot) == 0:
                    continue
                
                if flip_rot[1] % 2 == 0:
                    sx = self.size_x
                    sy = self.size_y
                else:
                    sx = self.size_y
                    sy = self.size_x
                name = self.get_string_xy(x,y)+"_"+str(flip_rot[0])+"_"+str(flip_rot[1])
                for gx in range(sx):
                    for gy in range(sy):
                        grid.get(x+gx,y+gy).append( name )

    def rot(self):
        orig_size_x = self.size_x
        orig_size_y = self.size_y

        self.size_x = orig_size_y
        self.size_y = orig_size_x

        new_linout = []
        for i in self.linout:
            # rotate clockwise
            in_pos  = i[0]
            out_pos = i[1]

            new_linout.append( (((orig_size_y-1 -  in_pos[1]),  in_pos[0]),
                ((orig_size_y-1 - out_pos[1]), out_pos[0])) )
        self.linout = new_linout
            

    def flip(self):
        new_linout = []
        for i in self.linout:
            in_pos  = i[0]
            out_pos = i[1]

            new_linout.append( (( in_pos[0], (self.size_y-1 -  in_pos[1])), 
                                (out_pos[0], (self.size_y-1 - out_pos[1]))))
        self.linout = new_linout

    def is_placeable_at(self, lWireSet, x, y):
        cop = self.copy()
        if( cop.is_placeable_with_currentPos(lWireSet, x, y) ):
            return (False, 0)
        cop.rot()
        if( cop.is_placeable_with_currentPos(lWireSet, x, y) ):
            return (False, 1)
        cop.rot()
        if( cop.is_placeable_with_currentPos(lWireSet, x, y) ):
            return (False, 2)
        cop.rot()
        if( cop.is_placeable_with_currentPos(lWireSet, x, y) ):
            return (False, 3)
        cop = self.copy()
        cop.flip()
        if( cop.is_placeable_with_currentPos(lWireSet, x, y) ):
            return (True, 0)
        cop.rot()
        if( cop.is_placeable_with_currentPos(lWireSet, x, y) ):
            return (True, 1)
        cop.rot()
        if( cop.is_placeable_with_currentPos(lWireSet, x, y) ):
            return (True, 2)
        cop.rot()
        if( cop.is_placeable_with_currentPos(lWireSet, x, y) ):
            return (True, 3)
        return ()

    def is_placeable_with_currentPos(self, lWireSet, x, y):
        lWireSetOnCell = []
        npath = 0
        for ws in lWireSet:
            pnum = ws.countNumThrough(x,y, self.size_x, self.size_y)
            if pnum != 0:
                lWireSetOnCell.append(ws)
                npath += pnum

        if npath != len(self.linout):
            return False

        matchCount = 0
        for i in self.linout:
            in_x  = i[0][0]
            in_y  = i[0][1]
            out_x = i[1][0]
            out_y = i[1][1]

            trim_in_x  = min(self.size_x-1, max(in_x,0))
            trim_in_y  = min(self.size_y-1, max(in_y,0))
            trim_out_x = min(self.size_x-1, max(out_x,0))
            trim_out_y = min(self.size_y-1, max(out_y,0))

            for ws in lWireSetOnCell:
                if (ws.isAdjacent(x+ in_x, y+ in_y, x+ trim_in_x, y+ trim_in_y) and
                    ws.isAdjacent(x+trim_out_x, y+trim_out_y, x+out_x, y+out_y) and
                    ws.checkDistance(x+in_x, y+in_y, x+out_x, y+out_y, 
                        ((2 if in_x==out_x and (in_x < 0 or in_x >= self.size_x) else 0) + abs(in_x-out_x)) + 
                        ((2 if in_y==out_y and (in_y < 0 or in_y >= self.size_y) else 0) + abs(in_y-out_y))
                                    ) and
                    ws.checkDistance(x+trim_in_x, y+trim_in_y, x+trim_out_x, y+trim_out_y, 
                        abs(trim_in_x-trim_out_x) + abs(trim_in_y-trim_out_y))
                    ):
                        matchCount+=1
                        break
        if matchCount == len(self.linout) :
            return True

        return False

    def print(self):
        print("CELL {} size=({},{})".format(self.cell_name, self.size_x, self.size_y))


def loadWireFromFile(filename):
    file = open(filename, 'rt')
    source_input = file.readlines()
    file.close()

    dWG = {}
    lLoadWire = []
    textLineNo = 0
    for line in source_input:
        textLineNo += 1
        if re.search(r"^wire:", line):
            lArgs = re.split(r":", line)
            validWire = True
            lw = []

            wireGroup = int(lArgs[1])
            if not(wireGroup in dWG):
                dWG[ wireGroup ] = []

            for arg in lArgs[2:]:
                lNum = re.split(",",arg)
                if len(lNum) != 2:
                    print("Syntax error: wire routing is specified in an incorrect form.")
                    validWire = False
                    continue
                lw.append( (int(lNum[0]), int(lNum[1])) )
            if validWire:
                w = Wire(lw)
                lLoadWire.append(w)
                dWG[wireGroup].append(w)

    lLoadWireSet = []
    for e in dWG:
        lLoadWireSet.append( WireSet(dWG[e]) )

    return lLoadWire, lLoadWireSet

lWcells = []

lWcells.append( WCell("jtl"        , [((-1,0),(1,0))], 1, 1) )
lWcells.append( WCell("jtl45deg"   , [((-1,1),(1,0))], 1, 2) )
lWcells.append( WCell("jtl45degc"  , [((-1,1),(1,0)),((0,2),(1,1))], 1, 2) )
lWcells.append( WCell("jtl45degcc" , [((-1,1),(1,0)),((0,2),(1,1)),((-1,0),(0,-1))], 1, 2) )
lWcells.append( WCell("jtl45degccr", [((-1,1),(1,0)),((1,1),(0,2)),((-1,0),(0,-1))], 1, 2) )
lWcells.append( WCell("jtl45degcr" , [((-1,1),(1,0)),((1,1),(0,2))], 1, 2) )
lWcells.append( WCell("jtl45degrc" , [((1,0),(-1,1)),((1,1),(0,2))], 1, 2) )
lWcells.append( WCell("jtl45degrcc", [((1,0),(-1,1)),((0,2),(1,1)),((-1,0),(0,-1))], 1, 2) )
lWcells.append( WCell("jtl45degrccr",[((1,0),(-1,1)),((0,2),(1,1)),((0,-1),(-1,0))], 1, 2) )
lWcells.append( WCell("jtl45degrcr", [((1,0),(-1,1)),((0,2),(1,1))], 1, 2) )

lWcells.append( WCell("jtlc", [((-1,0),(0,-1))], 1, 1) )
lWcells.append( WCell("jtlc2", [((-1,0),(1,-1))], 2, 1) )
lWcells.append( WCell("jtlc3", [((1,-1),(-1,0))], 2, 1) )

lWcells.append( WCell("jtlcc",    [((-1,0),(0,-1)),((0,1),(1,0))], 1, 1) )
lWcells.append( WCell("jtlccla",  [((-1,0),(0,-1)),((0,1),(2,0))], 2, 1) )
lWcells.append( WCell("jtlcclar", [((0,-1),(-1,0)),((2,0),(0,1))], 2, 1) )
lWcells.append( WCell("jtlccls",  [((-1,0),(1,-1)),((0,1),(2,0))], 2, 1) )

lWcells.append( WCell("jtlcclx1", [((-1,0),(1,-1)),((1,1),(0,-1)),((0,1),(2,0))], 2, 1) )
lWcells.append( WCell("jtlcclx2", [((-1,0),(1,-1)),((0,-1),(1,1)),((0,1),(2,0))], 2, 1) )
lWcells.append( WCell("jtlcclx3", [((-1,0),(1,-1)),((1,1),(0,-1)),((2,0),(0,1))], 2, 1) )
lWcells.append( WCell("jtlcclx4", [((1,-1),(-1,0)),((1,1),(0,-1)),((0,1),(2,0))], 2, 1) )
lWcells.append( WCell("jtlcclx5", [((-1,0),(0,-1)),((0,1),(2,0)),((1,1),(1,-1))], 2, 1) )
lWcells.append( WCell("jtlcclx6", [((-1,0),(0,-1)),((0,1),(2,0)),((1,-1),(1,1))], 2, 1) )
lWcells.append( WCell("jtlcclx7", [((-1,0),(0,-1)),((2,0),(0,1)),((1,1),(1,-1))], 2, 1) )
lWcells.append( WCell("jtlcclx8", [((-1,0),(0,-1)),((2,0),(0,1)),((1,-1),(1,1))], 2, 1) )
lWcells.append( WCell("jtlcclx9", [((0,-1),(-1,0)),((2,0),(0,1)),((1,1),(1,-1))], 2, 1) )
lWcells.append( WCell("jtlcclx10",[((0,-1),(-1,0)),((2,0),(0,1)),((1,-1),(1,1))], 2, 1) )
lWcells.append( WCell("jtlcclx11",[((0,-1),(-1,0)),((0,1),(2,0)),((1,1),(1,-1))], 2, 1) )
lWcells.append( WCell("jtlcclx12",[((0,-1),(-1,0)),((0,1),(2,0)),((1,-1),(1,1))], 2, 1) )

lWcells.append( WCell("jtlccr",    [((-1,0),(0,-1)),((1,0),(0,1))], 1, 1) )
lWcells.append( WCell("jtlccrla",  [((-1,0),(0,-1)),((2,0),(0,1))], 2, 1) )
lWcells.append( WCell("jtlccrlar", [((0,-1),(-1,0)),((0,1),(2,0))], 2, 1) )
lWcells.append( WCell("jtlccrls",  [((-1,0),(1,-1)),((2,0),(0,1))], 2, 1) )
lWcells.append( WCell("jtlccrlsr", [((1,-1),(-1,0)),((0,1),(2,0))], 2, 1) )

lWcells.append( WCell("jtlccx1",  [((1,-1),(-1,0)),((0,-1),(2,0))], 2, 1) )
lWcells.append( WCell("jtlccx2",  [((-1,0),(1,-1)),((2,0),(0,-1))], 2, 1) )
lWcells.append( WCell("jtlccx3",  [((-1,0),(1,-1)),((0,-1),(2,0))], 2, 1) )

lWcells.append( WCell("jtlcx1", [((-1,0),(1,-1)),((0,1),(0,-1))], 2, 1) )
lWcells.append( WCell("jtlcx2", [((-1,0),(1,-1)),((0,-1),(0,1))], 2, 1) )
lWcells.append( WCell("jtlcx3", [((1,-1),(-1,0)),((0,1),(0,-1))], 2, 1) )
lWcells.append( WCell("jtlcx4", [((1,-1),(-1,0)),((0,-1),(0,1))], 2, 1) )
lWcells.append( WCell("jtlcx5", [((-1,0),(1,-1)),((1,1),(0,-1))], 2, 1) )
lWcells.append( WCell("jtlcx6", [((-1,0),(1,-1)),((0,-1),(1,1))], 2, 1) )
lWcells.append( WCell("jtlcx7", [((1,-1),(-1,0)),((1,1),(0,-1))], 2, 1) )
lWcells.append( WCell("jtlcx8", [((1,-1),(-1,0)),((0,-1),(1,1))], 2, 1) )

lWcells.append( WCell("jtlcxcx1",[((-1,0),(0,2)),((-1,1),(1,2)),((2,1),(1,-1)),((2,0),(0,-1))], 2, 2) )
lWcells.append( WCell("jtllx1",  [((-1,0),(2,0)),((0,1),(1,-1))], 2, 1) )
lWcells.append( WCell("jtllx2",  [((-1,0),(2,0)),((1,1),(0,-1))], 2, 1) )
lWcells.append( WCell("jtlu",    [((-1,1),(-1,0))], 1, 2) )
lWcells.append( WCell("jtluc",   [((-1,1),(-1,0)),((0,2),(1,1))], 1, 2) )

lWcells.append( WCell("jtluc2",  [((-1,1),(-1,0)),((0,2),(1,0))], 1, 2) )
lWcells.append( WCell("jtluc2r", [((-1,1),(-1,0)),((1,0),(0,2))], 1, 2) )
lWcells.append( WCell("jtlucc1", [((-1,1),(-1,0)),((0,2),(1,1)),((0,-1),(1,0))], 1, 2) )
lWcells.append( WCell("jtlucc2", [((-1,1),(-1,0)),((1,1),(0,2)),((0,-1),(1,0))], 1, 2) )
lWcells.append( WCell("jtlucc3", [((-1,1),(-1,0)),((1,1),(0,2)),((1,0),(0,-1))], 1, 2) )
lWcells.append( WCell("jtlucc4", [((-1,1),(-1,0)),((0,2),(1,1)),((1,0),(0,-1))], 1, 2) )

lWcells.append( WCell("jtlucr",  [((-1,1),(-1,0)),((1,1),(0,2))], 1, 2) )
lWcells.append( WCell("jtlucx1", [((-1,1),(-1,0)),((0,2),(1,0)),((0,-1),(1,1))], 1, 2) )
lWcells.append( WCell("jtlucx2", [((-1,1),(-1,0)),((1,0),(0,2)),((0,-1),(1,1))], 1, 2) )
lWcells.append( WCell("jtlucx3", [((-1,1),(-1,0)),((1,0),(0,2)),((1,1),(0,-1))], 1, 2) )
lWcells.append( WCell("jtlucx4", [((-1,1),(-1,0)),((0,2),(1,0)),((1,1),(0,-1))], 1, 2) )

lWcells.append( WCell("jtlul",   [((-1,1),(-1,0)),((0,2),(0,-1))], 1, 2) )
lWcells.append( WCell("jtlulr",  [((-1,1),(-1,0)),((0,-1),(0,2))], 1, 2) )
lWcells.append( WCell("jtlurc",  [((-1,0),(-1,1)),((0,2),(1,1))], 1, 2) )
lWcells.append( WCell("jtlurc2", [((-1,0),(-1,1)),((0,2),(1,0))], 1, 2) )
lWcells.append( WCell("jtlurc2r",[((-1,0),(-1,1)),((1,0),(0,2))], 1, 2) )
lWcells.append( WCell("jtlurcr", [((-1,0),(-1,1)),((1,1),(0,2))], 1, 2) )
lWcells.append( WCell("jtluu",   [((-1,1),(-1,0)),((1,1),(1,0))], 1, 2) )
lWcells.append( WCell("jtluul1", [((-1,1),(-1,0)),((1,1),(1,0)),((0,-1),(0,2))], 1, 2) )
lWcells.append( WCell("jtluul2", [((-1,1),(-1,0)),((1,1),(1,0)),((0,2),(0,-1))], 1, 2) )
lWcells.append( WCell("jtluul3", [((-1,1),(-1,0)),((1,0),(1,1)),((0,2),(0,-1))], 1, 2) )
lWcells.append( WCell("jtluur",  [((-1,1),(-1,0)),((1,0),(1,1))], 1, 2) )

lWcells.append( WCell("jtlw1",[((-1,0),(2,0)),((-1,1),(2,1)),((0,2),(0,-1)),((1,2),(1,-1))], 2, 2) )
lWcells.append( WCell("jtlw2",[((-1,0),(2,0)),((-1,1),(2,1)),((0,2),(0,-1)),((1,-1),(1,2))], 2, 2) )
lWcells.append( WCell("jtlw4",[((2,0),(-1,0)),((-1,1),(1,2)),((0,2),(0,-1)),((1,-1),(1,2))], 2, 2) )
lWcells.append( WCell("jtlw5",[((2,0),(-1,0)),((-1,1),(1,2)),((0,-1),(0,2)),((1,2),(1,-1))], 2, 2) )

lWcells.append( WCell("jtlx",     [((-1,0),(1,0)),((0,1),(0,-1))], 1, 1) )
lWcells.append( WCell("jtlx2",    [((-1,0),(1,1)),((-1,1),(1,0))], 1, 2) )
lWcells.append( WCell("jtlx2r",   [((1,1),(-1,0)),((-1,1),(1,0))], 1, 2) )
lWcells.append( WCell("jtlx2rx",  [((1,1),(-1,0)),((-1,1),(1,0)),((0,2),(0,-1))], 1, 2) )
lWcells.append( WCell("jtlx2rxr", [((1,1),(-1,0)),((-1,1),(1,0)),((0,-1),(0,2))], 1, 2) )
lWcells.append( WCell("jtlx2x"  , [((-1,0),(1,1)),((-1,1),(1,0)),((0,2),(0,-1))], 1, 2) )

lWcells.append( WCell("jtlx3",    [((-1,0),(2,0)),((1,1),(1,-1))], 2, 1) )
lWcells.append( WCell("jtlx4",    [((-1,0),(2,0)),((0,1),(0,-1))], 2, 1) )
#lWcells.append( WCell("jtlx5",    [((-1,0),(2,0)),((0,-1),(0,2))], 2, 2) )
lWcells.append( WCell("jtlx5c",   [((-1,0),(2,0)),((0,-1),(0,2)),((1,2),(2,1))], 2, 2) )
#lWcells.append( WCell("jtlx6",    [((-1,0),(2,0)),((1,2),(1,-1))], 2, 2) )
lWcells.append( WCell("jtlx6c",   [((-1,0),(2,0)),((1,2),(1,-1)),((-1,1),(0,2))], 2, 2) )
#lWcells.append( WCell("jtlx7",    [((-1,0),(2,0)),((0,2),(0,-1))], 2, 2) )
lWcells.append( WCell("jtlx7c1",  [((-1,0),(2,0)),((0,2),(0,-1)),((1,2),(2,1))], 2, 2) )
lWcells.append( WCell("jtlx7c2",  [((-1,0),(2,0)),((0,2),(0,-1)),((2,1),(1,2))], 2, 2) )

lWcells.append( WCell("jtlxx1",[((-1,0),(2,0)),((0,1),(0,-1)),((1,1),(1,-1))], 2, 1) )
lWcells.append( WCell("jtlxx2",[((-1,0),(2,0)),((0,1),(0,-1)),((1,-1),(1,1))], 2, 1) )
lWcells.append( WCell("jtlxx3",[((-1,0),(2,0)),((0,-1),(0,2)),((1,-1),(1,2))], 2, 2) )
lWcells.append( WCell("jtlxx4",[((-1,1),(2,1)),((0,-1),(0,2)),((1,-1),(1,2))], 2, 2) )
lWcells.append( WCell("jtlxx5",[((-1,0),(2,0)),((0,-1),(0,2)),((1,2),(1,-1))], 2, 2) )
lWcells.append( WCell("jtlxx6",[((-1,1),(2,1)),((0,-1),(0,2)),((1,2),(1,-1))], 2, 2) )

lWcells.append( WCell("ljtl", [((-1,0),(2,0))], 2, 1) )

lWcells.append( WCell("spl3",     [((-1,0),(1,0)),((-1,0),(0,1)),((-1,0),(0,-1))], 1, 1) )
lWcells.append( WCell("spl3b",    [((-1,0),(2,0)),((-1,0),(0,1)),((-1,0),(0,-1))], 2, 1) )
lWcells.append( WCell("spl3bjtlx",[((-1,0),(2,0)),((-1,0),(0,1)),((-1,0),(0,-1)),((1,-1),(1,1))], 2, 1) )
lWcells.append( WCell("spl3c",    [((-1,0),(1,-1)),((-1,0),(0,1)),((-1,0),(0,-1))], 2, 1) )
lWcells.append( WCell("spl3d",    [((-1,0),(2,0)),((-1,0),(0,1)),((-1,0),(1,-1))], 2, 1) )
lWcells.append( WCell("spl3f",    [((-1,0),(1,0)),((-1,0),(1,1)),((-1,0),(1,-1))], 2, 1) )
lWcells.append( WCell("spl3fjtlx",[((-1,0),(1,0)),((-1,0),(1,1)),((-1,0),(1,-1)),((0,-1),(0,1))], 2, 1) )
lWcells.append( WCell("spl3g",    [((0,-1),(-1,0)),((0,-1),(0,1)),((0,-1),(2,0))], 2, 1) )
lWcells.append( WCell("spl3h",    [((0,-1),(-1,0)),((0,-1),(0,1)),((0,-1),(1,1))], 2, 1) )
lWcells.append( WCell("spl3i",    [((0,-1),(-1,0)),((0,-1),(0,1)),((0,-1),(1,-1))], 2, 1) )
lWcells.append( WCell("spl3j",    [((0,-1),(-1,0)),((0,-1),(1,1)),((0,-1),(2,0))], 2, 1) )
lWcells.append( WCell("spl3k",    [((-1,0),(0,1)),((-1,0),(1,1)),((-1,0),(2,0))], 2, 1) )
lWcells.append( WCell("spl3l",    [((0,-1),(-1,0)),((0,-1),(1,-1)),((0,-1),(2,0))], 2, 1) )
lWcells.append( WCell("spl3m",    [((0,-1),(0,1)),((0,-1),(1,1)),((0,-1),(2,0))], 2, 1) )
lWcells.append( WCell("spl3n",    [((-1,0),(0,1)),((-1,0),(1,1)),((-1,0),(1,-1))], 2, 1) )
lWcells.append( WCell("spl3o",    [((0,-1),(0,1)),((0,-1),(1,-1)),((0,-1),(2,0))], 2, 1) )
lWcells.append( WCell("spl3p",    [((0,-1),(1,1)),((0,-1),(1,-1)),((0,-1),(2,0))], 2, 1) )
lWcells.append( WCell("spl3q",    [((0,-1),(-1,0)),((0,-1),(1,1)),((0,-1),(1,-1))], 2, 1) )
lWcells.append( WCell("spl3q",    [((0,-1),(0,1)),((0,-1),(1,1)),((0,-1),(1,-1))], 2, 1) )


lWcells.append( WCell("spll",        [((-1,0),(1,0)),((-1,0),(0,1))], 1, 1) )
lWcells.append( WCell("spll2",       [((-1,0),(1,-1)),((-1,0),(2,0))], 2, 1) )
lWcells.append( WCell("spll2c1",     [((0,-1),(1,-1)),((0,-1),(2,0))], 2, 1) )
lWcells.append( WCell("spll2c2",     [((0,-1),(1,1)),((0,-1),(2,0))], 2, 1) )
lWcells.append( WCell("spll2c2jtlc", [((0,-1),(1,1)),((0,-1),(2,0)),((-1,0),(0,1))], 2, 1) )
lWcells.append( WCell("spll2jtl45x" ,[((-1,0),(1,-1)),((-1,0),(2,0)),((1,1),(0,-1))], 2, 1) )
lWcells.append( WCell("spll2jtl45xr",[((-1,0),(1,-1)),((-1,0),(2,0)),((0,-1),(1,1))], 2, 1) )
lWcells.append( WCell("spll3",       [((-1,0),(0,-1)),((-1,0),(2,0))], 2, 1) )
lWcells.append( WCell("spll3c1",     [((-1,0),(0,-1)),((-1,0),(1,1))], 2, 1) )
lWcells.append( WCell("spll3c1jtlc", [((-1,0),(0,-1)),((-1,0),(1,1)),((2,0),(1,-1))], 2, 1) )
lWcells.append( WCell("spll3c1jtlcr",[((-1,0),(0,-1)),((-1,0),(1,1)),((1,-1),(2,0))], 2, 1) )
lWcells.append( WCell("spll3c2",     [((-1,0),(0,-1)),((-1,0),(1,-1))], 2, 1) )
lWcells.append( WCell("spll3jtl45x", [((-1,0),(0,-1)),((-1,0),(2,0)),((0,1),(1,-1))], 2, 1) )
lWcells.append( WCell("spll3jtl45xr",[((-1,0),(0,-1)),((-1,0),(2,0)),((1,-1),(0,1))], 2, 1) )

lWcells.append( WCell("spll4",       [((-1,0),(1,0)),((-1,0),(0,2))], 1, 2) )
lWcells.append( WCell("spll4c1",     [((-1,0),(1,1)),((-1,0),(1,0))], 1, 2) )
lWcells.append( WCell("spll4c1jtlx", [((-1,0),(1,1)),((-1,0),(1,0)),((0,2),(0,-1))], 1, 2) )
lWcells.append( WCell("spll4c1jtlxr",[((-1,0),(1,1)),((-1,0),(1,0)),((0,-1),(0,2))], 1, 2) )
lWcells.append( WCell("spll4c2",     [((-1,0),(0,1)),((-1,0),(1,0))], 1, 2) )
lWcells.append( WCell("splljtlx",    [((-1,0),(1,-1)),((-1,0),(2,0)),((0,-1),(0,1))], 2, 1) )
lWcells.append( WCell("splljtlx2",   [((-1,0),(1,-1)),((-1,0),(2,0)),((0,1),(0,-1))], 2, 1) )
lWcells.append( WCell("splljtlx3",   [((-1,0),(0,-1)),((-1,0),(2,0)),((0,-1),(0,1))], 2, 1) )
lWcells.append( WCell("splljtlx4",   [((-1,0),(0,-1)),((-1,0),(2,0)),((1,1),(1,-1))], 2, 1) )
lWcells.append( WCell("splljtlx5",   [((0,1),(0,-1)),((0,1),(2,0)),((1,-1),(1,1))], 2, 1) )
lWcells.append( WCell("splljtlx6",   [((0,1),(0,-1)),((0,1),(2,0)),((1,1),(1,-1))], 2, 1) )

lWcells.append( WCell("splt",        [((-1,0),(0,1)),((-1,0),(0,-1))], 1, 1) )
lWcells.append( WCell("splt2",       [((-1,0),(1,1)),((-1,0),(1,-1))], 2, 1) )
lWcells.append( WCell("splt3",       [((-1,0),(0,2)),((-1,0),(0,-1))], 1, 2) )
lWcells.append( WCell("splt3c1",     [((-1,0),(-1,1)),((-1,0),(0,-1))], 1, 2) )
lWcells.append( WCell("splt3c2",     [((-1,0),(0,-1)),((-1,0),(1,1))], 1, 2) )
lWcells.append( WCell("spltc1",      [((0,-1),(1,1)),((0,-1),(1,-1))], 1, 2) )
lWcells.append( WCell("spltjtlx",    [((-1,0),(1,1)),((-1,0),(1,-1)),((0,1),(0,-1))], 2, 1) )
lWcells.append( WCell("spltjtlx2",   [((1,-1),(-1,0)),((1,-1),(2,0)),((0,-1),(0,1))], 2, 1) )
lWcells.append( WCell("spltjtlx3",   [((1,-1),(-1,0)),((1,-1),(2,0)),((0,1),(0,-1))], 2, 1) )

lWcells.append( WCell("splw1",       [((-1,1),(0,-1)),((-1,1),(2,1)),((2,0),(-1,0)),((2,0),(1,2))], 2, 2) )
lWcells.append( WCell("splw2",       [((-1,1),(0,-1)),((-1,1),(2,1)),((1,-1),(-1,0)),((1,-1),(1,2))], 2, 2) )
lWcells.append( WCell("splw3",       [((0,-1),(0,2)),((0,-1),(2,0)),((-1,1),(2,1)),((-1,1),(1,-1))], 2, 2) )
lWcells.append( WCell("splw4",       [((-1,0),(0,2)),((-1,0),(2,0)),((-1,1),(2,1)),((-1,1),(1,-1))], 2, 2) )


param = sys.argv

if len(param) >= 2 :
    lWire, lWireSet = loadWireFromFile( param[1] )
else:
    print("Please specify a routing file")
    sys.exit(1)

print(lWire)
print(lWireSet)
max_x = 0
max_y = 0
for w in lWire:
    for c in w.lCorner:
        max_x = max(max_x, c[0])
        max_y = max(max_y, c[1])

for y in range(max_y,-1,-1):
    print( str(y)+": ", end='')
    for x in range(max_x+1):
        isOccupied = False
        for w in lWire:
            if w.getDirectionOnPoint(x,y) != 0:
                isOccupied = True
                break
        if isOccupied:
            print("x", end='')
        else:
            print("-", end='')
    print("")

grid = Grid(max_x+1,max_y+1)
grid.set(2,3, Grid.GRID_IN_USE)
grid.print()

grid2 = Grid(max_x+1,max_y+1)
grid2.set_emptylist()

for wc in lWcells:
    wc.mark_placeable_possition(grid2, lWireSet)

grid2.print()
print("Placed : {}".format(grid2.isWirePlaced( lWireSet )))

print("======== CUT HERE ========")
print(grid2.genILP( lWire, lWireSet ))

