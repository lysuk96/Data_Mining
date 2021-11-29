import itertools, time, sys

global input_file, output_file

data_set=[] #TBD

check_set=set([]) #Cn
item_set={} # Ln / Hashmap <-> set 기능 번갈아가며 사용
result_set={} # as a dictionary to make association rule, support, confidence

min_support = 0 #default

def handle_input():
    global min_support, input_file, output_file
    min_support = int(sys.argv[1]) # initialize min_support
    input_file = sys.argv[2]
    output_file = sys.argv[3]    

# 'input.txt to DataSet'
def setting_data_set():
    global data_set, min_support
    with open(input_file, 'r') as f:
        for line in f:
            data_set.append(list(map(int,line.replace('\n','').split('\t'))))
    min_support = min_support * len(data_set) / 100

'''
Put and Count every element using Dictionary (format : frozenset)
Input : TDB (data_set)
Output : L1 (item_set)
'''
def first_scan():
    for i in range(0, len(data_set)):
        for data in data_set[i]:
            temp = frozenset([data])
            if temp in item_set:
                item_set[temp] += 1
            else :
                item_set[temp] = 1
    # Compare every elements if it's bigger than the min_support
    compare_min_support(item_set)
    print('first item set')
    print(item_set)

    result_set.update(item_set)

'''
Count Cn elements and compare
Input : Cn (check_set)
Output : Ln (new item_set, result_set)
'''
def scan():
    global item_set, check_set
    item_set.clear()

    for data in data_set :
        for check in check_set :
            if check <= frozenset(data):
                if check in item_set:
                    item_set[check] += 1
                else :
                    item_set[check] = 1
    compare_min_support(item_set)

    print("\nnext item set")
    print(item_set)
    result_set.update(item_set)

'''
Filtering the elements by comparing with min_support
'''
def compare_min_support(_dict):
    temp = []
    for item in _dict:
        if _dict[item] < min_support:
            temp.append(item)
    for i in range(0, len(temp)):
        del(_dict[temp[i]])

'''
Join the sets and filter bt length and subsets
Input : Ln (item_set)
Output : C(n+1) (check_set)
'''
def to_next_set(length):
    global item_set, check_set
    keys = list(item_set.keys())
    print('keys')
    print(len(keys))
    
    temp_set = set([])
    
    num = 0
    for i in range(0, len(keys)-1):
        for j in range(i+1, len(keys)):
            num+=1
            temp = keys[i].union(keys[j])
            # Check if the length is right and its subsets all exist
            if (len(temp) == length and get_subsets(temp, length-1) <= frozenset(keys)):
                temp_set.add(temp)

    check_set = temp_set

'''
Get all the subsets from the set
'''
def get_subsets(_set, length):
    temp = frozenset(frozenset(item) for item in itertools.combinations(_set,length))
    return temp

'''
Get and print all the association rule using result_set
'''
def apply_association_rule(_set):
    with open(output_file, 'w') as f:
        
        for items in _set:
            if len(items) != 1:
                for i in range(1, len(items)):
                    temp_set = get_subsets(items, i)
                    for item in temp_set:
                        counterpart = items - item
                        support = '%0.2f' %round(float(_set[items])/float(len(data_set))*100,2)
                        confidence =  '%0.2f' %round(float(_set[items])/float(_set[item])*100, 2)
                        line = str(set(item))+ '\t' + str(set(counterpart)) + '\t' + str(support)+ '\t' + str(confidence) +'\n'
                        f.write(line)
        f.close()


if __name__ == '__main__' :
    t1 = time.time()

    handle_input()
    setting_data_set() #TDB
    first_scan() #L1, C1
    length = 2
    while(item_set != {}):
        to_next_set(length) #Ln -> C(n+1)
        scan() #C(n+1) -> L(n+1)
        length+=1

    apply_association_rule(result_set)

    t2 = time.time()
    print("\nTime")
    print(t2-t1) # Time check
