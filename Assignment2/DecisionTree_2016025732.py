import numpy as np
import pandas as pd
import sys

'''
Decision Tree 
Using Gain Ratio

2016025732 YoungSuk Lee
'''

class Node():
    def __init__(self):
        self.criteria_attribute = None
        self.label_predict = None
        self.leaf = {} # key : attribute value, value: leaf node pointer

    def add(self, attribute_value, node):
        self.leaf[attribute_value] = node

    def is_leaf(self):
        if len(self.leaf)==0 :
            return True
        return False

class DecisionTree():
    def __init__(self):
        self.root = Node()

        self.df_train = None
        self.df_test = None

        self.attribute = [] # (ex. age, income, etc..)
        self.label_name = None # (ex. buy_computer)
        self.label_value = [] # label_name으로 구분한 row (ex. no, yes)

    def set_data(self, arg1, arg2):
        self.df_train = pd.read_csv(arg1, sep='\t', engine='python', encoding="cp949")
        self.df_test = pd.read_csv(arg2, sep='\t', engine='python', encoding="cp949")
        self.attribute = self.df_train.columns.tolist()
        self.label_name = self.attribute[self.df_train.shape[1]-1]
        del self.attribute[self.df_train.shape[1]-1]

        self.label_value = self.df_train.groupby(self.label_name)[self.label_name].count().index.tolist()
        
    def train_data(self):
        self.grow_tree(self.root, self.df_train)

    def grow_tree(self, node, data):

        # Predict label by majority voting
        label, counts = np.unique(data[self.label_name], return_counts=True)
        node.label_predict = label[np.argmax(counts)]

        if self.is_homogenius(data):
            return

        best_attribute = self.get_best_attribute(data)

        # Set criteria attribute
        node.criteria_attribute = best_attribute
        attribute_value = np.unique(data[best_attribute])

        # Recursively grow
        for i in range(len(attribute_value)):
            node.add(attribute_value[i], Node())
            _data = data.get(data[best_attribute]==attribute_value[i]) #해당 attribute에서 같은 value만 가진 data select
            _data = _data.drop(best_attribute, axis=1) #해당 attribute행 삭제
            self.grow_tree(node.leaf[attribute_value[i]], _data)


    def is_homogenius(self, data):
        if len(np.unique(data[self.label_name])) == 1:
            return True
        return False

    def get_best_attribute(self, data):
        temp = 0
        best_attribute = None
        temp_attribute = data.columns.tolist()
        del temp_attribute[-1] #Class label은 제외

        for i in range(len(temp_attribute)):
            gain = self.info(data) - self.expected_info(data, temp_attribute[i])
            gain_ratio = gain / self.split_info(data, temp_attribute[i])
            if temp < gain_ratio:
                temp = gain_ratio
                best_attribute = temp_attribute[i]

        return best_attribute


    def info(self, data):
        value, counts = np.unique(data[self.label_name], return_counts=True)
        temp = 0
        for i in range(len(value)):
            temp += counts[i]/np.sum(counts)*np.log2(counts[i]/np.sum(counts))
        return -temp
    
    def expected_info(self, data, attribute):
        value, counts = np.unique(data[attribute], return_counts=True)

        temp=0
        for i in range(len(value)):
            _data = data.get(data[attribute]==value[i])
            temp += counts[i]/np.sum(counts) * self.info(_data)
        return temp

    def split_info(self, data, attribute):
        value, counts = np.unique(data[attribute], return_counts=True)
        temp = 0
        for i in range(len(value)):
            temp += counts[i]/np.sum(counts) * np.log2(counts[i]/np.sum(counts))
        return -temp

    def test_data(self):
        self.df_test[self.label_name] = None
        for i in range(len(self.df_test)):
            self.df_test[self.label_name].iloc[i] = self.predict(self.df_test.iloc[i])

    def predict(self, data):
        node = self.root
        while(node.is_leaf() == False):
            try:
                node = node.leaf[data[node.criteria_attribute]]
            except:
                return node.label_predict
        return node.label_predict
        
    def print_output(self, arg3):
        self.df_test.to_csv(arg3, index=False, sep='\t')

    

if __name__ == '__main__' :
    tree = DecisionTree()
    tree.set_data(sys.argv[1], sys.argv[2])
    tree.train_data()
    tree.test_data()
    tree.print_output(sys.argv[3])