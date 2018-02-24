from fibheap4 import *


TaxiStands_list=[]
nodes = []
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[-1]


class TaxiStand:
    def __init__(self,n,file):
        self.q=Queue()
        for i in range(n):
            #model = input('Enter model\n')
            model=file.readline()
            #taxi_number = input('Enter taxi number\n')
            taxi_number=file.readline()
            #price = int(input('Enter price\n'))
            price=int(file.readline())
            self.q.enqueue(Taxi(model,taxi_number,price))

    def TaxiPeek(self):
        if (self.q.size()<=0):

            return None
        else:
            return self.q.peek()


    def TaxiLeaves(self):
        if (self.q.size()<=0):
            #print('No taxi available')
            return None
        return self.q.dequeue()

    def neighbhourhood(self,source):
            print("Getting taxi from neighbouring stand")
            nodes_copy=nodes[:]
            Dijikstra1(nodes_copy,source)
            currentTaxi=None
            insertionSort(nodes_copy)
            i=1
            while currentTaxi==None:
                currentTaxi=TaxiStands_list[nodes_copy[i].num].TaxiLeaves()
                i=i+1
            self.TaxiArrives(currentTaxi)

    def neighbhourhood_peek(self,source):
            #print("Getting taxi from neighbouring stand")
            nodes_copy=nodes[:]
            Dijikstra1(nodes_copy,source)
            currentTaxi=None
            insertionSort(nodes_copy)
            i=1
            while currentTaxi==None:
                currentTaxi=TaxiStands_list[nodes_copy[i].num].TaxiPeek()
                i=i+1
            #self.TaxiArrives(currentTaxi)
            return currentTaxi
    def TaxiArrives(self,taxi):
        self.q.enqueue(taxi)

class Taxi:
    def __init__(self,model,number,price):
        self.model=model
        self.number=number
        self.price=price


def Dijikstra(nodes_list, source, dest):
    for i in nodes_list:
        i.distance = 999999
        i.pred = None
    H = FibonacciHeap(nodes_list[0])

    for i in nodes_list[1:]:
        H.insertVertex(i)

    nodes_list[source].distance = 0
    H.decreaseKey(0, nodes_list[source])


    while not H.isEmpty():
        u = H.deleteMin()
        for i in u.adj:
            if nodes_list[i[0]].distance > i[1] + u.distance:
                H.decreaseKey(i[1] + u.distance, nodes_list[i[0]])
                nodes_list[i[0]].pred = u
    i = nodes_list[dest]

    return i

def insertionSort(alist):
   for index in range(1,len(alist)):
     current=alist[index]
     currentvalue = alist[index].distance
     position = index

     while position>0 and alist[position-1].distance>currentvalue:
         alist[position]=alist[position-1]
         position = position-1

     alist[position]=current

def Dijikstra1(nodes_list, source):
    for i in nodes_list:
        i.distance = 999999
        i.pred = None
    H = FibonacciHeap(nodes_list[0])

    for i in nodes_list[1:]:
       # nodes_fibheap[i.num] = Node(i, i.distance)
        H.insertVertex(i)

    nodes_list[source].distance = 0
    H.decreaseKey(0, nodes_list[source])


    while not H.isEmpty():
        u = H.deleteMin()
        for i in u.adj:
            if nodes_list[i[0]].distance > i[1] + u.distance:
                # print(nodes_fibheap[i[0]])
                H.decreaseKey(i[1] + u.distance, nodes_list[i[0]])
                #nodes_list[i[0]].distance = i[1] + u.key
                nodes_list[i[0]].pred = u

def taxi_alloc(source,dest):
    global nodes
    global TaxiStands_list
    currentTaxi = TaxiStands_list[source].TaxiLeaves()
    if currentTaxi==None:
                TaxiStands_list[source].neighbhourhood(source)
                currentTaxi = TaxiStands_list[source].TaxiLeaves()
    destination_node = Dijikstra(nodes, source, dest)
    TaxiStands_list[dest].TaxiArrives(currentTaxi)
    
    path_list=[]
    i = TaxiStands_list[dest]
    while destination_node:
        path_list.append(destination_node.num)
        destination_node = destination_node.pred
    path_list.reverse()
    print("path is :")
    path(path_list)
    print('Your Taxi details is')
    print('Model', currentTaxi.model, end="")
    print('Number', currentTaxi.number, end="")
    print('Price', currentTaxi.price)
    print("The total price is", nodes[dest].distance * currentTaxi.price)



def TaxiStandsInput():
    global nodes
    global TaxiStands_list
    f=open("file3.txt","r")
    n=int(f.readline())
    for i in range(n):
        nodes.append(Node(i))

    for i in range(n):
        numberOftaxi=int(f.readline())
        TaxiStands_list.append(TaxiStand(numberOftaxi,f))
    e=int(f.readline())

    for i in range(e):
        li = f.readline().split()
        li = [int(i) for i in li]
        nodes[li[0]].adj.append((li[1], li[2]))
        nodes[li[1]].adj.append((li[0], li[2]))

def path(path_list):
	i=0
	k=len(path_list)
	while i<k-1:
		print(path_list[i],"->",end=" ")
		i=i+1
	print(path_list[i])

def sharing():

        print('Enter Source of User 1')
        s1=int(input())
        print('Enter Destination of User 1')
        d1 = int(input())
        print('Enter Source of User 2')
        s2 = int(input())
        print('Enter Destination of User 2')
        d2 = int(input())
        s1_distance=9999999
        Dijikstra1(nodes,s1)
        if nodes[s2].distance<nodes[d1].distance:
            path_list1=[]
            temp=nodes[s2]
            s1_distance1=temp.distance
            sharingdistance=0
            while temp:
                path_list1.append(temp.num)
                temp=temp.pred
            path_list1.reverse()

            Dijikstra1(nodes,s2)
            if nodes[d1].distance < nodes[d2].distance:
                s1_dest=d2
                temp = nodes[d1]
                s1_distance1 = s1_distance1+temp.distance
                s1_distance2=temp.distance
                sharingdistance=temp.distance
                path_list1.pop()
                templist=[]
                while temp:
                    templist.append(temp.num)
                    temp = temp.pred
                templist.reverse()
                path_list1.extend(templist)

                #user1_distance=distance
                Dijikstra(nodes,d1,d2)
                temp = nodes[d2]
                s1_distance2 = s1_distance2+temp.distance
                templist=[]
                path_list1.pop()
                while temp:
                    templist.append(temp.num)
                    temp = temp.pred
                templist.reverse()
                path_list1.extend(templist)

            elif nodes[d2].distance <= nodes[d1].distance:
                s1_dest=d1
                temp = nodes[d2]
                s1_distance1 = s1_distance1+temp.distance
                s1_distance2=temp.distance
                sharingdistance=temp.distance
                #print(sharingdistance)
                path_list1.pop()
                templist=[]
                while temp:
                    templist.append(temp.num)
                    temp = temp.pred
                templist.reverse()
                path_list1.extend(templist)

                #user1_distance=distance
                Dijikstra(nodes,d2,d1)
                temp = nodes[d1]
                s1_distance1 = s1_distance1+temp.distance
                templist=[]
                path_list1.pop()
                while temp:
                    templist.append(temp.num)
                    temp = temp.pred
                templist.reverse()
                path_list1.extend(templist)


            s1_distance=s1_distance1+s1_distance2-sharingdistance
            sharingdistance1=sharingdistance
        else:
            flag=1

        Dijikstra1(nodes,s2)
        s2_distance=9999999
        if nodes[s1].distance<nodes[d2].distance:
            path_list2=[]
            temp=nodes[s1]
            s2_distance2=temp.distance
            sharingdistance=0
            while temp:
                path_list2.append(temp.num)
                temp=temp.pred
            path_list2.reverse()

            Dijikstra1(nodes,s1)
            if nodes[d1].distance < nodes[d2].distance:
                s2_dest=d2
                temp = nodes[d1]
                s2_distance2 = s2_distance2+temp.distance
                s2_distance1=temp.distance
                sharingdistance=temp.distance
                path_list2.pop()
                templist=[]
                while temp:
                    templist.append(temp.num)
                    temp = temp.pred
                templist.reverse()
                path_list2.extend(templist)

                #user1_distance=distance
                Dijikstra(nodes,d1,d2)
                temp = nodes[d2]
                s2_distance2 = s2_distance2+temp.distance
                templist=[]
                path_list2.pop()
                while temp:
                    templist.append(temp.num)
                    temp = temp.pred
                templist.reverse()
                path_list2.extend(templist)
            elif nodes[d2].distance <= nodes[d1].distance:
                s2_dest=d1
                temp = nodes[d2]
                s2_distance2 = s2_distance2+temp.distance
                s2_distance1=temp.distance
                sharingdistance=temp.distance
                path_list2.pop()
                templist=[]
                while temp:
                    templist.append(temp.num)
                    temp = temp.pred
                templist.reverse()
                path_list2.extend(templist)

                #user1_distance=distance
                Dijikstra(nodes,d2,d1)
                temp = nodes[d1]
                s2_distance1 = s2_distance1+temp.distance
                templist=[]
                path_list2.pop()
                while temp:
                    templist.append(temp.num)
                    temp = temp.pred
                templist.reverse()
                path_list2.extend(templist)

            s2_distance = s2_distance1 + s2_distance2 - sharingdistance
        else:
            try:
                flag=flag+1
            except:
                flag=1
            if flag==2:
                print("")
                taxi_alloc(s1,d1)
                taxi_alloc(s2,d2)
                return


        #TaxiStands_list[d2].TaxiArrives(currentTaxi)
        if s1_distance>s2_distance:
            currentTaxi = TaxiStands_list[s2].TaxiPeek()
            flag=0
            if currentTaxi==None:
                currentTaxi=TaxiStands_list[s2].neighbhourhood_peek(s2)
                flag=1

            #print(currentTaxi.model)
            price1=s2_distance1 * currentTaxi.price - sharingdistance * currentTaxi.price // 2
            price2=s2_distance2*currentTaxi.price-sharingdistance*currentTaxi.price//2

            if Dijikstra(nodes,s1,d1).distance*currentTaxi.price<price1:
                #TaxiStands_list[s2].TaxiArrives(currentTaxi)
                taxi_alloc(s1,d1)
                taxi_alloc(s2,d2)
                #print('hi')
                return
            elif Dijikstra(nodes,s2,d2).distance*currentTaxi.price<price2:
                #TaxiStands_list[s2].TaxiArrives(currentTaxi)
                taxi_alloc(s1,d1)
                taxi_alloc(s2,d2)
                #print('hi1')
                return


            if currentTaxi==None or flag==1:
                flag=0
                TaxiStands_list[s2].neighbhourhood(s2)

            currentTaxi = TaxiStands_list[s2].TaxiLeaves()
            TaxiStands_list[s2_dest].TaxiArrives(currentTaxi)
            print('The path : ',end=" ")
            path(path_list2)
            print('Your Taxi details is')
            print('Model', currentTaxi.model, end="")
            print('Number', currentTaxi.number, end="")
            print('Price', currentTaxi.price)
            print('Price of user 1 is ',s2_distance1*currentTaxi.price - sharingdistance*currentTaxi.price//2)
            print('Price of user 2 is ',s2_distance2*currentTaxi.price-sharingdistance*currentTaxi.price//2)


        else:
            currentTaxi = TaxiStands_list[s1].TaxiPeek()
            flag=0
            if currentTaxi==None:
                currentTaxi=TaxiStands_list[s1].neighbhourhood_peek(s1)
                flag=1

            price1=s1_distance1 * currentTaxi.price - sharingdistance1 * currentTaxi.price // 2
            price2=s1_distance2*currentTaxi.price-sharingdistance1*currentTaxi.price//2

            if Dijikstra(nodes,s1,d1).distance*currentTaxi.price<price1:
                #TaxiStands_list[s1].TaxiArrives(currentTaxi)
                taxi_alloc(s1,d1)
                taxi_alloc(s2,d2)
                #print('hi12')
                return
            elif Dijikstra(nodes,s2,d2).distance*currentTaxi.price<price2:
                #TaxiStands_list[s1].TaxiArrives(currentTaxi)
                taxi_alloc(s1,d1)
                taxi_alloc(s2,d2)
                #print('hi3')
                return
            if currentTaxi==None or flag==1:
                flag=0
                TaxiStands_list[s1].neighbhourhood(s1)

            #TaxiStands_list[s1_dest].TaxiArrives(currentTaxi)
            currentTaxi = TaxiStands_list[s1].TaxiLeaves()
            TaxiStands_list[s1_dest].TaxiArrives(currentTaxi)

            print('The path is : ',end=" ")
            path(path_list1)
            print('Your Taxi details is')
            print('Model', currentTaxi.model, end="")
            print('Number', currentTaxi.number, end="")
            print('Price', currentTaxi.price)
            #print("distance1",s1_distance1,s1_distance2,sharingdistance1)
            print('Price of user 1 is ', s1_distance1 * currentTaxi.price-sharingdistance1*currentTaxi.price//2)
            print('Price of user 2 is ', s1_distance2 * currentTaxi.price-sharingdistance1*currentTaxi.price//2)



def taxi():

        source = int(input("Enter the source\n"))
        dest = int(input("Enter the destination\n"))

        taxi_alloc(source,dest)


def main():
    y='y'
    TaxiStandsInput()
    while y=='y':
        print("Choose appropiate option:\n1 -> Personal Cab \n2 -> Sharing Cab ")
        users=int(input())
        if users==1:
            taxi()
        elif users==2:
            sharing()
        else:
            print("There are currently no more than 2 users in your surrounding")
        print("Do you want to use again")
        y=input()

main()
#print(Dijikstra(nodes,14,4).distance)

#print detail function
#brute force for any source vertex