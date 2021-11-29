import numpy as np
from numpy.core.numeric import NaN
from numpy.lib.type_check import nan_to_num
import pandas as pd
import sys, time

from pandas.core.frame import DataFrame

'''
DBScan Algorithm

2016025732 YoungSuk Lee
'''

data_origin = None

input_name = None

def set_data():
    global data_origin

    df = pd.read_csv(input_name, sep='\t', engine='python', encoding="cp949", header=None)
    df.rename(columns={0:'index',1:'x', 2:'y',3:'cluster'},inplace=True)
    
    df['cluster'] = None # Class label 생성
    data_origin = df

def get_distance(point1, point2):
    x_change = data_origin.loc[point2, 'x'] - data_origin.loc[point1, 'x']
    y_change = data_origin.loc[point2, 'y'] - data_origin.loc[point1, 'y']

    return(np.sqrt(np.square(x_change)+ np.square(y_change)))

class DBScan():
    def __init__(self,n,eps,min_pts):
        self.n = int(n)
        self.eps = int(eps)
        self.min_pts = int(min_pts)

    def clustering(self):
        cluster_id = 0
        cluster_size = []
        for i in range(len(data_origin)):
            if data_origin.loc[i, 'cluster'] is None:
                flag = self.set_label(i, cluster_id) # flag : outlier detection
                if flag is not False :
                    cluster_size.append(flag)
                    print('cluster #'+str(cluster_id)+' labeled')
                    cluster_id += 1
        top_n_count = np.argsort(cluster_size)[-self.n:]
        print('Top n Cluster:\t', top_n_count)
        print('Each size:\t', np.sort(cluster_size)[-self.n:])

        return top_n_count
    
    def set_label(self, id, cluster_id):
        neighbors = self.get_neighbors(id)
        
        # Outlier setting / Outlier label(-1) can be changed anytime
        if len(neighbors) < self.min_pts :
            data_origin.loc[id, 'cluster'] = -1
            return False

        i = 0
        # Grow neighbors
        while(i< len(neighbors)):
            data_origin.loc[neighbors[i], 'cluster'] = cluster_id # Cluster label 삽입
            if len(self.get_neighbors(neighbors[i])) >= self.min_pts:
                neighbors += self.get_neighbors(neighbors[i])
                neighbors = list(dict.fromkeys(neighbors)) # 중복제거
            i+=1
        
        # print(neighbors)
        return len(neighbors)
        
    def get_neighbors(self,id):
        x = data_origin.loc[id,'x']
        y = data_origin.loc[id,'y']

        # 검사할 dataset 크기 줄이기
        x_min = x - self.eps
        x_max = x + self.eps
        y_min = y -self.eps
        y_max = y + self.eps
        tmp = list(np.where((x_min <=data_origin.to_numpy()[:,1]) & (data_origin.to_numpy()[:,1] <= x_max) & (y_min <= data_origin.to_numpy()[:,2]) & (data_origin.to_numpy()[:,2] <= y_max)))

        # distance > eps 인거 빼기
        to_remove = []
        for candidate in tmp :
            to_remove = list(np.where(get_distance(id, candidate) > self.eps))
        tmp = np.delete(tmp, to_remove)

        return list(tmp)

    def print_output(self, top_n_label):
        print(data_origin)
        for i in range(len(top_n_label)):
            output = DataFrame(data_origin[data_origin['cluster']==top_n_label[i]].index)
            output_name = input_name.split(sep='.')[0] + '_cluster_' + str(i) + '.txt'
            output.to_csv(output_name, index=False, sep='\n', header=False)

if __name__=='__main__':
    input_name = sys.argv[1]

    set_data()
    dbScan= DBScan(n= sys.argv[2], eps= sys.argv[3], min_pts= sys.argv[4])

    t1 = time.time()
    top_n_label = dbScan.clustering()
    t2 = time.time()
    
    dbScan.print_output(top_n_label)
    print('Clustering time : ',t2-t1)