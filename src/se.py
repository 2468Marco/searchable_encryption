import os

def get_index():
    index = {}
    directory = '../data/files'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            print(filename)
            path = directory + '/' + filename
            f = open(path, "r")
            keywords = f.read()
            print (keywords)
            f.close()
            index[filename] = keywords
            continue
        else:
            continue
    print(index)
    return index

def invert_index(index):
    inverted_index = {}
    for txt in index:
        print(txt)
        keyword_list = index[txt].split(" ")
        for keyword in keyword_list:
            if (keyword not in inverted_index):
                temp_list = []
                temp_list.append(txt)
                inverted_index[keyword] = temp_list
                print(inverted_index)
                continue
            else:
                inverted_index[keyword].append(txt)
                print(inverted_index)
                continue
    return inverted_index
