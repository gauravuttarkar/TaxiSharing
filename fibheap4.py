
class Node:
    def __init__(self,i):
        self.distance=99999
        #self.color=0
        self.pred=None
        self.num=i
        self.adj=[]
        self.parent = None
        self.children = None
        self.leftSibling = None
        self.rightSibling = None
        self.pred = None
        self.rank = 0

    def addChild(self,node):
        if self.children!=None:
            self.children.addSibling(node)  #Addsibling

        else:
            self.children=node
            node.parent=self
            self.rank=1

        return True

    def addSibling(self,node):
        temp=self.rightMostSibling()
        if (temp==None):
            return False
        temp.rightSibling=node
        node.leftSibling=temp
        node.parent=self.parent
        node.rightSibling=None

        if(self.parent!=None):

            self.parent.rank=self.parent.rank+1
        return True


    def remove(self):
        if self.parent!=None:
            self.parent.rank=self.parent.rank-1
            if (self.leftSibling!=None):
                self.parent.children=self.leftSibling
            elif (self.rightSibling!=None):
                self.parent.children=self.rightSibling
            else:
                self.parent.children=None
        if(self.leftSibling!=None):
            self.leftSibling.rightSibling =self.rightSibling
        if(self.rightSibling!=None):
            self.rightSibling.leftSibling =self.leftSibling

        self.leftSibling = None
        self.rightSibling = None
        self.parent = None
        return True

    def  leftMostSibling(self):
        if self==None:
            return None
        temp=self
        while temp.leftSibling!=None:
            temp=temp.leftSibling
        return temp 
  
    def rightMostSibling(self):
        if self==None:
            return None
        temp=self
        while temp.rightSibling!=None:
            temp=temp.rightSibling
        return temp 


class FibonacciHeap:
    def __init__(self,root=None):
        self.rootListByRank=[None]*100
        self.minRoot=root
        self.minRoot.parent=None
        self.minRoot.children=None
        self.minRoot.leftSibling=None
        self.minRoot.rightSibling=None
        self.minRoot.rank=0


    def isEmpty(self):
        return (self.minRoot==None)


    def insertVertex(self,node):
        if(node==None):
            return False
        if(self.minRoot==None):
            self.minRoot=node
        else:
            self.minRoot.addSibling(node)
            if(self.minRoot.distance > node.distance):
                self.minRoot=node
        return True

    def findMin(self):
        return self.minRoot




    def deleteMin(self):
        try:
            temp= self.minRoot.children.leftMostSibling()
        except:
            temp=None

        nextTemp=None

        while(temp!=None):
            nextTemp=temp.rightSibling
            temp.remove()
            self.minRoot.addSibling(temp)
            temp=nextTemp
        temp=self.minRoot.leftMostSibling()

        if (temp==self.minRoot):
            if (self.minRoot.rightSibling):
                temp=self.minRoot.rightSibling
            else:
                out=self.minRoot
                self.minRoot.remove()
                self.minRoot=None
                return out

        out = self.minRoot
        self.minRoot.remove()
        self.minRoot = temp
        for i in range(0, 100):
           self.rootListByRank[i] = None

        while (temp):
            if temp.distance < self.minRoot.distance:
                self.minRoot = temp
            nextTemp = temp.rightSibling;
            self.link(temp)
            temp = nextTemp
        return out

    def link(self, root):
            if self.rootListByRank[root.rank] == None:
                self.rootListByRank[root.rank] = root
                return False
            else:
                linkVertex = self.rootListByRank[root.rank]
                self.rootListByRank[root.rank] = None
                if root.distance < linkVertex.distance or root == self.minRoot:
                    linkVertex.remove()
                    root.addChild(linkVertex)
                    if self.rootListByRank[root.rank] != None:
                        self.link(root)
                    else:
                        self.rootListByRank[root.rank] = root
                else:
                    root.remove()
                    linkVertex.addChild(root)
                    if self.rootListByRank[linkVertex.rank] != None:
                        self.link(linkVertex)
                    else:
                        self.rootListByRank[linkVertex.rank] = linkVertex
                return True

    def decreaseKey(self, delta, vertex):
            vertex.distance = delta
            if vertex.parent!=None and vertex.parent.distance<=vertex.distance:
                return
            if vertex.parent != None:
                vertex.remove()
                self.minRoot.addSibling(vertex)
            if vertex.distance < self.minRoot.distance:
                self.minRoot = vertex





"""
n=Node(0)
n.distance=6
n1=Node(1)
n1.distance=9
n2=Node(2)
n2.distance=4
n3=Node(3)
n3.distance=-8
n4=Node(4)
n4.distance=0

H=FibonacciHeap(n)
H.insertVertex(n1)
H.insertVertex(n2)
H.insertVertex(n3)
H.insertVertex(n4)
#H.insertVertex(n1)
H.decreaseKey(5,n2)

print(H.deleteMin().distance)
print(H.deleteMin().distance)
print(H.deleteMin().distance)
print(H.deleteMin().distance)
print(H.deleteMin().distance)

print(n2.distance)
print(H.isEmpty())"""