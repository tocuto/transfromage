from .bytearray import ByteArray

import base64
import hashlib

salt = "".join(map(chr, [
	247,  26, 166, 222, 143,  23, 118, 168,
	  3, 157,  50, 184, 161,  86, 178, 169,
	 62, 221,  67, 157, 197, 221, 206,  86,
	211, 183, 164,   5,  74,  13,   8, 176
]))
packet_keys = []
identification_keys = []
msg_keys = []

def HashPassword(password):
	global salt
	salted_hash = hashlib.sha256(password.encode("ISO8859_1")).hexdigest() + salt
	
	return base64.b64encode(hashlib.sha256(salted_hash.encode("ISO8859_1")).digest())

def SetPacketKeys(keys):
	global packet_keys, identification_keys, msg_keys
	packet_keys, identification_keys, msg_keys = keys

def encode_chunks(v, n):
	global identification_keys
	
	DELTA = 0x9e3779b9
	def MX():
		return int(((z>>5)^(y<<2)) + ((y>>3)^(z<<4))^(sum^y) + (identification_keys[(p & 3)^e]^z))

	y = v[0]
	sum = 0
	if n > 1:
		z = v[n - 1]
		q = int(6 + 52 / n)
	while q > 0:
		q -= 1
		sum = (sum + DELTA) & 0xffffffff
		e =  ((sum >> 2) & 0xffffffff) & 3
		p = 0
		while p < n - 1:
			y = v[p + 1]
			z = v[p] = (v[p] + MX()) & 0xffffffff
			p += 1
		y = v[0]
		z = v[n - 1] = (v[n - 1] + MX()) & 0xffffffff
	return v

def BlockCipher(packet):
	stack = packet.stack
	if len(stack) == 0:
		raise Exception("Block cipher algorithm can't be applied to an empty ByteArray.")
	
	while len(stack) < 8:
		stack += b"\x00"
	
	packet = ByteArray(stack)
	chunks = []
	while len(packet.stack) > 0:
		chunks.append(packet.readLong())
	
	chunks = encode_chunks(chunks, len(chunks))
	
	packet.writeShort(len(chunks))
	for chunk in chunks:
		packet.writeLong(chunk)
	
	return packet

def XorCipher(packet, fingerprint):
	global msg_keys
	
	stack = packet.stack
	new_stack = []
	
	for index, byte in enumerate(stack):
		fingerprint += 1
		new_stack.append((byte ^ msg_keys[fingerprint % 20]) & 255)
	
	return ByteArray(bytes(new_stack))