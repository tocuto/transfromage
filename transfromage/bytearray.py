class ByteArray(object):
	def __init__(self, stack = b""):
		self.stack = stack
	
	def writeByte(self, *byte):
		self.stack += bytes(map(lambda n: int(n % 256), [*byte]))
		return self
	
	def writeShort(self, short):
		short = int(short)
		return self.writeByte((short >> 8) & 255, short & 255)
	
	def writeInt(self, integer):
		integer = int(integer)
		return self.writeByte((integer >> 16) & 255, (integer >> 8) & 255, integer & 255)
	
	def writeLong(self, long):
		long = int(long)
		return self.writeByte((long >> 24) & 255, (long >> 16) & 255, (long >> 8) & 255, long & 255)
	
	def writeUTF(self, utf):
		if type(utf) == str:
			utf = utf.encode()
		
		self.writeShort(len(utf))
		self.stack += utf
		
		return self
	
	def writeBigUTF(self, big_utf):
		if type(big_utf) == str:
			big_utf = big_utf.encode()
		
		self.writeInt(len(big_utf))
		self.stack += big_utf
		
		return stack
	
	def writeBool(self, boolean):
		self.writeByte(boolean)
		return self
	
	def readByte(self, bytesQuantity = 1):
		byteStack = self.stack[:bytesQuantity]
		self.stack = self.stack[bytesQuantity:]
		
		byteStack += b"\x00" * (bytesQuantity - len(byteStack))
		
		return byteStack if len(byteStack) != 1 else byteStack[0]
	
	def readShort(self):
		shortStack = self.readByte(2)
		return (shortStack[0] << 8) + shortStack[1]
	
	def readInt(self):
		intStack = self.readByte(3)
		return (intStack[0] << 16) + (intStack[1] << 8) + intStack[2]
	
	def readLong(self):
		longStack = self.readByte(4)
		return (longStack[0] << 24) + (longStack[1] << 16) + (longStack[2] << 8) + longStack[3]
	
	def readUTF(self):
		byte = self.readByte(self.readShort())
		
		if type(byte) == int:
			return chr(byte)
		return byte.decode()
	
	def readBigUTF(self):
		byte = self.readByte(self.readInt())
		
		if type(byte) == int:
			return chr(byte)
		return byte.decode()
	
	def readBool(self):
		return self.readByte() == 1