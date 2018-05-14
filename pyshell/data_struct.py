################################################################################
#
# data_struct.py
#
# This contains the definition of the abstract syntax tree structure.
#
# Written by Paul Magnus in Spring 2018
#
################################################################################

import ply.yacc as yacc


################################################################################
# ast                                                                          
# A PyShell abstract syntax tree node.                                         
#                                                                              
# Attributes:                                                                  
# label - This is the name of the node.  It is used in several processes to    
#   differentiate betweeen different types of nodes.                           
#                                                                              
# children - This is a list of the children of this node. Children are usually 
#   abstract syntax tree nodes but may be strings.  The number and types of    
#   children are consistent across all nodes of the same kind.  Children can   
#   also be accessed through the overloaded indexing operator (n.children[0] is
#   equivalent to n[0])                                                        
#                                                                              
# parent - This is the abstract syntax tree node which contains this node as a 
#   child.  All nodes have a parent defined except for the root node which has 
#   a parent of None.                                                          
#                                                                              
# lineNum - This is an integer representing the line number upon which the code
#   that this node represents resides in the CSPy code.                        
#                                                                              
# endLineNum - This is an integer representing the line number upon which the  
#   end of the code that this node represents resides in the CSPy code.        
#                                                                              
# position - This is an integer representing the index of the first character  
#   of the code that this node represents with respect to the whole file.      
#                                                                              
# endPosition - This is an integer representing the index of the last character
#   of the code that this node represents with respect to the whole file.      
#                                                                              
# column - This is an integer representing the index of the first character    
#   of the code that this node represents with respect to the line that the    
#   code is on. The function "set_column_num(sourceCode)" must be called on    
#   the root of the tree in order to initialize this attribute.                
#                                                                              
# endColumn - This is an integer representing the index of the last character  
#   of the code that this node represents with respect to the line that the    
#   code is on.  If the code spans multiple lines, then "endColumn" is the     
#   number of characters after the first character of the first line of the    
#   code.  The function "set_column_num(sourceCode)" must be called on the     
#   root of the tree in order to initialize this attribute.                    
#                                                                              
# line - This is a string representing the line or line upon which the code    
#   that this node represents resides in the CSPy code.  The function          
#   "set_column_num(sourceCode)" must be called on the root of the tree        
#   in order to initialize this attribute.                                     
################################################################################
class ast:
    #########################################################################
    # __init__(p:YaccProduction, label:string, * children:int)              
    # This method initializes the Abstract Syntax Tree node.  The method is 
    # a YaccProduction "p" which is the parsing symbol that the ast node    
    # represents, a string "label" which is the name and type of the node,  
    # and a tuple of integers "children" which are the indexes of "p" that  
    # should be added to "self.children".                                   
    #########################################################################
    def __init__(self, p, label, *children):
        self.label = label
        self.children = []
        self.add_children(list(children), p)
        self.parent = None
        self.column = 0
        self.endColumn = 0
        self.line = ""
        self.varname = None

        # Set line number and position for non empty nodes
        if isinstance(p, yacc.YaccProduction):
            self.lineNum, self.endLineNum = p.linespan(0)
            self.position, self.endPosition = p.lexspan(0)
            if (len(p) > 1 and type(self.children[-1]) == str):
                self.endPosition += len(self.children[-1]) - 1

        else:
            self.lineNum = 0
            self.endLineNum = 0
            self.position = 0
            self.endPosition = 0

    #########################################################################
    # set_column_num(s:string)                                              
    # This method sets the values of the "column", "endColumn", and "line"  
    # attributes for this node and for all nodes that this node dominates.  
    # The method is given a string "s" which is the CSPy source code.       
    #########################################################################
    def set_column_num(self, s):
        last_nl = s.rfind('\n', 0, self.position)
        if last_nl < 0:
            last = -1

        next_nl = s.find('\n', self.endPosition, len(s))
        if next_nl < 0:
            next_nl = len(s)

        self.column = self.position - last_nl
        self.endColumn = self.endPosition - last_nl
        self.line = s[last_nl + 1:next_nl]

        for child in self.children:
            if isinstance(child, ast):
                child.set_column_num(s)

    #########################################################################
    # add_children(children:list of int, p:YaccProduction)                  
    # This method adds certain children from "p" to the children of the     
    # current node given their indices.  The method is given a list of      
    # integers "children" which are the indices of the children of "p"      
    # which should be added to the children of the current node, and        
    # a YaccProduction "p" which is the grammar symbol whose children are   
    # being added to the children of the current node.                      
    #########################################################################
    def add_children(self, children, p):
        for i in children:
            if isinstance(p[i], ast):
                p[i].parent = self
            self.children.append(p[i])

    #########################################################################
    # flatten(label:string) -> list of ast                                  
    # This method flattens the current tree an return a list of tree nodes.  
    # The method is given a string "label" which is the label of the nodes  
    # which should be the elements of the list.                             
    #########################################################################
    def flatten(self, label):
        if self.label == label:
            return [self]

        result = []
        for child in self.children:
            if isinstance(child, ast):
                result += child.flatten(label)
        return result

    #########################################################################
    # __getitem__(index:int) -> ast                                         
    # This method overloades the indexing operator for abstract syntax      
    # trees.  The method is given an integer "index" which is the index of  
    # the element returned. The method return an element of "self.children" 
    # with the given index. Thus, the following expressions are equivalent: 
    # myTree[index]                                                         
    # myTree.__getitem__(index)                                             
    # myTree.children[index]                                                
    #########################################################################
    def __getitem__(self, index):
        return self.children[index]

    #########################################################################
    # __setitem__(index:int, value:ast)                                     
    # This method overloads the indexing assignment operator for abstract   
    # syntax tree.  The method is given an integer "index" which is the     
    # index of the element to be set and an abstract syntax tree "value"    
    # which is the value to be set at the given index.  The method sets the 
    # values of "self.children" at the given index.  Thus, the following    
    # statements are equivalent:                                            
    # myTree[index] = childTree                                             
    # myTree.__setitem__(index, childTree)                                  
    # myTree.children[index] = childTree                                    
    #########################################################################
    def __setitem__(self, index, value):
        self.children[index] = value

    #########################################################################
    # __repr__() -> string                                                  
    # This method returns a string representation of the abstract syntax    
    # tree.  The string representation is formatted as follows:             
    # (lineNum,lexPosition:treeDepth:label:environment:type,                
    #  child1,                                                               
    #  child2,                                                              
    #  ...                                                                  
    #  childn                                                               
    # )                                                                     
    #########################################################################
    def __repr__(self):
        return self.str_traverse()

    #########################################################################
    # str_traverse(depth:int) -> string                                     
    # This method is a recursive helper function for the "__repr__" method. 
    # The method is given an integer "depth" which represents the recursive 
    # depth of the current node.  The output is formatted as follows:       
    # (lineNum,lexPosition:treeDepth:label:environment:type,                
    #  child1,                                                              
    #  child2,                                                              
    #  ...                                                                  
    #  childn                                                               
    # )                                                                     
    #########################################################################
    def str_traverse(self, depth = 0):
        result = "(" + repr(self.lineNum) + "," + repr(self.position) + ":" + \
                 repr(depth) + ":" + repr(self.label)

        for child in self.children:
            result += ",\n" + " " * (depth + 1)
            if isinstance(child, ast):
                result += child.str_traverse(depth + 1)
            else:
                result += repr(child)
        
        result += "\n" + " " * depth + ")"
        return result
