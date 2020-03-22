#One time pad cracker
import base64


def main():
	f = open("ciphertext.txt","r+")

	SPACE = ord(' ')	
	cracked = []
	for i in range(350):
		cracked.append("Unknown")
	
	contents = f.read()
	ciphertexts = contents.split("\n")

	cleartexts = [None] * len(ciphertexts)
	for idx,c in enumerate(cleartexts):
		cleartexts[idx] = [None] * 350
		

	for idx, c in enumerate(ciphertexts): 
		contents = base64.b64decode(c)
		ciphertexts[idx] = contents

	#key = bytearray(b'?' * 350)
	f = open('key.txt', 'r+b')
	key = bytearray(f.read())
	print(len(key))
	f.close()
	
	for k in range(max(len(key) for c in ciphertexts)):
		cts = [c for c in ciphertexts if len(c) > k]
		guess = ord('?') #holds guess for current key char
			
		for curs1 in range(len(cts)):
			for curs2 in range(len(cts)):
						
				if curs2 == curs1:
					continue
				
				xor = cts[curs1][k] ^ cts[curs2][k]
				
				if 0 < xor < 65:
					guess = ord('?')
					break
 
				guess = SPACE
			
			if guess == SPACE: #we can use the space to recover one key char and decrypt the whole column!
				print(k, max(len(c) for c in ciphertexts))
				x = cts[curs1][k] ^ SPACE
				key[k] = x
				cracked[k] = "Yes"
				break


	indexOfClear = 217
	#45
	key[0] = 193
	key[1] = 237
	key[2] = 230
	key[5] = 130
	key[26] = 200


	#Decode messages
	for k in range(len(key)):					#for each letter in key (350)
		for curs in range(len(cleartexts)):			#for each message (2)	
			if len(ciphertexts[curs]) > k:			#if length of clear[0..1] > [0..350]
				cleartexts[curs][k] = key[k] ^ ciphertexts[curs][k]	# clear[0..1][0..350] = xor

	txt = []

	for idx,c in enumerate(cleartexts[indexOfClear]):
		if c != None:
			print(str(idx) + ":", "\tClear:", chr(c), "\tClearInt:", c, "\tCiph:", ciphertexts[indexOfClear][idx], "\tKey:", key[idx], "\t",cracked[idx])
			txt.append(chr(c))


	f = open('keyout.txt', 'w+b')
	binary_format = bytearray(key[0:320])
	f.write(binary_format)
	f.close()
	
	'''l = []
	minN = 255
	maxN = 0
	minIdx = 0
	maxIdx = 0
	for i in range(len(ciphertexts)):
		if(ciphertexts[i][0] > maxN):
			maxN = ciphertexts[i][2]
			maxIdx = i
		if(ciphertexts[i][0] < minN):
			minN = ciphertexts[i][2]
			minIdx = i	
		l.append(ciphertexts[i][2])
	#print( "Min:", minN, minIdx, "Max:", maxN, maxIdx)
	'''


if __name__ == "__main__":
	main()