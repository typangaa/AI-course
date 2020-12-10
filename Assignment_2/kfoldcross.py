from math import log
#from statistics import mode
import sys
from collections import Counter
#import matplotlib.pyplot as plt

def mode(list):
    data = Counter(list)
    mode_two = data.most_common(2) 
    if len(mode_two) < 2:
        return mode_two[0][0]
    if mode_two[0][1] == mode_two[1][1]:
        return "No unique mode"
    else:
        mode = mode_two[0][0]
    return mode

sys.setrecursionlimit(1000)

class TreeNode:
    def __init__(self,input_data):

        self.attr = None
        self.label = None
        self.splitval = None
        self.left = None
        self.right = None
        #self.data = input_data
        self.info_content = self.information_content(input_data)
    
    def print_chlid(self):
        if self.label != None:
            pass
            #print(f'this is label{self.label}')
        if self.attr!=None: 
            pass
            #print(f'this is att{self.attr}')
        if self.splitval!=None:
            pass
            #print(f'this is splitval{self.splitval}')
        if self.left!= None:
            #print('left')
            pass
            self.left.print_chlid()
        if self.right!= None:
            #print('right')
            pass
            self.right.print_chlid()
        
    def information_content(self, input):
        
        rating_list = ['AAA','AA','A','BBB','BB','B','CCC']
        count_rating = {'AAA': 0,
                        'AA' : 0,
                        'A'  : 0,
                        'BBB': 0,
                        'BB' : 0,
                        'B'  : 0,
                        'CCC'  : 0}
        
        ic = float(0)
        
        count_total = len(input)

        if input == []:
            return (ic, count_total)

        #print(count_rating)
        for rating in rating_list:
            count_rating[rating] = input.count(rating)
            c = float(count_rating[rating])/float(count_total)
            if c == 0:
                pass
            else:
                ic += -(c*log(c,2))

        #print(count_rating)
        #print(ic)

        return (ic, float(count_total))

    def information_gain(self,x,data_t,x_attr,split_val):

        #data_T = [list(z) for z in zip(*x)]
        data_left_label = [x[j][5] for j in range(len(data_t[x_attr])) if data_t[x_attr][j] <= split_val]
        data_right_label = [x[j][5] for j in range(len(data_t[x_attr])) if data_t[x_attr][j] > split_val]

        ic_left, count_left = self.information_content(data_left_label)
        ic_right, count_right = self.information_content(data_right_label)
        ic , count_total = self.information_content(data_t[5])

        #print(f'this is ic_right:{ic_right}')
        count_left = float(count_left)
        count_right = float(count_right)
        
        ic_gain = ic - (count_left/count_total)*ic_left - (count_right/count_total)*ic_right
        #print(f'this is ic gain{ic_gain}')
        
        return ic_gain

    def choose_split(self,x):
        bestgain = 0
        bestattr = 0
        bestspiltval = 0
        #splitval = []
        #print(x)
        len_N = len(x)
        #print(len_N)
        
        for attr in range(5):
            #print(x[attr])
            #x[attr].sort()
            x.sort(key=lambda x: x[attr])
            #self.sortby_inplace(x,attr)
            data_T = [list(z) for z in zip(*x)]
            for i in range(len_N-1):
                
                splitval = (data_T[attr][i] + data_T[attr][i+1])/float(2)
                gain = self.information_gain(x, data_T, attr, splitval)
                
                #print(f'this is attr:{attr} and val:{splitval} and gain:{gain}')
                if gain > bestgain:
                    bestattr = attr
                    bestspiltval = splitval
                    bestgain = gain
        #print(f'!!!!!!!!!!!!!!!!!!!!!this is battr and bval {bestattr},{bestspiltval}')
        #print(f'!!!!!!!!!!!!!!!!!!!!!this is bgain{bestgain}')
        return (bestattr,bestspiltval)

    def predict(n_node, data_set):
        x = data_set
        #print(n_node.attr)
        #print(x)
        while n_node.label == None:
            if x[n_node.attr] <= n_node.splitval:
                n_node = n_node.left
            else:
                n_node = n_node.right
            
        return n_node.label


    def DTL(self,data,minleaf):
        if data ==[]:
          n = TreeNode(data)
          return n
        boolean_check = False 
        len_N = len(data)
        data_T = [list(x) for x in zip(*data)]
        if len_N <= minleaf:
            boolean_check = True

        for i in range(len(data_T)):
            if len(set(data_T[i])) == 1:
                boolean_check = True
        
        if boolean_check == True:
            n = TreeNode(data)
            
            uni_mode = mode(data_T[len(data_T)-1])
                
            if uni_mode == "No unique mode":
                n.label = 'unknown'
            else:
                n.label = uni_mode
            
            return n
        attr , splitval = self.choose_split(data)
        #print(f'this is attr:{attr}')
        #print(f'this is splitval:{splitval}')
        
        n = TreeNode(data)
        n.attr = attr
        n.splitval = splitval
        
        #data_left_T = [data_T[j] for j in range(len(data[n.attr])) if data[n.attr][j] <= splitval]
        #data_right_T = [data_T[j] for j in range(len(data[n.attr])) if data[n.attr][j] > splitval]

        data.sort(key=lambda x: x[attr])
        #n.sortby_inplace(data,attr)

        data_T = [list(x) for x in zip(*data)]
        data_left = [data[j] for j in range(len(data_T[n.attr])) if data_T[n.attr][j] <= splitval]
        data_right = [data[j] for j in range(len(data_T[n.attr])) if data_T[n.attr][j] > splitval]

        
        n.left = self.DTL(data_left,minleaf)
        #print(f'this is data right:{data_right}')
        
        n.right = self.DTL(data_right,minleaf)
        return n

    def K_fold(self,data,k, h):
        len_N = len(data)
        len_M = len(h)
        Z = len_N/k
        Data_K = []
        data_temp = []
        avgerr_list = []
       
        lowest_avgerr = 1
        for m in range(len_M):
            accerr = 0
            for t in range(k):
                test_data = []
                train_data = []
                for i in range(len_N):
                    
                    start = int(t*Z)
                    end = int((t+1)*Z)
                    #print(start)
                    #print(end)
                    if i in range(start,end):
                        test_data.append(data[i])
                    else:
                        train_data.append(data[i])
                
                start = TreeNode(train_data)
                #print(h)
                n = start.DTL(train_data, h[m])
                count_true = 0
                #err = 0
                for j in range(len(test_data)):
                    if n.predict(test_data[j]) == test_data[j][5]:
                        
                        count_true += 1
                err = float(1) - float(count_true)/float(len(test_data))
                #print(err)
                accerr += err
            avgerr = accerr/k
            avgerr_list.append(avgerr)
            
            if lowest_avgerr > avgerr:
                lowest_avgerr = avgerr
                best_h = h[m]

        #plt.plot(h,avgerr_list)
        #plt.title('Average error versus minleaf')
        #plt.xlabel('minleaf')
        #plt.xticks(range(0,200,20))
        #plt.ylabel('average error(%)')
        #plt.savefig('crossval.png', bbox_inches='tight')
        
        return best_h

if __name__ == "__main__":

    train_txt = sys.argv[1]
    k_txt = sys.argv[2]
    minleaf_txt = sys.argv[3:]
    
    k = int(k_txt)
    min_leaf_list = [int(i) for i in minleaf_txt]
    
    f = open(train_txt,'r')

    WC_TA = []
    RE_TA = []
    EBIT_TA = []
    MVE_BVTD = []
    S_TA = []
    Rating = []
    #x = []
    count_N = 0

    next(f)

    for line in f:
        row = line.split()
        #x.append(row)
        WC_TA.append(float(row[0]))
        RE_TA.append(float(row[1]))
        EBIT_TA.append(float(row[2]))
        MVE_BVTD.append(float(row[3]))
        S_TA.append(float(row[4]))
        Rating.append(row[5])
        count_N += 1

    x_T = list([WC_TA,RE_TA,EBIT_TA,MVE_BVTD,S_TA, Rating])
    x = [list(z) for z in zip(*x_T)]
   
    start = TreeNode(x)
    print(start.K_fold(x,k,min_leaf_list))
  
    f.close()