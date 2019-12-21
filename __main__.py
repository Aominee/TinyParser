import sys
#For GUI
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QLabel, QTextEdit, QWidget
#Our Scanner (will dispose)
from scanner import TinyScanner
#Our Parser (will edit)
from tinyparser import Parser
import networkx as nx
#For plotting an image
import matplotlib.pyplot as plt


#inherit from QWidget -> TinyParserWidget
class TinyParserWidget(QWidget):
    #Constructor
    def __init__(self):
        #Calls the parent's constructor first
        super().__init__()
        #My own constructor code
        self.initUI()

    def initUI(self):
        #Create QLabel with TinyParserWidget as Parent
        lbl = QLabel('Enter Tiny Code', self)
        #Define input_code = QTextEdit
        self.input_code = QTextEdit()
        #Call function add_initial_code to popualize our input_code aka the QTextEdit
        self.add_initial_code()
        #Defines submit_button = QPushButton
        submit_button = QPushButton('Parse')
        #Add a callback for the button
        submit_button.clicked.connect(self.submitted)
        #Creates a QGridLayout object
        grid = QGridLayout()
        #Sets the grid's spacing to 10
        grid.setSpacing(10)
        #Adds the first item (the label)
        grid.addWidget(lbl, 1, 0)
        #Adds the second item (the text)
        grid.addWidget(self.input_code, 1, 1)
        #Adds the third item (the submit button)
        grid.addWidget(submit_button, 2, 1)
        #Specifies for the Widget to use the grid
        self.setLayout(grid)
        #Specifies the window size for the widget
        self.setGeometry(300, 300, 350, 300)
        #Sets a window title for the wiget
        self.setWindowTitle('Tiny Parser')
        #Finally show the widget
        self.show()

    #Adds all the needed text for a simple Tiny Language Code
    def add_initial_code(self):
        self.input_code.append("read x;")
        self.input_code.append("if 0<x then")
        self.input_code.append("    fact:=1;")
        self.input_code.append("    repeat")
        self.input_code.append("        fact:=fact*x;")
        self.input_code.append("        x:=x-1")
        self.input_code.append("    until x=0;")
        self.input_code.append("    write fact")
        self.input_code.append("end")

    def draw(self):
        #Rename G to graph
        graph = self.G
        #Specify you will use 'dot'
        pos = nx.nx_pydot.graphviz_layout(graph, prog='dot')
        #Specify all the node labels
        labels = dict((n, d['value']) for n, d in graph.nodes(data=True))
        #Draw given the graph, the format, and the labels
        nx.draw(graph, pos, labels=labels, with_labels=True, arrows=False)
        #Show the graph
        plt.show()

    def submitted(self):
        #Create a TinyScanner object, and pass to it our Tiny Code in the constructor
        #scanned_code = TinyScanner(self.input_code.toPlainText())
        #Call scan() on the object to start Scanning
        #scanned_code.scan()
        self.code_list = []
        self.tokens_list = []

        for eachLine in self.input_code.toPlainText().splitlines():
        	lineParts = eachLine.split(',')
        	self.code_list.append(lineParts[0].strip())
        	self.tokens_list.append(lineParts[1].strip())

        
        #Create Parser object with empty constructor
        parse_code = Parser()
        #Set the token list and code list???
        parse_code.set_tokens_list_and_code_list(self.tokens_list, self.code_list)
        #Call run() on the parser object
        parse_code.run()
        #Retrieve the nodes_table and edges table from the Parser object
        nodes_list = parse_code.nodes_table
        edges_list = parse_code.edges_table

        #Defines a diagraph object and stores in variable G
        self.G = nx.DiGraph()
        #Add the nodes to the diagraph
        for node_number, node_value in nodes_list.items():
            self.G.add_node(node_number, value=node_value)
        #Add the edgs to the diagram
        self.G.add_edges_from(edges_list)
        #Clear the tables nodes_table and edges_table and..
        parse_code.clear_tables()

        #self.code_list.clear()
        #self.tokens_list.clear()
        self.draw()

app = QApplication(sys.argv)
#Create Object from TinyParserWidget class
w = TinyParserWidget()
sys.exit(app.exec_())