import sys
from random import *
import pygame
import time
from collections import deque
from math import *
import heapq
from pygame.locals import QUIT,KEYDOWN,K_LEFT,K_RIGHT,K_UP,K_DOWN,Rect,MOUSEBUTTONDOWN,K_SPACE
pygame.init()
FPSCLOCK = pygame.time.Clock()
size=(1000,630)
SURFACE = pygame.display.set_mode(size)
color={
    "black":[0,0,0],
    "white":[255,255,255],
    "red":[255,0,0],
    "blue":[0,0,255],
    "yellow":[255,255,0],
    "green":[0,255,0],
    "gray":[192,192,192]
    }

node=45
start=1
end=45
fps=100
#((n_distance*10)/(v*fps))) => 틱당 이동거리
#v/10 : 초

side_empty=100
n_distance=100
ball_size=20 #반지름
weight_size=30
num_size=25
length_c=((size[0]-side_empty*2)//n_distance+1)#가로 개수
width_c=((size[1]-side_empty*2)//n_distance+1)#세로 개수

graph=[[]for i in range(node+1)]
q = []
path=[i for i in range(node+1)]
distance = [inf]*(node+1)
g_c=[[inf for i in range(node+1)]for g in range(node+1)]
map_p=[[[-1,-1]for i in range(length_c+2)]for g in range(width_c+2)]

def n_pos(length_c,num):
    return [(num-1)//length_c,(num-1)%length_c]#y,x

class Car():
    def __init__(self,start,end,mode):
        global SURFACE
        self.ps=0
        self.mode=mode #mode = 1 : 처음에만 최단시간 경로 시행,mode = 2 : 계속 탐색하며 최단 시간 경로 시행
        self.start=start
        self.end=end
        self.last_node=-1
        self.now_node=start
        self.tick=0
        self.time=0
        self.fh=0
        self.cnt=0
        self.t_d=0
        self.SURFACE=SURFACE
        if self.mode==1:
            self.color=color["yellow"]
        else:
            self.color=color["green"]

        sq=n_pos(length_c,self.start)
        self.pos=[map_p[sq[0]][sq[1]][0],map_p[sq[0]][sq[1]][1]]
        self.dka()
    
    def dka(self):
        dijkstra(self.now_node)
        self.R=backtrack(self.end,self.now_node)

    def car_move(self):
        A=n_pos(length_c,self.last_node)
        B=n_pos(length_c,self.now_node)
        if A[0]==B[0]:
            if A[1]<B[1]:
                self.pos[0]+=self.t_d
            else:
                self.pos[0]-=self.t_d
        else:
            if A[0]<B[0]:
                self.pos[1]+=self.t_d
            else:
                self.pos[1]-=self.t_d

    def car_draw(self):
        pygame.draw.circle(self.SURFACE,self.color,self.pos,10)

    def car_g(self):
        if self.ps==0:
            if self.mode==2:
                self.dka()
            #print(R)
            if self.end==self.now_node:
                self.fh=1
                #print("@#")
                return
            self.last_node=self.R[0]
            self.now_node=self.R[1]
            self.time+=graph[self.R[0]][g_c[self.R[0]][self.R[1]]][1]
            A=graph[self.R[0]][g_c[self.R[0]][self.R[1]]][1]/10
            #print(A*5)
            self.tick=1#A*fps
            self.cnt=0
            self.ps=1
            self.t_d=100#(n_distance/self.tick)
            #print(car['tick'],car['t_d'],n_distance)
        else:
            self.cnt+=1
            if self.cnt>=self.tick:
                Q=n_pos(length_c,self.now_node)
                self.pos=[map_p[Q[0]][Q[1]][0],map_p[Q[0]][Q[1]][1]]
                self.ps=0
                if self.mode==1:self.R.pop(0)
            else:
                self.car_move()

        self.car_draw()


def dijkstra(start):
    global distance
    global path
    global q
    distance = [inf]*(node+1)
    distance[start] = 0 
    heapq.heappush(q,(0,start))
    while q:
        #print(q)
        # print(data)
        # print(distance)
        dist, now_node = heapq.heappop(q)
        for n_n, weight in graph[now_node]:
            if (n_n,weight)==[-1,-1]:break
            cost = dist + weight
            if cost < distance[n_n]:
                distance[n_n] = cost
                path[n_n]=now_node
                heapq.heappush(q,(cost,n_n))

def backtrack(start,end):
    #print(path)
    node=start
    bt=[node]
    while node!=end:
        #print(node)
        #A=((node-1)//length_c,(node-1)%length_c)
        #B=((path[node]-1)//length_c,(path[node]-1)%length_c)
        #pygame.draw.line(SURFACE,color["green"],map_p[A[0]][A[1]],map_p[B[0]][B[1]],3)

        bt.append(path[node])
        node=path[node]


    bt.reverse()
    return bt

def text_pr(txt,x,y,size,color):
    myFont = pygame.font.Font( None, size)
    text_Title= myFont.render(txt, True,color)
    text_Rect = text_Title.get_rect()
    text_Rect.center = (x,y)
    SURFACE.blit(text_Title, text_Rect)

def map_produce(width_c,length_c,side_empty,n_distance,node):
    global map_p
    cnt=0
    for i in range(width_c):
        for g in range(length_c):
            cnt+=1
            if cnt>node:
                graph_produce(width_c,length_c)
                return
            map_p[i][g]=[side_empty+n_distance*g,side_empty+n_distance*i]
    graph_produce(width_c,length_c)

def graph_produce(width_c,length_c):
    global map_p,graph
    for i in range(width_c):
        for g in range(length_c):
            if map_p[i][g]==[-1,-1]:return
            A=length_c*i+g+1
            B=length_c*(i+1)+g+1
            C=length_c*i+(g+1)+1
            D=randint(1,10)
            #print(A,B,C)
            if i+1!=width_c and map_p[i+1][g]!=[-1,-1]:
                graph[A].append([B,D])
                graph[B].append([A,D])

                g_c[A][B]=len(graph[A])-1
                g_c[B][A]=len(graph[B])-1
            if g+1!=length_c and map_p[i][g+1]!=[-1,-1]:
                graph[A].append([C,D])
                graph[C].append([A,D])

                g_c[A][C]=len(graph[A])-1
                g_c[C][A]=len(graph[C])-1

def map_draw_num():

    for i in range(width_c):
        for g in range(length_c):
            if map_p[i][g]==[-1,-1]:
                #map_draw_line()
                return
            cnt=0
            A=length_c*i+g+1
            if i+1!=width_c and map_p[i+1][g]!=[-1,-1]:
                #print("####",)
                text_pr(str(graph[A][cnt][1]),(map_p[i][g][0]+map_p[i+1][g][0])/2-10,(map_p[i][g][1]+map_p[i+1][g][1])/2,weight_size,color["black"])
                #pygame.draw.line(SURFACE,color["red"],map_p[i][g],map_p[i+1][g],3)
                cnt+=1

            if g+1!=length_c and map_p[i][g+1]!=[-1,-1]:
                text_pr(str(graph[A][cnt][1]),(map_p[i][g][0]+map_p[i][g+1][0])/2,(map_p[i][g][1]+map_p[i][g+1][1])/2-10,weight_size,color["black"])
                #pygame.draw.line(SURFACE,color["red"],map_p[i][g],map_p[i][g+1],3)
                cnt+=1
    #map_draw_line()

def map_draw_line():
    #print("!@#@!#@!")
    for i in range(width_c):
        chk=0
        for g in range(length_c):
            if map_p[i][g]==[-1,-1]:
                #print("#",i,g)
                if g!=0:
                    #print("@",i,map_p[i][0],map_p[i][g-1])
                    pygame.draw.line(SURFACE,color["red"],map_p[i][0],map_p[i][g-1],3)
                    chk=1
                    break

        if chk==0:
            #print("#",i,map_p[i][0],map_p[i][length_c-1])
            pygame.draw.line(SURFACE,color["red"],map_p[i][0],map_p[i][length_c-1],3)


    for i in range(length_c):
        chk=0
        for g in range(width_c):
            if map_p[g][i]==[-1,-1]:
                #print("##",g,i)
                if g!=0:
                    #print("@@",i,map_p[0][i],map_p[g-1][i])
                    pygame.draw.line(SURFACE,color["red"],map_p[0][i],map_p[g-1][i],3)
                    chk=1
                    break

        if chk==0:
            #print("##",i,map_p[0][i],map_p[width_c-1][i])
            pygame.draw.line(SURFACE,color["red"],map_p[0][i],map_p[width_c-1][i],3)

def map_draw_circle(ball_size):
    cnt=0
    for i in range(width_c):
        for g in range(length_c):
            cnt+=1
            if map_p[i][g]==[-1,-1]:return
            pygame.draw.circle(SURFACE,color["blue"],map_p[i][g],ball_size)
            text_pr(str(cnt),map_p[i][g][0],map_p[i][g][1],num_size,color["white"])

def Experiment():
    global score,map_p,distance,g_c,path,graph,q
    graph=[[]for i in range(node+1)]
    q = []
    path=[i for i in range(node+1)]
    distance = [inf]*(node+1)
    g_c=[[inf for i in range(node+1)]for g in range(node+1)]
    map_p=[[[-1,-1]for i in range(length_c+2)]for g in range(width_c+2)]
    map_produce(width_c,length_c,side_empty,n_distance,node)

    C1=Car(start,end,1)
    C2=Car(start,end,2)

    while 1:
        if randint(1,3)==1:
            for i in range(1,node+1):
                for g in range(1,node+1):
                    if g_c[i][g]!=inf:
                        graph[i][g_c[i][g]][1]=randint(1,10)
            
        SURFACE.fill(color["gray"])
        event = pygame.event.poll()
        if event.type == pygame.QUIT:break

        map_draw_num()
        map_draw_circle(ball_size)
        if C1.fh==0:
            C1.car_g()
            if C1.fh!=0:
                print("1. 처음에만 최단시간 계산 :",C1.time)
        if C2.fh==0:
            C2.car_g()
            if C2.fh!=0:
                print("2. 계속 최단시간 계산 :",C2.time)
        #print(C1.fh,C2.fh)

        if C1.fh!=0 and C2.fh!=0:
            score.append([C1.time,C2.time])
            return

        pygame.display.update()

score=[]
for i in range(30):
    print("######################")
    Experiment()

print(score)

b=[0,0,0]#1win,2win,draw
st_t=[]
for i in range(len(score)):
    if score[i][0]<score[i][1]:
        b[0]+=1
        st_t.append([abs(score[i][0]-score[i][1]),1])
    elif score[i][0]>score[i][1]:
        b[1]+=1
        st_t.append([abs(score[i][0]-score[i][1]),2])
    else:
        b[2]+=1
print("처음에만 최단시간 계산이 더 빠른 횟수 :",b[0])
print("계속 최단시간 계산이 더 빠른 횟수 :",b[1])
print("같은 횟수",b[2])
st_t.sort(reverse=True)
print(st_t)
print("1 = 처음에만 최단시간 계산이 더 빠른 횟수")
print("2 = 계속 최단시간 계산이 더 빠른 횟수")
#print("처음에만 최단시간 계산 :",Experiment(1))
#print("계속 최단시간 계산 :",Experiment(2))

# 가중치 랜덤 부여 말고도 차는 도로따라 이동하거나 멈추거나 하기때문에 인접한 노드들로 값이 분배 또는 삭제 되는 기능 추가 해서 테스트
