import matplotlib.pyplot as plt
import time #timeモジュールのインポート
import math 
import csv
import random
import statistics
import sys


def cross_check (a, b, c, d): #クロスしてたらTRUE
    if a == c or a == d or b == c or b ==d:
        return False
    if a[0] >= b[0]:
        if (a[0] < c[0] and a[0] < d[0]) or (b[0] > c[0] and b[0] > d[0]):
            return False
    else:
        if (b[0] < c[0] and b[0] < d[0]) or (a[0] > c[0] and a[0] > d[0]):
            return False

    if a[1] >= b[1]:
        if (a[1] < c[1] and a[1] < d[1]) or (b[1] > c[1] and b[1] > d[1]):
            return False
    else:
        if (b[1] < c[1] and b[1] < d[1]) or (a[1] > c[1] and a[1] > d[1]):
            return False

    if ((a[0]-b[0])*(c[1]-a[1]) + (a[1]-b[1])*(a[0]-c[0])) * ((a[0]-b[0])*(d[1]-a[1]) + (a[1]-b[1])*(a[0]-d[0])) > 0:
        return False
    if ((c[0]-d[0])*(a[1]-c[1]) + (c[1]-d[1])*(c[0]-a[0])) * ((c[0]-d[0])*(b[1]-c[1]) + (c[1]-d[1])*(c[0]-b[0])) > 0:
        return False
    return True


def cross_check_all(edge_list,edge_check_list,v1, v2, v3, p_list, tar_edge):#クロスしてたらTRUE
    for i in range(len(edge_list)):
        if cross_check(p_list[edge_list[i][0]], p_list[edge_list[i][1]], v1, v2):
            return True
        if cross_check(p_list[edge_list[i][0]], p_list[edge_list[i][1]], v1, v3):
            return True
    for i in range(len(edge_check_list)):
        if cross_check(p_list[edge_check_list[i][0]], p_list[edge_check_list[i][1]], v1, v2):
            return True
        if cross_check(p_list[edge_check_list[i][0]], p_list[edge_check_list[i][1]], v1, v3):
            return True
    return False


def line_on_p_check (p,a,b):#線上にあったらTRUE
    if (a[0] <= p[0] and p[0] <= b[0] ) or (b[0] <= p[0] and p[0] <= a[0] ):
        if (a[1] <= p[1] and p[1] <= b[1] ) or (b[1] <= p[1] and p[1] <= a[1] ):
            if (p[1] *(a[0]-b[0])) + (a[1] *(b[0]-p[0])) + (b[1] * (p[0]-a[0])) == 0:
                return True 
    return False 


def sign (p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])


def area_check (p_list, tar_p, tar_edge,edge_check_list, edge_list):#クロスしてたらFALSE
    b1 = True
    b2 = True
    b3 = True
    v1 = p_list[tar_p]
    v2 = p_list[tar_edge[0]]
    v3 = p_list[tar_edge[1]]
    for i in range (len(p_list)):
        if i == tar_p or i == tar_edge[0] or i == tar_edge[1]:
            continue
        else:
            b1 = sign(p_list[i], v1, v2) < 0
            b2 = sign(p_list[i], v2, v3) < 0
            b3 = sign(p_list[i], v3, v1) < 0
            if ((b1 == b2) and (b2 == b3)):
                return False
            if line_on_p_check(p_list[i],v1,v2) or line_on_p_check(p_list[i],v1,v3):
                return False
        if cross_check_all(edge_list,edge_check_list,v1, v2, v3, p_list,tar_edge):
            return False
    return True    


def list_copy (a,b):
    for i in range (len(b)):
        a[i] = b[i] 


def insert_edge_check_list(edge_check_list, tar_p, a, b):
    if tar_p < a:
        aa = [tar_p, a]
        edge_check_list.append(aa)
    else:
        aa = [int(a), int(tar_p)]
        edge_check_list.append(aa)
    if tar_p < b:
        aa = [tar_p, b]
        edge_check_list.append(aa)
    else:
        aa = [b, tar_p]
        edge_check_list.append(aa)


def edge_compare(a, b):
    if a[0] < b[0] or ((a[0] == b[0]) and (a[1] <b[1]) ):
        return True
    return False


def update_edge(edge_check_list,edge_list, end_num):
    tar_num = end_num
    tar_edge = edge_check_list[tar_num]
    edge_check_list.pop(tar_num)


def edge_connect(edge_list, edge_route):
    tar_edge = edge_list[0][0]
    edge_route.append (tar_edge)
    while len(edge_list) != 1:
        for i in range (len(edge_list)):
            if edge_list[i][0] == tar_edge:
                tar_edge = edge_list[i][1]
                edge_route.append (tar_edge)
                edge_list.pop(i)
                break
            elif edge_list[i][1] == tar_edge:
                tar_edge = edge_list[i][0]
                edge_route.append (tar_edge)
                edge_list.pop(i)
                break


def cp(x1, y1, x2, y2):#外積
    return x1*y2 - x2*y1


def culc_area(edge_route, p_list):
    s = 0
    for i in range (len(edge_route)-1):
        s += cp(p_list[edge_route[i]][0], p_list[edge_route[i]][1], p_list[edge_route[i+1]][0], p_list[edge_route[i+1]][1])
    s += cp(p_list[edge_route[len(edge_route)-1]][0], p_list[edge_route[len(edge_route)-1]][1], p_list[edge_route[0]][0], p_list[edge_route[0]][1])
    return abs(s)/2


def paint_lines(p_list, min_edge_route):
    route_x = []
    route_y = []
    for i in range(len(min_edge_route)):
        route_x.append(p_list[min_edge_route[i]][0])
        route_y.append(p_list[min_edge_route[i]][1])
    route_x.append(p_list[min_edge_route[0]][0])
    route_y.append(p_list[min_edge_route[0]][1])

    plt.plot(route_x, route_y)
    plt.scatter(route_x, route_y, color = "b", label="score")
    plt.draw()
 

def edge_random_pick(p_list, min_edge_route, min_area,random_edge_route, result_area_list,time_list):
    p_check_list = []
    for i in range (len(p_list)):
        p_check_list.append(i)
    edge_list = []
    edge_check_list = [[0,1],[0,2],[1,2]]

    p_check_list.remove(2)
    p_check_list.remove(1)
    p_check_list.remove(0)
    while (len(p_check_list)) != 0:
    
        tar_edge = random.randint(0,len(edge_check_list)-1)
        tar_point = random.randint(0,len(p_check_list)-1)
        for i in range(len(p_check_list)):
            x_point  = (tar_point+i) % len(p_check_list) 
            if area_check(p_list, p_check_list[x_point], edge_check_list[tar_edge],edge_check_list, edge_list) == True:
                insert_edge_check_list(edge_check_list, p_check_list[x_point], edge_check_list[tar_edge][0], edge_check_list[tar_edge][1])
                p_check_list.pop(x_point)
                update_edge(edge_check_list, edge_list, tar_edge)
                break
            if i ==len(p_check_list)-1:
                edge_list.append(edge_check_list.pop(tar_edge))
        if len(edge_check_list) ==0:
            break
    for i in range (len(edge_check_list)):
        edge_list.append(edge_check_list[i])
    edge_route = []
    edge_connect(edge_list, edge_route)
    list_copy(random_edge_route,edge_route)
    area = culc_area(edge_route, p_list)
    result_area_list.append(area)
    print(area)
    if min_area[0] > area:
        list_copy(min_edge_route,edge_route)
        min_area[0] = area
        

if __name__ == '__main__':
    filename = sys.argv[1]
    csv_file = open(filename, "r", encoding="ms932", errors="", newline="" )
    f = csv.reader(csv_file, delimiter="	", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    header = next(f)
    p_num = int(header[0])
    p_list = [[int(row[1]), int(row[2])] for row in f]

    min_area = [100000000]
    result_area_list = []
    time_list = []
    random_edge_route= [i for i in range(len(p_list))]
    min_edge_route = [i for i in range(len(p_list))]
    fig, ax = plt.subplots()
    loop_num = 100

    for i in range(loop_num):
        edge_random_pick(p_list, min_edge_route, min_area, random_edge_route, result_area_list,time_list)
        ax.cla()
        route_x = []
        route_y = []
        for i in range(len(random_edge_route)):
            route_x.append(p_list[random_edge_route[i]][0])
            route_y.append(p_list[random_edge_route[i]][1])
        route_x.append(p_list[random_edge_route[0]][0])
        route_y.append(p_list[random_edge_route[0]][1])
        plt.scatter(route_x, route_y, color = "b", label="score")
        plt.plot(route_x, route_y)
        plt.draw()  
        plt.pause(0.3)

    print ("最小面積 Minimum area",min_area[0])
    print("面積中央値 Median area" ,statistics.median(result_area_list))
    print("面積平均 area average" ,statistics.mean(result_area_list))


    ax.cla()
    route_x = []
    route_y = []
    for i in range(len(min_edge_route)):
        route_x.append(p_list[min_edge_route[i]][0])
        route_y.append(p_list[min_edge_route[i]][1])
    route_x.append(p_list[min_edge_route[0]][0])
    route_y.append(p_list[min_edge_route[0]][1])

    plt.plot(route_x, route_y)
    plt.scatter(route_x, route_y, color = "b", label="score")

    plt.show()  
