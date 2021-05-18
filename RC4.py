"""
Decrypts a stream of bytes, maintaining an internal state.
"""

class RC4:

	def __init__(self, key):

		self.key = key
		self.reset()

	""" every time you enter a new map, reset ciphers"""
	def reset(self):

		self.S = list(range(256))
		j = 0

		for i in range(256):
			j = j + self.S[i] + self.key[i % len(self.key)] & 255
			tmp = self.S[i]
			self.S[i] = self.S[j]
			self.S[j] = tmp

		self.i = 0
		self.j = 0



	def encrypt(self, data):

		for idx in range(len(data)):

			self.i = self.i + 1 & 255
			self.j = self.j + self.S[self.i] & 255
			tmp = self.S[self.i]
			self.S[self.i] = self.S[self.j]
			self.S[self.j] = tmp;

			data[idx] = data[idx] ^ self.S[tmp + self.S[self.i] & 255]		

	def decrypt(self, data):
		self.encrypt(data)
