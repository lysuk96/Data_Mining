import numpy as np
from numpy.core.fromnumeric import nonzero
import pandas as pd
from sklearn.model_selection import train_test_split
import sys
import math

'''
Longterm Project

Recommender System
Using Deep Learning

2016025732 Youngsuk Lee
'''

learning_rate = 1e-2
lambda_ = 0.005
epochs = 40
F = 3 # shape parameter / U = N * F / V = M * F / 


# Matrix Shape : R = N * M / U = N * F / V = M * F
R = None; R_train = None; R_valid = None; R_hat = None

N = None
M = None

def set_data(base_name):
    global N,M

    df = pd.read_csv(base_name, sep='\t', engine='python', encoding="cp949", header= None)
    del df[3]

    df = df.to_numpy()
    
    N = np.unique(df[:,0]).max()
    M = np.unique(df[:,1]).max()
    print(N, M)

    R = np.empty((N, M))
    for temp in df:
        R[temp[0]-1, temp[1]-1] = temp[2]
    
    return df

def split_data(df):
    df_train, df_valid = train_test_split(df, test_size=0.1)

    R_train = np.empty((N, M))
    for temp in df_train:
            R_train[temp[0]-1, temp[1]-1] = temp[2] #index 0부터 시작

    R_valid = np.empty((N, M))
    for temp in df_valid:
            R_valid[temp[0]-1, temp[1]-1] = temp[2] #index 0부터 시작

    return R_train, R_valid

def get_rmse(flag): 
    if flag : #True : train set, False : validation set
        xi, yi = R_train.nonzero()
    else :
        xi, yi = R_valid.nonzero()

    cost = 0
    for x, y in zip(xi, yi):
        if flag:
            cost += pow(R_train[x,y] - R_hat[x,y], 2)
        else:
            cost += pow(R_valid[x,y] - R_hat[x,y], 2)
    return np.sqrt(cost/len(xi))

def train(base_name):
    global R_train, R_valid, R_hat
    df = set_data(base_name)
    R_train, R_valid = split_data(df)

    U = np.random.rand(N,F)
    V = np.random.rand(M,F)

    users, items = R_train.nonzero()
    for epoch in range(epochs):
        for i, j in zip(users,items):
            error = R_train[i,j] - U[i].dot(V[j].T)
            U[i] -= learning_rate * (-error * V[j] + lambda_ * U[i])
            V[j] -= learning_rate * (-error * U[i] + lambda_ * V[j])
                                 
        R_hat = U.dot(V.T)
        rmse_train = get_rmse(True)
        rmse_valid = get_rmse(False)
        if(epoch % 5 == 4):
            print('---------epoch : %d--------'%(epoch+1))
            print('Train rmse : ', rmse_train)
            print('Valid rmse : ', rmse_valid)

        if(rmse_train + 0.1 < rmse_valid): #prevent overfitting
            print("Overfitting occured in epoch %d"%(epoch+1))
            break
        
    R_hat[R_hat < 1] = 1
    R_hat[R_hat > 5] = 5
    # print(R_hat)

def test(test_name):
    df_test = pd.read_csv(test_name, sep='\t', engine='python', encoding="cp949", header= None)
    del df_test[3]
    df_test = df_test.to_numpy()

    output_name = test_name.split(sep='.')[0] + '.base_prediction.txt'
    with open(output_name, 'w') as f:
        mse = 0
        for i in range(len(df_test)):
            user = df_test[i][0] - 1
            item = df_test[i][1] - 1

            # Exception Handling
            if user >= R_hat.shape[0]:
                predict = R_hat.mean(axis=item)
            elif item >= R_hat.shape[1]:
                predict = R_hat.mean()
            else:
                predict = R_hat[user, item]

            err = df_test[i][2] - predict
            mse += err * err
            line = str(user+1) + '\t' + str(item+1) + '\t' + str(predict) + '\n'
            f.write(line)
    mse /= df_test.shape[0]+1
    rmse = math.sqrt(mse)
    print('rmse for test data : ',rmse)

        
if __name__ == "__main__":    
    train(sys.argv[1])
    test(sys.argv[2])