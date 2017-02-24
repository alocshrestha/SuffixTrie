import string
import pudb
class Node:
    def __init__(self, suffixLink = None):
        self.children = {}
        self.start = 0
        self.end = 0
        self.suffixIndex = 0
        if suffixLink is not None:
            self.suffixLink = suffixLink
        else:
            self.suffixLink = self

    def __repr__(self):
         return "\nChildren: " + str({k:v for k,v in self.children.items() if v is not None}) + " \nStart: " + str(self.start) + " \nEnd: " + str(self.end)

class SuffixTreeNode:            
    pu.db
    def __init__(self, txt, s1):
#         self.start = 0
#         self.end = 0
#         self.suffixIndex = 0
        self.text = txt
        self.root = None
        self.Node = None
        self.lastNewNode = None
        self.activeNode = None
        self.activeEdge = -1
        self.activeLength = 0
        self.remainingSuffixCount = 0
        self.leafEnd = -1
        self.rootEnd = None
        self.splitEnd = None
        self.size = -1
        self.size1 = s1
        self.MAXCHAR = 256
        
#         self.maxHeight = 0
#         self.substringStartIndex = 0
    
    def __str__(self):
        s = ""
        for k,v in self.Node.children.iteritems():
            s += "\nKeys: " + str(k) + " Value: " + str(v)
        return s
        #return "\nNode: " + str(self.Node.children.keys()) + "\nValue: " + str(self.Node.children.values()) + "\nStart: " + str(self.start) + "\nEnd: " + str(self.end)        
            
        
    def newNode(self, start, end):
        if self.root == None:
            self.root = Node()
        if self.Node == None:
            self.Node = Node()
            	
        for i in xrange(self.MAXCHAR):
            self.Node.children[i] = None
             #self.Node.children.insert(i, None)    
        self.Node.suffixLink = self.root
        self.start = start
        self.end = end
        self.SuffixIndex = -1
        return self.Node
    
    def edgeLength(self, n):
        if n == self.root:
            return 0
        return n.end - n.start + 1
    
    def walkDown(self, currNode):
        
        if self.activeLength >= self.edgeLength(currNode):
            self.activeEdge += self.edgeLength(currNode)
            self.activeLength -= self.edgeLength(currNode)
            self.activeNode = currNode
            print "ActiveLength: " , self.activeLength
            return 1
        return 0
    
    #not sure about this function being correct
    def extendSuffixTree(self, pos):
        self.leafEnd = pos
        self.remainingSuffixCount += 1
        self.lastNewNode = None
        
        while self.remainingSuffixCount > 0:
            if self.activeLength == 0:
                self.activeEdge = pos                
            
            #There is no outgoing edge starting with activeEdge from activeNode    
            if self.activeNode.children[ord(self.text[self.activeEdge])] == None:
            #if self.text[self.activeEdge] not in self.activeNode.children:
                self.activeNode.children[ord(self.text[self.activeEdge])] = self.newNode(pos, self.leafEnd)        
                
                if self.lastNewNode != None:
                    self.lastNewNode.suffixLink = self.activeNode
                    self.lastNewNode = None
                    
            else: #There is an outgoing edge starting with activeEdge from activeNode                
                next_node = self.activeNode.children[ord(self.text[self.activeEdge])]                
#                 if self.walkDown(next_node):
#                     continue
                self.walkDown(next_node)
                
                if self.text[next_node.start + self.activeLength] == self.text[pos]:
                    if self.lastNewNode != None and self.activeNode != self.root:
                        self.lastNewNode.suffixLink = self.activeNode
                        self.lastNewNode = None
                    self.activeLength += 1
                    break
                
                self.splitEnd = next_node.start + self.activeLength - 1
                
                #new internal node
                split = self.newNode(next_node.start, self.splitEnd)
                self.activeNode.children[ord(self.text[self.activeEdge])] = split
                
                #new leaf coming out of new internal node
                split.children[ord(self.text[pos])] = self.newNode(pos, self.leafEnd)
                next_node.start += self.activeLength
                split.children[ord(self.text[next_node.start])] = next_node
                
                if self.lastNewNode != None:
                    self.lastNewNode.suffixLink = split
                
                self.lastNewNode = split
                
            self.remainingSuffixCount -= 1
            if self.activeNode == self.root and self.activeLength > 0:
                self.activeLength -= 1
                self.activeEdge = pos - self.remainingSuffixCount + 1
                
            elif self.activeNode != self.root:
                self.activeNode = self.activeNode.suffixLink
                
    def printf(self, i, j):
        for k in xrange(i, j):
            if self.text[k] != '#':
                print "%c", self.text[k]
            if k <= j:
                print "#"
                
    
    def setSuffixIndexByDFS(self, n, labelHeight):
        """ Print the suffix tree along with setting suffix index
            So tree will be printed in DFS manner
            Each edge along with it's suffix index will be printed """
        if n == None: return
        if n.start != -1: # a non-root node
            self.printf(n.start, n.end)
        
        leaf = 1
        for i in xrange(self.MAXCHAR):
            if n.children[i] != None: #Current node is not a leaf as it has outgoing edges from it
                leaf = 0
                self.setSuffixIndexByDFS(n.children[i], labelHeight + self.edgeLength(n.children[i]))
                
        if leaf == 1:
            for i in xrange(n.start, n.end):
                if self.text[i] == '#':
                    n.end = i
            n.suffixIndex = self.size - labelHeight
            
    
    def buildSuffixTree(self):
        self.size = len(self.text)
        self.rootEnd = -1 
        
        self.root = self.newNode(-1, self.rootEnd)
        self.activeNode = self.root
        
        for i in xrange(self.size):
            self.extendSuffixTree(i)
        
        labelHeight = 0
        self.setSuffixIndexByDFS(self.root, labelHeight)
    
    #not sure about this - edited
    def doTraversal(self, n, labelHeight, maxHeight, substringStartIndex):
        if n == None: return
        ret = -1        
        print n.suffixIndex, self.size1
        if n.suffixIndex < 0: #if it is internal node
            for i in xrange(self.MAXCHAR):                
                if n.children[i] != None:                    
                    ret = self.doTraversal(n.children[i], labelHeight + self.edgeLength(n.children[i]), maxHeight, substringStartIndex)
                    #ret = self.doTraversal(n.children[i], labelHeight + self.edgeLength(n.children[i]), self.maxHeight, self.substringStartIndex)
                    
                    if n.suffixIndex == -1:
                        n.suffixIndex = ret
                    elif n.suffixIndex == -2 and ret == -3 | \
                        n.suffixIndex == -3 and ret == -2 | \
                        n.suffixIndex == -4:
                        
                        n.suffixIndex = -4 #Mark node as XY
                        #keep track of deepest node
                        if maxHeight < labelHeight:
                            maxHeight = labelHeight
#                         if self.maxHeight < labelHeight:
#                             self.maxHeight = labelHeight            
                            substringStartIndex = n.end - labelHeight + 1
        elif n.suffixIndex > -1 and n.suffixIndex < self.size1: #suffix of X
            return -2 #mark node as X
        
        elif n.suffixIndex >= self.size1: #suffix of Y
            return -3 #mark node as Y
        return n.suffixIndex
    
    
    # edited - not certain about this func as maxHeight is 0 not sure how this var changes
    def getLongestCommonSubstring(self):
        maxHeight = 0
        substringStartIndex = 0
        r = self.doTraversal(self.root, 0, maxHeight, substringStartIndex)
        print 'traversal returned', r
        print "maxheight " , maxHeight
        i = 0
        for k in xrange(maxHeight):
            i = k
            print "%c", self.text[k + substringStartIndex]            
        if i == 0:
            print "No common Substring"
        else:
            print ", of lenght: %d", maxHeight
        print "\n"


if __name__ == "__main__":
	N = SuffixTreeNode("xabxac#abcabxabcd$", 7)
	N.buildSuffixTree()
