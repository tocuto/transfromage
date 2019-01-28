from .bytearray import ByteArray

import sys
import socket
import traceback

class ConnectionHandler(object):
	def __init__(self, name, call_event):
		self.call_event = call_event
		self.socket = None
		self.ip = ""
		self.packetID = 0
		self.port = 0
		self.name = name
		self.open = False
	
	def connect(self, ip, port):
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except:
			print("[{name}]: socket can't be created.".format(name=self.name))
			sys.exit(0)
		
		self.socket.setblocking(0)
		self.socket.settimeout(3)
		
		host = socket.gethostbyname(ip)
		if host == None:
			print("[{name}] host could not be resolved.".format(name=self.name))
			sys.exit(0)
		try:
			self.socket.connect((host, port))
		except socket.timeout:
			print("[{name}]: connection timed out.".format(name=self.name))
			sys.exit(0)
		
		self.socket.settimeout(None)
		
		self.ip = ip
		self.port = port
		self.open = True
		
		self.call_event("on_connection_made", self)
	
	def __receive(self, length):
		result = self.socket.recv(length)
		if length > 0 and len(result) == 0:
			self.open = False
			self.socket.close()
			raise Exception("The connection has been closed.")
		
		return result
	
	def receive(self):
		stack_length_size = self.__receive(1)[0]
		
		if stack_length_size > 0:
			stack_length_bytes = self.__receive(stack_length_size)
			stack_length = 0
			for index, byte in enumerate(stack_length_bytes):
				stack_length += byte << (8 * (stack_length_size - index - 1))
			
			return self.__receive(stack_length)
		return b""
	
	def send(self, identifiers, alpha_packet):
		beta_packet = None
		gamma_packet = None
		
		if not isinstance(identifiers, (list, tuple)):
			raise Exception("Unknown identifiers type? Must be a list or tuple object!")
		
		if isinstance(alpha_packet, ByteArray):
			beta_packet = ByteArray(bytes(identifiers) + alpha_packet.stack)
		
		elif isinstance(alpha_packet, bytes):
			beta_packet = ByteArray(bytes(identifiers) + alpha_packet)
		
		elif isinstance(alpha_packet, int):
			beta_packet = ByteArray().writeByte([*identifiers, alpha_packet])
		
		elif isinstance(alpha_packet, (list, tuple)):
			beta_packet = ByteArray().writeByte(1, 1).writeUTF(
				"\x01".join(
					map(
						str,
						[chr(identifiers[0]) + chr(identifiers[1])] + alpha_packet
					)
				)
			)
		
		else:
			raise Exception("Unknown packet type? Must be a ByteArray, bytes, int, list or tuple object! (Identifiers: " + repr(identifiers) + ")")
		
		stack_length = len(beta_packet.stack)
		if stack_length < 256:
			gamma_packet = ByteArray().writeByte(1, stack_length)
		elif stack_length < 65536:
			gamma_packet = ByteArray().writeByte(2).writeShort(stack_length)
		elif stack_length < 16777216:
			gamma_packet = ByteArray().writeByte(3).writeInt(stack_length)
		else:
			raise Exception("The packet is too big! (Identifiers: " + repr(identifiers) + ")")
		
		gamma_packet.writeByte(self.packetID)
		self.packetID = (self.packetID + 1) % 100
		
		gamma_packet.stack += beta_packet.stack
		
		self.call_event("on_socket_raw_send", self, identifiers, alpha_packet)
		try:
			self.socket.send(gamma_packet.stack)
		except:
			self.open = False
			self.call_event("on_connection_close", self)