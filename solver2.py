from math import sqrt, pow

class analyseMaze():
        def __init__(self, node, end):
            self.node = node
            self.end = end

        def calculateHeuristics(self):
            return sqrt(pow((self.end[0]-self.node[0]), 2) + pow((self.end[1]-self.node[1]), 2)) 

        def neighbourAnalyser(self):
            neighbours = []
            if not self.node[0]-1 < 0:    # mkch f 7it fou9ani belkol
                if maze[self.node[0]-1][self.node[1]] == '0' or \
                maze[self.node[0]-1][self.node[1]] in locator.keys():  # if eli fou9ek :    ="0"  |  =  door , key ...
                    neighbours.append([self.node[0]-1, self.node[1], self.node[2]+1])  # appendi lel neighbours : [ligne eli fou9ou , meme colonne , cout + 1 ]
                    
            if not self.node[0]+1 > maze_dim[0]: # mkch f 7it loutani belkol
                if maze[self.node[0]+1][self.node[1]] == '0' or \
                maze[self.node[0]+1][self.node[1]] in locator.keys():# if eli ta7tek :    ="0"  |  =  door , key ...
                    neighbours.append([self.node[0]+1, self.node[1], self.node[2]+1])  # appendi lel neighbours : [ligne eli ta7tou , meme colonne , cout + 1 
                    
            if not self.node[1]-1 < 0:  # mkch f 7it eli 3a lissar belkol
                if maze[self.node[0]][self.node[1]-1] == '0' or \
                maze[self.node[0]][self.node[1]-1] in locator.keys():# if eli bjanbek 3alisar :    ="0"  |  =  door , key ...
                    neighbours.append([self.node[0], self.node[1]-1, self.node[2]+1])  # appendi lel neighbours : [meme ligne , colonne eli fou9ou , cout + 1 ]
                    
            if not self.node[1]+1 > maze_dim[1]: # mkch f 7it eli 3a limin belkol
                if maze[self.node[0]][self.node[1]+1] == '0' or \
                maze[self.node[0]][self.node[1]+1] in locator.keys():# if eli bjanbek 3alimin :    ="0"  |  =  door , key ...
                    neighbours.append([self.node[0], self.node[1]+1, self.node[2]+1])  # appendi lel neighbours : [meme ligne , colonne eli ta7tou , cout + 1 ]
            return neighbours




def pathFinder(start,end):
        obj = analyseMaze(start, end)  # start = [ x , y , cout ]  / end = [ x , y ]
        unvisitedNodes = [[obj, 0, [start[:2].copy()]]]   # unvisitedNodes = [  [  (start , end) ,  0  ,  [x,y]  ] , ]
        visitedNodes = []
        nodeHistory = []
        nodeHistory.append(start[:2])    #  [ start ]
        pathFound = False
        i = 0
        while not pathFound:
            f = []
            newNodes = []
            for node in unvisitedNodes:
                #print('----node : ' , node)
                f.append([node, node[1] + node[0].calculateHeuristics()])  #  f =  [ [ '[(start , end),0,[x,y]]' , cout +h ]   ,  ] 
                if node[0].calculateHeuristics() == 0:
                    # print(node[2])
                    return node
            f.sort(key=lambda x: x[1])  # sort selon el cout + h
            neighbours = f[0][0][0].neighbourAnalyser()  #  (start , end).neighbourAnalyser()  -> tatik neighbours 
            parent = f[0][0][2].copy()  #  [x , y] mt3 eli 9balha

            selected_node = unvisitedNodes.index(f[0][0])  #  '[(start , end),0,[x,y]]'  : index mt3 node loula fi f , fi west el unvisitedNodes
            visitedNodes.append(unvisitedNodes[selected_node])  #  ne5dhou el  node edhika ( loula f f ) eli heya tete mt3 OUVERT 
            del unvisitedNodes[selected_node]  #  nfas5oha node edhika men OUvert  
            
            for n in neighbours:
                cObj = analyseMaze(n, end)  # n = [ x , y , cout ]  / end = [ x , y ]
                parent = f[0][0][2].copy() #  [x , y] mt3 eli 9balha
                child = []
                child.extend(parent)  # n7otou parent (eli 9balha) fi e5er child 
                child.append(n[:2])  # append [ x , y ] mt3 neighbors 'n'
                if not n[:2] in nodeHistory: 
                    nodeHistory.append(n[:2])
                    newNodes.append([cObj, n[2], child])
            unvisitedNodes.extend(newNodes)

            # i += 1
            # if i > 36:
            #     break
            if not len(unvisitedNodes):
                break  
            

def getPath():
    start_point = locator['s'].copy()  # start_point  = [1, 1]
    start_point.append(0) # start_point  = [1, 1 , 0]
    end_point = locator['e'].copy()  # end_point = [5 , 16]
    path = pathFinder(start_point, end_point)
    return  path[2]


def getMaze(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()

    global locator
    locator = {}
    
    global ghost_locator
    ghost_locator = []
    
    global door_key
    door_key = {'b':'a', 'd':'c', 'g':'f', 'h':'i'}
    
    global maze
    maze = []
    
    global maze_dim
    maze_dim = [len(data), 0]
    
    for i in range(maze_dim[0]):
        line = data[i].split()
        maze.append(line)
        maze_dim[1] = len(line)
        for j in range(maze_dim[1]):
            if line[j].isalpha():
                locator[line[j]] = [i, j]
            if line[j].isnumeric() and int(line[j]) > 1:
                ghost_locator.append([i, j, int(line[j])])
    
    print(' -------------------------- GHOST LOCATOR -------------------------- :')
    print(ghost_locator)
    print(' ------------------')

    for ghost in ghost_locator:
        for i in range(1,ghost[2]):
            if ghost[1]+i < maze_dim[1] and maze[ghost[0]][ghost[1]+i] == '0':
                maze[ghost[0]][ghost[1]+i] = '-1'
            elif ghost[1]+i < maze_dim[1] and maze[ghost[0]][ghost[1]+i] == '1':
                break
            elif ghost[1]-i >= 0 and maze[ghost[0]][ghost[1]-i] == '0':
                maze[ghost[0]][ghost[1]-i] = '-1'
            elif ghost[1]-i >= 0 and maze[ghost[0]][ghost[1]-i] == '1':
                break
            elif ghost[0]+i < maze_dim[0] and maze[ghost[0]+i][ghost[1]] == '0':
                maze[ghost[0]+i][ghost[1]] = '-1'
            elif ghost[0]+i < maze_dim[0] and maze[ghost[0]+i][ghost[1]] == '1':
                break
            elif ghost[0]-i >= 0 and maze[ghost[0]-i][ghost[1]] == '0':
                maze[ghost[0]-i][ghost[1]] = '-1'
            elif ghost[0]-i >= 0 and maze[ghost[0]-i][ghost[1]] == '1':
                break
    return maze

if __name__ == '__main__':
    getMaze()
    getPath()











