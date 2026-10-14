class Node():
    def __init__(self,data):
        self.data = data
        self.parent = None
        self.leftChild = None
        self.rightChild = None
        self.height = -1

    def setLeftChild(self,leftChild):
        self.leftChild=leftChild

    def setRightChild(self,rightChild):
        self.rightChild=rightChild

    def setParent(self,parent):
        self.parent=parent

    def setData(self,data): # update data
        self.data=data

    def setHeight(self,height):
        self.height=height

    def getData(self):
        return self.data

    def getLeftChild(self):
        return self.leftChild

    def getRightChild(self):
        return self.rightChild

    def getParent(self):
        return self.parent




class BinarySearchTree():

    def __init__(self):
        self.root = None
        self.size = 0

    def getRoot(self):
        return self.root

    def insertNode(self, data):
        tempNode = self.root

        newNode = Node(data)
        if(tempNode == None):
            self.root = newNode

        else:
            while(True):
                if(data < tempNode.getData()):
                    if(tempNode.getLeftChild() == None):
                        tempNode.setLeftChild(newNode)
                        tempNode.getLeftChild().setParent(tempNode)
                        break
                    else:
                        tempNode = tempNode.getLeftChild()
                else:
                    if (tempNode.getRightChild() == None):
                        tempNode.setRightChild(newNode)
                        tempNode.getRightChild().setParent(tempNode)

                        break
                    else:
                        tempNode = tempNode.getRightChild()
        self.size+=1
    def getSorted(self,a):
        self.printTreeInOrder(self.root,a)

    def printTreeInOrder(self, node,a):
        if(node == None): return
        self.printTreeInOrder(node.getLeftChild(),a)
        a.append(node.getData())
        self.printTreeInOrder(node.getRightChild(),a)


if __name__ == '__main__':

    tr = BinarySearchTree()



    string = input()
    ans = input()
    if (len(string) == 1):
        if(string=='0'): print('WRONG_ANSWER')
        else:
            if (int(ans) <= int(string)):
                print('OK')
            else:
                print('WRONG_ANSWER')
    else:
        if (len(set(string)) == 1):
            if (string == ans):
                print('OK')
            else:
                print('WRONG_ANSWER')
        else:
            zeros = ""
            for i in range(len(string)):
                if (string[i] != '0'):
                    tr.insertNode(int(string[i]))
                else:
                    zeros += str(string[i])
            a = []
            tr.getSorted(a)
            newS = "" + str(a[0]) + str(zeros)
            for i in range(1, len(a)):
                newS += str(a[i])
            if (newS == ans):
                print('OK')
            else:
                print('WRONG_ANSWER')


    print(end='')