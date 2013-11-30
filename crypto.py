#Licenced under the GNU General Public License. (V3)
#Designed and coded by caffeinemonster
#Copyright (2013) J. Green
#please read the licence.txt file for more information
import os, binascii, string, random, sys
from Crypto.Cipher import AES

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
    elif method == 2:
        strkey = binascii.b2a_hex(os.urandom(intdigits))[:intdigits]
        print(strkey)
        return strkey


def func_EncryptAES(key, strmessage):
    obj = AES.new(key, AES.MODE_CBC, IV)
    ciphertext = obj.encrypt(strmessage)
    return ciphertext


def func_DecryptAES(strkey, strencrypted):
    cipher = AES.new(strkey, AES.MODE_CBC, IV)
    strdecodedtext = cipher.decrypt(strencrypted)
    return strdecodedtext


def func_EncryptLayers(strmessage, keylist):
    for i in range(0, intKeys, 1):
        encryptedmessage = func_EncryptAES(keylist[i], strmessage)
        strmessage = encryptedmessage
    return strmessage


def func_DecryptLayers(strmessage, keylist):
    for i in range(intKeys, 0, -1):
        decryptedmessage = func_DecryptAES(myKeys[i - 1], strmessage)
        strmessage = decryptedmessage
    return strmessage


def func_SaveKeys(strfile, keylist, strIV):
    f = open(strfile, 'w')
    for i in range(0, intKeys, 1):
        f.write(keylist[i] + '\n')
    f.write(strIV + '\n')
    f.close()


def func_LoadKeys(strfile):
    keylist = [line.strip() for line in open(strfile)]
    return keylist


def func_PadMessage(strmessage, intblocksize):
    for i in range(0, len(strmessage) + intblocksize, intblocksize):
        if i >= len(strmessage):
            return strmessage.ljust(i)


def func_CharToBytes_rstr(strmessage):
    sreturn = 'ENC'
    for c in list(strmessage):
        sreturn += '-' + str(ord(c))
        #print chr(ord(c))
    return sreturn


def func_BytesToChar_rstr(strmessage):
    sreturn = ''
    for c in strmessage.split('-'):
        if c != 'ENC':
            sreturn += str(chr(int(c)))
    return sreturn

def func_GenerateKeyFile():
    myKeys = func_GenKeys(intKeys)
    IV = func_GenIV()
    func_SaveKeys('ENCDEC.key', myKeys, IV)
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
intKeys = 1024
myKeys = []
action = 0
intDoEncrypt = 0
intDoDecrypt = 1
intDoKeyList = 3

for i in range(0, len(sys.argv)):
    #print(('Argument:' + str(i) + sys.argv[i]))
    if sys.argv[i] == '-h':
        func_DisplayHelp()
        exit()
    elif sys.argv[i] == '-g':
        try:
            intKeys = int(sys.argv[i + 1])
        except IndexError:
            intKeys = 1024
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
    if len(myKeys) == 0:
        print('Error loading key file.')
        exit()

#set globals according to key file
intKeys = len(myKeys) - 1
IV = myKeys[len(myKeys) - 1]


if (action == intDoEncrypt):
    #encrypt message
    somemessage = func_EncryptLayers(somemessage, myKeys)
    print(('ENC(' + str(intKeys) + '):' + func_CharToBytes_rstr(somemessage)))
    exit()
elif (action == intDoDecrypt):
    #decrypt message
    somemessage = func_DecryptLayers(somemessage, myKeys)
    print(('DEC(' + str(intKeys) + '):' + somemessage))
    exit()
elif action == intDoKeyList:
    #output key
    for i in range(0, intKeys, 1):
        print((myKeys[i]))
    print(IV)
    exit()
