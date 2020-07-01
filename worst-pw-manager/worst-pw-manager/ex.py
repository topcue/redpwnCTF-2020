import itertools
import string
import pathlib
import binascii
import os

from Crypto.Cipher import ARC4

ALPHABET = string.ascii_lowercase + "_"

flag = itertools.cycle(bytearray(open("flag.txt").read().strip(), "utf-8"))

class KeyByteHolder(): # im paid by LoC, excuse the enterprise level code
	def __init__(self, num):
		assert num >= 0 and num < 256
		self.num = num

	def __repr__(self):
		return hex(self.num)[2:]

def rc4(text, key): # definitely not stolen from stackoverflow
	S = [i for i in range(256)]
	j = 0
	out = bytearray()
	
	#KSA Phase
	for i in range(256):
		j = (j + S[i] + key[i % len(key)].num) % 256
		S[i] , S[j] = S[j] , S[i]

	#PRGA Phase
	i = j = 0
	for char in text:
		i = ( i + 1 ) % 256
		j = ( j + S[i] ) % 256
		S[i] , S[j] = S[j] , S[i]
		out.append(ord(char) ^ S[(S[i] + S[j]) % 256])
	return out

def take(iterator, count):
    return [next(iterator) for _ in range(count)]

def generate_key():
	key = [KeyByteHolder(0)] * 8 # TODO: increase key length for more security?
	#print("[*] key : ", end="")
	for i, c in enumerate(take(flag, 8)): # use top secret master password to encrypt all passwords    
		key[i].num = c
		#print(chr(c), end="")
	#print("")
	print("[*] key :", chr(key[0].num)*8)

	return key

def get_dic():
	path = "../passwords"
	file_list = os.listdir(path)
	dic = {}
	for file_name in file_list:
		file_name = file_name[:-4]    
		idx = file_name.split('_')[0]
		name = file_name.split('_')[1]
		dic[int(idx)] = name
	dic = sorted(dic.items())

	return dic


def main(args):
	dic = get_dic()
	pathlib.Path("./passwords").mkdir(exist_ok=True)
	
	passwords = open("passwords.txt").read()
	for pw_idx, password in enumerate(passwords.splitlines()):
		plain_list = [ord(x) for x in password]
		masked_file_name = "".join([chr((((c - ord("0") + i) % 10) + ord("0")) * int(chr(c) not in string.ascii_lowercase) + (((c - ord("a") + i) % 26) + ord("a")) * int(chr(c) in string.ascii_lowercase)) for c, i in zip([ord(a) for a in password], range(0xffff))])
		
		tmp = dic[pw_idx][0]

		if tmp == 10:
			for i in range(4, 10):
				print("=" * 30)
				pw_idx += 1
				generate_key()
		elif tmp == 100:
			for i in range(39, 100):
				print("=" * 30)
				pw_idx += 1
				generate_key()

		real_idx = tmp
		
		print("=" * 30)
		
		f_cipher = open("../passwords/" + str(real_idx) + "_" + masked_file_name + ".enc", "rb")
		cipher = f_cipher.read()
		cipher_list = [x for x in cipher]

		f = open("passwords/" + str(real_idx) + "_" + masked_file_name + ".enc", "wb")
		out = rc4(password, generate_key())
	
		print("[*] pwd :", binascii.hexlify(cipher))
		print("[*] out :", binascii.hexlify(out))
		
		f.write(out)
		f.close()
		f_cipher.close
		if real_idx == 1:
			exit()	

if __name__ == "__main__":
	import sys
	main(sys.argv)

# EOF
