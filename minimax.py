def ParseTextFile(fileName):
    f = open(fileName)
    txt = f.read()

    elements = txt.split(',')

    elements[0] = elements[0][1:]
    elements[-1] = elements[-1][:-1]

    for i in range(0,len(elements)):
        elements[i] = int(elements[i])

    return elements


class Tree:
    def __init__(this,root,parent,children,processedNodeCount):
        this.root = root
        this.children = children
        this.parent = parent
        this.processedNodeCount = processedNodeCount


    def IncrementAllParentsProcessedNodeCount(this):
        if(this.parent != None):
            this.parent.processedNodeCount += 1
            this.parent.IncrementAllParentsProcessedNodeCount()


    def CreateChildren(this):
        for i in range(0,len(this.root.game)):
            counter = 0
            while(counter < this.root.game[i]):
                childNode = this.root.DeepCopyNode()
                child = Tree(childNode,this,[],0)
                child.root.game[i] = counter
                this.children.append(child)    
                counter += 1


    def GetCalculatedSiblingValues(this):
        result = []
        if(this.parent == None):
            return result

        for i in this.parent.children:
            val = i.root.value
            if(val != -2):
                result.append(val)

        return result

    

    def OneExistInSiblings(this):
        vals = this.GetCalculatedSiblingValues()
        for i in vals:
            if(i == 1):
                return True

        return False


    def MinusOneExistInSiblings(this):
        vals = this.GetCalculatedSiblingValues()
        for i in vals:
            if(i == -1):
                return True

        return False
    


class Node:
    def __init__(this,game,value,move):
        this.game = game
        this.value = value
        this.move = move



    def DeepCopyNode(this):
        result = Node([],this.value,None)
        for i in this.game:
            result.game.append(i)

            
        return result




def Minimax(tree,player_type):
    
    tree.IncrementAllParentsProcessedNodeCount()
    tree.CreateChildren()

    if(len(tree.children) == 0):
        if(player_type == "MAX"):
            tree.root.value = 1
            return tree
        else:
            tree.root.value = -1
            return tree

    if(player_type == "MAX"):

        tree.root.value = -1
        
        for i in tree.children:
            
            i.root.value = (Minimax(i,"MIN")).root.value
   
        for i in tree.children:
            
            if(i.root.value == 1):
                tree.root.value = 1
                tree.root.move = i
                break

    else:
        tree.root.value = 1
        
        for i in tree.children:
            i.root.value = Minimax(i,"MAX").root.value

        for i in tree.children:
            if(i.root.value == -1):
                tree.root.value = -1
                tree.root.move = i
                break
        
    return tree
    




def AlphaBeta(tree,player_type,alpha,beta):
    
    if(player_type == "MIN" and alpha == 1):
        tree.root.value = -1
        return tree

    if(player_type == "MAX" and beta == -1):
        tree.root.value = 1
        return tree

    tree.IncrementAllParentsProcessedNodeCount()
    tree.CreateChildren()

    if(len(tree.children) == 0):
        if(player_type == "MAX"):
            tree.root.value = 1
            return tree
        else:
            tree.root.value = -1
            return tree

    if(player_type == "MAX"):

        tree.root.value = -1

        for i in tree.children:
            i.root.value = (AlphaBeta(i,"MIN",alpha,beta)).root.value
            if(i.root.value == 1):
                alpha = 1
   
        for i in tree.children:
            if(i.root.value == 1):
                tree.root.value = 1
                tree.root.move = i
                alpha = 1
                break

    else:
        tree.root.value = 1
        
        for i in tree.children:
            i.root.value = AlphaBeta(i,"MAX",alpha,beta).root.value
            if(i.root.value == -1):
                beta = -1

        for i in tree.children:
            if(i.root.value == -1):
                tree.root.value = -1
                tree.root.move = i
                break
        
    return tree



def SolveGame(method_name,problem_file_name,player_type) :

    game = ParseTextFile(problem_file_name)
    rootNode = Node(game,-2,None)
    tree = Tree(rootNode,None,[],0)
    
    if(method_name == "Minimax"):
        resultTree = Minimax(tree,player_type)
        return [resultTree.root.move.root.game,resultTree.root.move.processedNodeCount]
    elif(method_name == "AlphaBeta"):
        resultTree = AlphaBeta(tree,player_type,-1,1)
        return [resultTree.root.move.root.game,resultTree.root.move.processedNodeCount]
    else:
        return None


