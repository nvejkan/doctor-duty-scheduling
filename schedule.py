# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 20:39:01 2017

@author: nattawutvejkanchana
"""
from days import *

class Node:
    def __init__( self, parent, day_no,isweekday,duty1,duty2,teach_duty ):
		# Contains the node that generated this node
        self.parent = parent #board object
        self.day_no = day_no
        self.isweekday = isweekday
        self.duty1 = duty1
        self.duty2 = duty2 #duty1 != duty2
        self.teach_duty = teach_duty
    def get_no_duty(self, pname):
        return int(self.isweekday and (self.duty1 == pname or self.duty2 == pname))
    def get_no_teach_duty(self, pname):
        return int(self.isweekday and self.teach_duty == pname)
    def get_no_duty_weekend(self, pname):
        return int( (not self.isweekday) and (self.duty1 == pname or self.duty2 == pname))
    def get_no_teach_duty_weekend(self, pname):
        return int( (not self.isweekday) and self.teach_duty == pname)
    def __str__(self):
        return "{0}\t{1}\t{2}\t{3}\t{4}".format(self.day_no,self.isweekday,self.duty1,self.duty2,self.teach_duty)
    def get_duty_names(self):
        return {self.duty1,self.duty2,self.teach_duty}
    def get_day_no(self):
        return self.day_no
       
def node_duty_count(node,pname):
    if node.parent == None:
        no_duty = node.get_no_duty(pname)
        no_teach_duty = node.get_no_teach_duty(pname)
        no_duty_weekend = node.get_no_duty_weekend(pname)
        no_duty_teach_weekend = node.get_no_teach_duty_weekend(pname)
    else:
        no_duty = node.get_no_duty(pname) \
                    + node_duty_count(node.parent,pname)[0]
        no_teach_duty = node.get_no_teach_duty(pname)\
                        + node_duty_count(node.parent,pname)[1]
        no_duty_weekend = node.get_no_duty_weekend(pname)\
                            + node_duty_count(node.parent,pname)[2]
        no_duty_teach_weekend = node.get_no_teach_duty_weekend(pname)\
                                + node_duty_count(node.parent,pname)[3]
    return (no_duty,no_teach_duty,no_duty_weekend,no_duty_teach_weekend)

def completeness_all_people(node,ppl):
    for p in ppl:
        if not check_completeness(node,p):
            return False
    
    return True
def check_completeness(node,p):
    no_duty,no_teach_duty,no_duty_weekend,no_duty_teach_weekend = node_duty_count(node,p)
    if (no_duty in (6,7)) \
        and no_duty_weekend in (2,3) \
        and no_teach_duty in (1,2) \
        and no_duty_teach_weekend in (1,2):
            return True
    else:
        return False
def check_constraint(node,p):
    no_duty,no_teach_duty,no_duty_weekend,no_duty_teach_weekend = node_duty_count(node,p)
    if no_duty > 7 \
        or no_duty_weekend > 3 \
        or no_teach_duty > 2 \
        or no_duty_teach_weekend > 2:
            return False
    else:
        return True
        
def check_all_people(node,ppl):
    for p in ppl:
        if not check_constraint(node,p):
            return False
    
    return True

def print_sol(node):
    temp = node
    while True:
        print(temp)
        if temp.get_day_no() == 1:
            break
        temp = temp.parent
def dfs(nodes):
    while True:
        # We've run out of states, no solution.
        if len( nodes ) == 0:
            print("NO nodes left!")
            return None
    		# take the node from the front of the queue
        node = nodes.pop(0)
        if node.get_day_no() == 31 and completeness_all_people(node,ppl):
            print("Solution found!")
#            temp = node
#            while True:
#                print(temp)
#                if temp.get_day_no() == 1:
#                    break
#                temp = temp.parent
            print_sol(node)
            #print(count,moves)
            return True
            #print("-------------------------sol_x---------------------")
#        if node.get_day_no() > 5:
#            print('5 break')
#            return False
#        if node.get_day_no() ==10:
#            print('10 break')
#            temp = node
#            while True:
#                print(temp)
#                if temp.get_day_no() == 1:
#                    break
#                temp = temp.parent
#            return False
        if(node.get_day_no() == 10):
            print_sol(node)
        print(len(nodes),node.get_day_no())
        new_nodes = expand_node(node)
        new_nodes.extend(nodes)
        nodes = new_nodes
        
def expand_node(node):
    expanded_nodes = []
    correct_nodes = []
    parent_names = node.get_duty_names()
    eligible_names = set(ppl) - parent_names
    new_day_no = node.get_day_no() + 1
    if new_day_no <= 31 and len(eligible_names) > 0:
    #pattern1 : only 1 duty
        l_pattern1 = list(itertools.combinations(eligible_names, 1))
        new_nodes = [ Node(node
                        ,new_day_no
                        ,is_weekday(dates_in_month[new_day_no-1])
                        ,pat[0]
                        ,None
                        ,None) for pat in l_pattern1 ]
        expanded_nodes.extend(new_nodes)
        #pattern2 : duty1 and duty2 or duty1 and teach
        l_pattern2 = list(itertools.combinations(eligible_names, 2))
        if len(l_pattern2) > 0:
            new_nodes = [ Node(node
                            ,new_day_no
                            ,is_weekday(dates_in_month[new_day_no-1])
                            ,pat[0]
                            ,pat[1]
                            ,None) for pat in l_pattern2 ]
            expanded_nodes.extend(new_nodes)
            if teachable:
                new_nodes = [ Node(node
                            ,new_day_no
                            ,is_weekday(dates_in_month[new_day_no-1])
                            ,pat[0]
                            ,None
                            ,pat[1]) for pat in l_pattern2 ]
                expanded_nodes.extend(new_nodes)
                
        for n in expanded_nodes:
            if check_all_people(n,ppl):
                correct_nodes.append(n)
        return correct_nodes
    
    

if __name__ == '__main__':
    dates_in_month = get_dates_in_month(2017,3) #year, month
    ppl = ['A','B','C','D'] #people
    teachable = True 
#    n1 = Node(None,1,is_weekday(dates_in_month[1-1]),'A',None,None)
#    n2 = Node(n1,2,is_weekday(dates_in_month[2-1]),'B','C',None)
#    n3 = Node(n2,3,is_weekday(dates_in_month[3-1]),'A',None,None)
#    n4 = Node(n3,4,is_weekday(dates_in_month[4-1]),'B',None,None)
#    print(n1)
#    print(n2)
#    print(n3)
#    print(n4)
    nodes = [ Node(None,1,is_weekday(dates_in_month[1-1]),p,None,None) for p in ppl ]
    #n = nodes[0]
    #new_nodes = expand_node(n)
    dfs(nodes)