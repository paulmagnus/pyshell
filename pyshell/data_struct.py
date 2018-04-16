import ply.yacc as yacc

class ast:
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

    def add_children(self, children, p):
        for i in children:
            if isinstance(p[i], ast):
                p[i].parent = self
            self.children.append(p[i])

    def flatten(self, label):
        if self.label == label:
            return [self]

        result = []
        for child in self.children:
            if isinstance(child, ast):
                result += child.flatten(label)
        return result

    def __getitem__(self, index):
        return self.children[index]

    def __setitem__(self, index, value):
        self.children[index] = value

    def __repr__(self):
        return self.str_traverse()

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
