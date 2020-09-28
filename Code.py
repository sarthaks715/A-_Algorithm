import argparse as ap

import re

import copy

import platform

import pandas as pd


######## RUNNING THE CODE ####################################################

#   You can run this code from terminal by executing the following command

#   python planpath.py <INPUT/input#.txt> <OUTPUT/output#.txt> <flag>

#   for example: python planpath.py INPUT/input2.txt OUTPUT/output2.txt 0

#   NOTE: THIS IS JUST ONE EXAMPLE INPUT DATA

###############################################################################
#creating class node to store information of each node
class Node:
    def __init__(self, ident):
        self.ident = ident
        self.child = []
        self.parent = []
        self.f = 0
        self.g = 0
        self.h = 0
        self.path = ""
        self.operator = "S"
        self.n_id="N" + str(self.ident[0]) + str(self.ident[1])

#function op to calculate the operator and returning a string according to current node and next node
def op(current_node_ident, x):
    first = x[0]
    second = x[1]
    if current_node_ident[0] + 1 == first and current_node_ident[1] == second:
        operator = "D"

    elif current_node_ident[0] == first and current_node_ident[1] + 1 == second:
        operator = "R"

    elif current_node_ident[0] + 1 == first and current_node_ident[1] + 1 == second:
        operator = "RD"

    elif current_node_ident[0] + 1 == first and current_node_ident[1] - 1 == second:
        operator = "LD"

    elif current_node_ident[0] == first and current_node_ident[1] - 1 == second:
        operator = "L"

    elif current_node_ident[0] - 1 == first and current_node_ident[1] - 1 == second:
        operator = "LU"

    elif current_node_ident[0] - 1 == first and current_node_ident[1] == second:
        operator = "U"

    elif current_node_ident[0] - 1 == first and current_node_ident[1] + 1 == second:
        operator = "RU"
    else:
        operator = None
    return operator

#to get path from start node to current node
def get_path(current_node):
    path_list = []
    while len(current_node.parent) != 0:
        path_list.append(current_node.operator)
        current_node = current_node.parent[0]
    return path_list

#to get path in a string
def final_path(lst):
    path_string = ""
    for j in lst[::-1]:
        path_string = path_string + j + "-"

    return (path_string[:-1])

#returning final output as a string
def print_output(dataframe, v_list, current,start_node,goalindex):
    final_string_out = ""

    current = start_node
    x = current.ident[0]
    y = current.ident[1]
    map = dataframe
    #creating a copy of a dataframe map into a new dataframe
    new = copy.deepcopy(map)
    new.iloc[x, y] = "*"
    map_string_temp = new.to_string(index=False)
    map_string_temp2 = map_string_temp.split('\n')
    map_string_temp3 = map_string_temp2[1:]
    map_string = '\n'.join(some.replace(' ', '') for some in map_string_temp3)
    out = "S"
    final_string_out = final_string_out + map_string + "\n" + out + " " + str(current.g) + "\n"+"\n"+"\n"
    for i in v_list[1:]:
        if i == "RD":
            x = current.ident[0] + 1
            y = current.ident[1] + 1
        elif i == "LD":
            x = current.ident[0] + 1
            y = current.ident[1] - 1
        elif i == "RU":
            x = current.ident[0] - 1
            y = current.ident[1] + 1
        elif i == "LU":
            x = current.ident[0] - 1
            y = current.ident[1] - 1
        elif i == "D":
            x = current.ident[0] + 1
            y = current.ident[1]
        elif i == "R":
            x = current.ident[0]
            y = current.ident[1] + 1
        elif i == "L":
            x = current.ident[0]
            y = current.ident[1] - 1
        elif i == "U":
            x = current.ident[0] - 1
            y = current.ident[1]


        for r in current.child:
            if r.ident == [x, y]:
                #creating the next node to the current node
                current = r

        if current.ident == goalindex:
            out = out + "-" + i
            g_val = current.g
            new = copy.deepcopy(map)
            new.loc[x, y] = "*"
            map_string_temp = new.to_string(index=False)
            map_string_temp2 = map_string_temp.split('\n')
            map_string_temp3 = map_string_temp2[1:]
            map_string = '\n'.join(some.replace(' ', '') for some in map_string_temp3)
            final_string_out = final_string_out + map_string + "\n" + out + "-G" + " " + str(g_val) + "\n"+"\n\n"

            break
        else:
            out = out + "-" + i
            g_val = current.g
            new = copy.deepcopy(map)
            new.loc[x, y] = "*"
            map_string_temp = new.to_string(index=False)
            map_string_temp2 = map_string_temp.split('\n')
            map_string_temp3 = map_string_temp2[1:]
            map_string = '\n'.join(some.replace(' ', '') for some in map_string_temp3)
            final_string_out = final_string_out + map_string + "\n" + out + " " + str(g_val) + "\n"+"\n\n"

    if current.ident == goalindex:
        final_string_out = final_string_out
    else:
        final_string_out = "No Path Found"

    return final_string_out


################## YOUR CODE GOES HERE ########################################
#fidn the best path from start node to goal node in map
def graphsearch(map, flag):
    n = len(map.index)
    openlist = []
    closedlist = []
    abc = []
    goalindex = []
    for i in map.index:
        for j in map:
            if map.loc[i, j] == "S":
                abc = [i,j]
                startindex = [i, j]
    #creating a start node object of class node
    start_node = Node(abc)
    for i in map.index:
        for j in map:
            if map.loc[i, j] == "G":
                #find the goal index
                goalindex = [i, j]
    #creating the current node as start node
    current_node = start_node
    start_node.g = 0
    #calculating h of start node using heuristic function
    start_node.h = ((((goalindex[0] - current_node.ident[0]) ** 2) + (goalindex[1] - current_node.ident[1]) ** 2) ** (
            1 / 2))
    start_node.f = start_node.g + start_node.h
    #appending into a open list
    openlist.append(start_node)

    while (len(openlist) > 0):
        openlist.sort(key=lambda x: (x.f, x.g))
        current_node=openlist.pop(0)
        if flag > 0:
            count = 1
            current_node_id = "N" + str(current_node.ident[0]) + str(current_node.ident[1])
            curr = current_node
            node_lst_path = get_path(curr)
            node_path = final_path(node_lst_path)
            string = current_node_id + ":" + node_path + " " + curr.operator + " " + str(count) + " " + str(
                round(curr.g, 2)) + " " + str(round(curr.h, 2)) + " " + str(round(curr.f, 2))
            print(string)
            count = count + 1
        #appending into current node in closed list
        closedlist.append(current_node)
        if flag > 0:

            count2 = 1
            string_closed = ""
            for l in closedlist:
                path_closed = ""
                l_id = "N" + str(l.ident[0]) + str(l.ident[1])
                list_closed = get_path(l)
                path_closed = final_path(list_closed)
                string_closed = string_closed + l_id + ":" + l.operator + " " + str(count2) + " " + str(
                    round(l.g, 2)) + " " + str(round(l.h, 2)) + " " + str(round(l.f, 2)) + ","
                count2 = count2 + 1

            print("CLOSED:" + " " + string_closed[:-1])



        neigh = []
        #checking current node is equal to goal index
        if current_node.ident == goalindex:

            break

        else:
            x = current_node.ident[0]
            y = current_node.ident[1]
            newlist = []
            newlist.append([x + 1, y])
            newlist.append([x, y + 1])
            newlist.append([x + 1, y + 1])
            newlist.append([x + 1, y - 1])
            newlist.append([x, y - 1])
            newlist.append([x - 1, y - 1])
            newlist.append([x - 1, y])
            newlist.append([x - 1, y + 1])
            neigh = newlist.copy()
            #removing the out boundaries from the map
            for i in newlist:
                if i[0] > n - 1 or i[1] < 0 or i[0] < 0 or i[1] > n - 1:
                    neigh.remove(i)

            neigh2 = neigh.copy()
            xlist = []
            #appending the indexes of "X" in xlist
            for i in neigh:

                if map.iloc[i[0], i[1]] == "X":
                    xlist.append(i)
            #removing X adjacent
            for x in xlist:
                first = x[0]
                second = x[1]
                a = op(current_node.ident, x)

                if a == "D" or a == "U":
                    right1 = first
                    right2 = second + 1
                    left1 = first
                    left2 = second - 1
                    for i in neigh2:
                        if i == [right1, right2] or i == [left1, left2]:
                            try:
                                neigh.remove(i)
                            except:
                                pass

                if a == "R" or a == "L":

                    up1 = first - 1
                    up2 = second
                    down1 = first + 1
                    down2 = second
                    for i in neigh2:

                        if i == [up1, up2] or i == [down1, down2]:
                            try:
                                neigh.remove(i)
                            except:
                                pass
            #removing the X from the neigh list
            for i in xlist:
                for j in neigh2:
                    if j == i:
                        try:
                            neigh.remove(j)
                        except:
                            pass

            neigh3 = neigh.copy()
            #checking in open list
            for i in neigh3:

                for j in openlist:
                    if i == j.ident:
                        try:
                            neigh.remove(i)
                        except:
                            pass
            #checking in closed list
            for i in neigh3:
                for j in closedlist:
                    if i == j.ident:
                        try:
                            neigh.remove(i)
                        except:
                            pass
            #creating nodes
            for i in neigh:
                new_node = Node(i)
                sign = op(current_node.ident, i)
                new_node.operator = sign
                openlist.append(new_node)
                current_node.child.append(new_node)
                new_node.parent.append(current_node)

                if sign == "D" or sign == "R" or sign == "L" or sign == "U":
                    new_node.g = 2
                elif sign == "RD" or sign == "LD" or sign == "LU" or sign == "RU":
                    new_node.g = 1

                new_node.g = new_node.g + new_node.parent[0].g
                new_node.h = ((((i[0] - goalindex[0]) ** 2) + (i[1] - goalindex[1]) ** 2) ** (0.5))
                new_node.f = new_node.g + new_node.h
                new_node.path = "-" + sign

            if flag > 0:
                child_string = ""
                curr = current_node
                for c in curr.child:
                    c_id = "N" + str(c.ident[0]) + str(c.ident[1])
                    child_path = get_path(c)
                    finalstring = final_path(child_path)
                    child_string = child_string + str(c_id) + " : " + finalstring + "  " + c.operator + ","

                print("Children : " + "{" + child_string[:-1] + "}")

            if flag > 0:

                string_open = ""
                for o in openlist:
                    path_open = ""
                    o_id = "N" + str(o.ident[0]) + str(o.ident[1])
                    list_open = get_path(o)
                    path_open = final_path(list_open)
                    string_open = string_open + "(" + o_id + ":" + path_open + " " + o.operator + " " + str(
                        round(o.g, 3)) + " " + str(round(o.h, 3)) + " " + str(round(o.f, 3)) + ")" + ","

                print("OPEN :" + "{" + string_open[:-1] + "}")
                flag=flag-1


    #function call to get the path
    v = get_path(current_node)
    v_list = v[::-1]
    v_list.insert(0, "S")
    v_list.insert(len(v_list), "G")
    solution = print_output(map, v_list, current_node, start_node, goalindex)



    return solution


def read_from_file(file_name):


    file_handle = open(file_name)
    # reading the file with read() which gives as a string of the file
    read = file_handle.read()
    # Saving the value of n from the first index of the file
    n = int(read[0])
    # spliting the string
    string = read[1:].split("\n")[1:n+1]
    temp_list_1 = []
    temp_list_2 = []
    # adding into a list of list
    for i in string:
        for j in i:
            temp_list_2.append(j)
        temp_list_1.append(temp_list_2)
        temp_list_2 = []
    # creating temp_list_1 into a dataframe
    map = pd.DataFrame(temp_list_1)

    return map


###############################################################################

########### DO NOT CHANGE ANYTHING BELOW ######################################

###############################################################################


def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')

    file_handle.write(solution)


def main():
    # create a parser object

    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline

    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)

    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)

    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)

    # parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)

    # get all the arguments

    arguments = parser.parse_args()

    ##############################################################################

    # these print statements are here to check if the arguments are correct.

    #    print("The input_file_name is " + arguments.input_file_name)

    #    print("The output_file_name is " + arguments.output_file_name)

    #    print("The flag is " + str(arguments.flag))

    #    print("The procedure_name is " + arguments.procedure_name)

    ##############################################################################

    # Extract the required arguments

    operating_system = platform.system()

    if operating_system == "Windows":

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("\\")

        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT\input#.txt")

            return -1

        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("\\")

        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT\output#.txt")

            return -1

    else:

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("/")

        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT/input#.txt")

            return -1

        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("/")

        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT/output#.txt")

            return -1

    flag = arguments.flag

    # procedure_name = arguments.procedure_name

    try:

        map = read_from_file(input_file_name)  # get the map

    except FileNotFoundError:

        print("input file is not present")

        return -1

    # print(map)

    solution_string = ""  # contains solution

    solution_string = graphsearch(map, flag)

    write_flag = 1

    # call function write to file only in case we have a solution

    if write_flag == 1:
        write_to_file(output_file_name, solution_string)


if __name__ == "__main__":
    main()