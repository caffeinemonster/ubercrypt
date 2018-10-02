#Licenced under the GNU General Public License. (V3)
#Designed and coded by caffeinemonster
#please read the licence.txt file for more information
import os
import binascii
import string
import random
import sys
from Crypto.Cipher import AES


def func_GenIVs(intAmount):
    print('Generating keys!')
    arrIVs = [None] * (intAmount + 1)
    for i in range(0, intAmount + 1):
        arrIVs[i] = func_GenIV()
    return arrIVs


def func_GenIV():
    return func_GenKey(16, 1)


def func_GenKeys(intAmount):
    print('Generating keys!')
    arrKeys = [None] * (intAmount + 1)
    for i in range(0, intAmount + 1):
        arrKeys[i] = func_GenKey(32, 1)
    return arrKeys


def func_GenKey(intdigits, method):
    if method == 1:
        oList = [random.choice(string.ascii_letters + string.digits) for n in range(intdigits)]
        strkey = "".join(oList)
        print (strkey)
        return strkey
    elif method == 2:  # shit do not use
        strkey = binascii.b2a_hex(os.urandom(intdigits))[:intdigits]
        print(strkey)
        return strkey


def func_EncryptAES(key, strmessage, strIV):
    obj = AES.new(key, AES.MODE_CBC, strIV)
    ciphertext = obj.encrypt(strmessage)
    return ciphertext


def func_DecryptAES(strkey, strencrypted, strIV):
    cipher = AES.new(strkey, AES.MODE_CBC, strIV)
    strdecodedtext = cipher.decrypt(strencrypted)
    return strdecodedtext


def func_EncryptLayers(strmessage, keylist, ivlist):
    for i in range(0, intKeys, 1):
        encmsg = func_EncryptAES(keylist[i], strmessage, ivlist[i])
        strmessage = encmsg
    return strmessage


def func_DecryptLayers(strmessage, keylist, ivlist):
    for i in range(intKeys, 0, -1):
        decmsg = func_DecryptAES(myKeys[i - 1], strmessage, ivlist[i - 1])
        strmessage = decmsg
    return strmessage


def func_SaveKeys(strfile, keylist, ivlist):
    f = open(strfile, 'w')
    for i in range(0, intKeys, 1):
        f.write(keylist[i] + '\n')
    for i in range(0, intKeys, 1):
        f.write(ivlist[i] + '\n')
    f.close()


def func_LoadKeys(strfile):
    keylist = [line.strip() for line in open(strfile)]
    return keylist


def func_LoadIVs(strfile):
    intCount = 1
    myIVs = []
    with open(strfile) as f:
        content = f.readlines()
        for s in content:
            if intCount > (intKeys):
                myIVs.append(s.rstrip())
            intCount += 1
    return myIVs


def func_PadMessage(strmessage, intblocksize):
    for i in range(0, len(strmessage) + intblocksize, intblocksize):
        if i >= len(strmessage):
            return strmessage.ljust(i)


def func_CharToBytes_rstr(strmessage):
    strreturn = 'ENC'
    for c in list(strmessage):
        strreturn += '-' + str(ord(c))
        #print chr(ord(c))
    return strreturn


def func_BytesToChar_rstr(strmessage):
    strreturn = ''
    for c in strmessage.split('-'):
        if c != 'ENC':
            strreturn += str(chr(int(c)))
    return strreturn


def func_GenerateKeyFile():
    myKeys = func_GenKeys(intKeys)
    #IV = func_GenIV()
    myIVs = func_GenIVs(intKeys)
    func_SaveKeys('ENCDEC.key', myKeys, myIVs)
    print(('Generated keys. (' + str(intKeys) + ')'))
    print(('Saved to file: ENCDEC.key'))
    print(('Carefully share this file.'))


def func_DisplayHelp():
    print('')
    print('Help:')
    print(('-h Displays this help screen\n'))
    print(('-g # Generate keys'))
    print(('example:    python ' + sys.argv[0] + ' -g 2056'))
    print(('example:    python ' + sys.argv[0] + ' -g\n'))
    print(('-k Output key to screen'))
    print(('example:    python ' + sys.argv[0] + ' -k'))
    print(('example:    python ' + sys.argv[0] + ' -k > backup.key\n'))
    print(('Restore a key file'))
    print(('example:    cat backup.key > ENCDEC.key\n'))
    print(('-e "message" Encrypt message'))
    print(('example:    python ' + sys.argv[0] + ' -e "Top secret message."\n'))
    print(('-d ENC-XXX-XXX Decrypt message'))
    print(('example:    python ' + sys.argv[0] + ' -d ENC-XXX-XXX-XXX-XXX-...'))
    print(('example:    python ' + sys.argv[0] + ' -d ENC-12-132-214-61-...\n'))


if len(sys.argv) == 1:
    print('No data to encrypt / decrypt exiting application')
    func_DisplayHelp()
    print('')
    exit()

#declare globals
intKeys = 16
myKeys = []
myIVs = []
action = 0
intDoEncrypt = 0
intDoDecrypt = 1
intDoKeyList = 2

for i in range(0, len(sys.argv)):
    if sys.argv[i] == '-h':
        func_DisplayHelp()
        exit()

    elif sys.argv[i] == '-g':
        try:
            intKeys = int(sys.argv[int(i + 1)])
        except IndexError:
            intKeys = 16
        print(('Generating keys. (' + str(intKeys) + ')'))
        #generate keyfile
        func_GenerateKeyFile()
        exit()

    elif sys.argv[i] == '-e':
        try:
            somemessage = func_PadMessage(sys.argv[i + 1], 16)
            action = intDoEncrypt
        except IndexError:
            print('No data to encrypt.')
            exit()

    elif sys.argv[i] == '-d':
        try:
            somemessage = func_BytesToChar_rstr(sys.argv[i + 1])
            action = intDoDecrypt
        except ValueError:
            print('Encryption format appears incorrect.')
            exit()
        except IndexError:
            print('No data to decrypt.')
            exit()

    elif sys.argv[i] == '-k':
        action = intDoKeyList

#check to see if a key file exists
if not os.path.isfile('ENCDEC.key'):
    func_GenerateKeyFile()

#if the keys havent just been generated then load them
if len(myKeys) == 0:
    myKeys = func_LoadKeys('ENCDEC.key')
    intKeys = int(len(myKeys) / 2)
    myIVs = func_LoadIVs('ENCDEC.key')
    if len(myKeys) == 0:
        print('Error loading key file.')
        exit()
#calculate the amount of keys generated / loaded
intKeys = int(len(myKeys) / 2)

#performa action
if (action == intDoEncrypt):
    #encrypt message
    somemessage = func_EncryptLayers(somemessage, myKeys, myIVs)
    print((func_CharToBytes_rstr(somemessage)))
    exit()

elif (action == intDoDecrypt):
    #decrypt message
    somemessage = func_DecryptLayers(somemessage, myKeys, myIVs)
    print(('DEC(' + str(intKeys) + '):' + somemessage))
    exit()

elif action == intDoKeyList:
    #output key
    for i in range(0, intKeys, 1):
        print((myKeys[i]))
    for i in range(0, intKeys, 1):
        print((myIVs[i]))
    exit()
