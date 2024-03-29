import os
import ast
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

### INDEX CREATION AND MANIPULATION 
def get_index():
    index = {}
    directory = '../data/files'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            path = directory + '/' + filename
            f = open(path, "r")
            keywords = f.read()
            f.close()
            index[filename] = keywords
            continue
        else:
            continue
    return index

def invert_index(index):
    inverted_index = {}
    for txt in index:
        for keyword in index[txt]:
            if (keyword not in inverted_index):
                temp_list = []
                temp_list.append(txt)
                inverted_index[keyword] = temp_list
                continue
            else:
                inverted_index[keyword].append(txt)
                continue
    return inverted_index


### KEY GENERATION FUNCTIONS
#key_make takes in a integer and returns a hexidecimal string with the same length
def key_make(key_length):
        #Gets a hexidecimal that uses the number of bytes given)
        key=get_random_bytes(key_length)
        #print(key.hex())
        return key.hex()

#key_save saves the key inputed to the file key.txt
def key_save(key,file):
        f = open(file,"w+")
        f.write(key)
        f.close

#keyGen creates 2 'l' bit key and then saves them to skprf.txt and skaes.txt
#'l' should be 16,24,32
def keys_gen(length):
        key = key_make(length)
        print("PRF KEY: "+key)
        key_save(key,"../data/skprf.txt")
        key = key_make(length)
        print("AES KEY: "+key)
        key_save(key,"../data/skaes.txt")


### STRING MANIPULATION
#converts strings to hexadecimal format
def strToHex(string):
        binary_string = ""
        for x in string:
                one_letter_ASCII = ord(x)
                one_letter_binary = bin(one_letter_ASCII)
                one_letter_binary = one_letter_binary[2::]
                #Padding front zeros
                while (len(one_letter_binary) != 8):
                        one_letter_binary = "0"+one_letter_binary
                binary_string += one_letter_binary
        hex_string = hex(int(binary_string,2))
        return hex_string[2::]

def enc():
    
    iv = bytes
    iv = b'.$\xc7\x98\x84&\x9d\xf8(c\xfe\xb0K\xef\xeb\x06'
        
    #get the plaintext index
    index = get_index()

    #get skprf
    f = open("../data/skprf.txt","r")
    if f.mode == "r":
        sk = f.read()
        #print("secret key prf:    "+sk)
    f.close()
    prfKey = bytes
    prfKey = prfKey.fromhex(sk)

    #get skaes
    f = open("../data/skaes.txt","r")
    if f.mode == "r":
        sk = f.read()
        #print("secret key aes:    "+sk)
    f.close()
    aesKey = bytes
    aesKey = aesKey.fromhex(sk)

    ## make ciphers
    #keywords cipher
    prfCipher = AES.new(prfKey,AES.MODE_ECB)
    #files cipher
    aesCipher = AES.new(aesKey,AES.MODE_CBC, iv)

    #preperation for indexing
    byteText = bytes
    encIndex = {}
    i=0

    #for every document in the plaintext index
    for doc in index:
        #encrypting the file text
        #generate filename/path
        i+=1
        fileName = "c"+str(i)+".txt"
        #NOTE THE FOLDER 'ciphertextfiles' MUST BE PREEXISTING
        filepath = "../data/ciphertextfiles/"+fileName

        #encrypting the file
        f = open(filepath,"w")
        encFileText = encString(aesKey, index[doc])
        f.write(encFileText)
        f.close()

        #encrypting the keywords
        keyword_list = index[doc].split(" ")
        encIndex[fileName] = []
        for keyword in keyword_list:
            hexText = strToHex(keyword)
            byteText = byteText.fromhex(hexText)
            padmsg = pad(byteText,16)
            wordEnc = prfCipher.encrypt(padmsg)
            #print(wordEnc.hex())
            encIndex[fileName].append(wordEnc.hex())
    #inverting the encrypted index
    invertedEncIndex = invert_index(encIndex)
    f = open("../data/index.txt","w")
    f.write(str(invertedEncIndex))
    f.close()
    print(index)
    print(invertedEncIndex)

def gen_tok(keyword):
    byteText = bytes
    f = open("../data/skprf.txt","r")
    prfCipher = AES.new(byteText.fromhex(f.read()),AES.MODE_ECB)
    f.close
    hexText = strToHex(keyword)
    byteText = byteText.fromhex(hexText)
    padmsg = pad(byteText,16)
    wordEnc = prfCipher.encrypt(padmsg)
    token = wordEnc.hex()
    f = open("../data/token.txt","w+")
    f.write(token)
    f.close
    print(token)
    return token

def search():    
    #get skaes
    f = open("../data/skaes.txt","r")
    if f.mode == "r":
        sk = f.read()
        #print("secret key aes:    "+sk)
    f.close()
    aesKey = bytes
    aesKey = aesKey.fromhex(sk)
    f = open("../data/index.txt","r")
    dic = {}
    dic = ast.literal_eval(f.read())
    f.close()
    f = open("../data/token.txt","r")
    token = f.read()
    f.close
    for pair in dic:
        if pair == token:
            list_of_enc_files = dic[pair]
            print(list_of_enc_files)
    with open("../result.txt", "w+") as r:
        for text_file in list_of_enc_files:
            file_path = '../data/ciphertextfiles/'+text_file
            f = open(file_path,'r')
            enc_word = f.read()
            f.close
            decWord = dec(aesKey, enc_word)
            print(text_file +'  '+decWord)
            r.write(text_file +'  '+str(decWord)+'\n')
        r.close

def dec(key, ct):
    iv = bytes
    iv = b'.$\xc7\x98\x84&\x9d\xf8(c\xfe\xb0K\xef\xeb\x06'

    ciphertext = bytes
    ciphertext = ciphertext.fromhex(ct)

    #create a cipher with the key and iv
    cipher = AES.new(key, AES.MODE_CBC, iv)

    #decrypt the ciphertext
    data = cipher.decrypt(ciphertext)

    #unpad the extra bytes from the decrypted ciphertext and format it
    finalmsg = str(unpad(data,16))[2:-1]
    return finalmsg

def encString(sk, pt):
    #make a bytes object to hold the key value
    key = bytes
    key = sk

    #the encrypt funciton does not use 'str' objects so it is nessassary to change it to hex format
    hexText = strToHex(pt)
    byteText = bytes
    byteText = byteText.fromhex(hexText)

    #create the iv
    iv = bytes
    iv = b'.$\xc7\x98\x84&\x9d\xf8(c\xfe\xb0K\xef\xeb\x06'

    #create the cipher using the key and the iv
    cipher = AES.new(key, AES.MODE_CBC, iv)

    #pad the message so that it fills the block
    padmsg = pad(byteText,16)

    #encrypt the message
    msg = cipher.encrypt(padmsg)

    return msg.hex()
gen_tok("packers")
