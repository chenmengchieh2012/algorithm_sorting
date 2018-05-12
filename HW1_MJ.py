# -*- coding: utf-8 -*-
"""
Created on Tue May  1 13:36:29 2018

@author: HeJiXiao

Algorithm
"""
from time import time
from random import randint,seed
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plot

# 在0~500隨機取整數
def random_number(quantity):
    
    num_list = []
    seed(time()) 
    for i in range(quantity):
        num_list.append(randint(0,500))
    return num_list

def bubble_sorted(data):
    
    new_list = list(data)
    list_len = len(new_list)
    for i in range(list_len - 1):
    	flag = False
        for j in range(list_len - 1, i, -1):
            if new_list[j] < new_list[j - 1]:
            	flag = True
                new_list[j], new_list[j - 1] = new_list[j - 1], new_list[j]
            if flag == False:
				break
    return new_list

def selection_sorted(data):
    
    for i in range(len(data)) :
        min_num = data[i]
        min_index = i
        for j in range(i,len(data)):
            if data[j] < min_num:
                min_num = data[j]
                min_index = j
        data[i] , data[min_index] = data[min_index] , data[i]
    return data

def insertion_sorted(data):
    
    for i in range(1,len(data)):
        temp = data[i]
        for j in range(i-1,-1,-1):
            if temp <= data[j]:
                data[j+1] = data[j]
                data[j] = temp
            else :
                break
        
    return data            

def quick_sorted(data):
    
    temp_data = data

    def partition(left , right):
        if right-left <=1:
            return
        pivot_value = temp_data[right-1]    
        p = left - 1
        for i in range(left,right):
            if temp_data[i] <= pivot_value:
                p += 1
                temp_data[i],temp_data[p] = temp_data[p],temp_data[i]
                
        partition(left,p)
        partition(p+1,right)
    
    partition(0,len(temp_data))
    return  temp_data

def heap_sorted(data):
    def swap(start , end) :
        root = start
        while True :
            child = root * 2 + 1 #left_child
            if child > end :
                break
            if child + 1 <= end and data[child] < data[child+1] :
                child+=1
            if data[root] < data[child] :
                data[root] , data[child] = data[child] , data[root]
                root = child
            else :
                break

    for start in range((len(data)-2)//2, -1, -1):
        swap(start, len(data)-1)
    
    for end in range(len(data)-1, 0, -1):
        data[0], data[end] = data[end],data[0]
        swap(0, end-1)
    return data
def calculate_time(sort):
    
    #N = [i for i in range(100,600,100)]
    N = [50000,100000,150000,200000,250000,300000]
    time_records = []
    for quantity in N:
        q = random_number(quantity) #亂數
        start = time()
        with ThreadPoolExecutor(max_workers=None) as excutor:
            for i in range(25):
                single_start_time = time()
                excutor.submit(sort(q[:]))
                single_end_time = time()
                single_total_time = single_end_time - single_start_time
                print('Sorting %s 數量 %d 第 %d 次 時間: %f'%(sort.__name__,quantity,i+1,single_total_time))
        end = time()
        time_records.append((end - start)/25)
    '''
        Log.w
        2018.05.11
        這裡拿不到excutor.result() 一直會有tyep_error
        不應該在這裡直接畫圖，須修正
    '''    
    drawing_plot(sort.__name__,time_records)
    return

def drawing_plot(sorting_name,times):
    
    x = [5,10,15,20,25,30]
    y = [time for time in times]
    
    plot.xlabel('quantity'+'\n'+'(10^4)')
    plot.ylabel('time'+'\n'+'second')
    plot.title(sorting_name)
    
    plot.plot(x,y,'-o')
    '''
        Log.i
        2018.05.11
        在Spyder 存下來的圖，跟在cmd跑所存下來的圖不一樣，不知道為什麼
    '''
    plot.savefig(sorting_name + '.png')
    plot.show(block=False)
    
if __name__ == '__main__':
    
    '''每個演算法 50000 100000 150000 200000 250000 300000
        每個亂數數量25次 求平均
    '''
    total_start = time()
    with ThreadPoolExecutor(max_workers=5) as excutor:
        # heap_time = excutor.submit(calculate_time(heap_sorted))
        bubble_time = excutor.submit(calculate_time(bubble_sorted))
        selection_time = excutor.submit(calculate_time(selection_sorted))
        insertion_time = excutor.submit(calculate_time(insertion_sorted))
        quick_time = excutor.submit(calculate_time(quick_sorted))
        
    total_end = time()
    print(total_end - total_start)
    '''drawing_plot('bubble_sorted',bubble_time.result())    
    drawing_plot('selection_sorted',selection_time.result())    
    drawing_plot('insertion_sorted',insertion_time.result())    
    drawing_plot('quick_sorted',quick_time.result())    
    drawing_plot('heap_sorted',heap_time.result())'''
    
    
            
    
