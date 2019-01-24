from .connection import ConnectionHandler
from .bytearray import ByteArray
from .cipher import HashPassword, BlockCipher, XorCipher, SetPacketKeys

from urllib.request import urlopen, Request
from threading import Thread
from json import loads

import traceback
import time

class ApiEndpointException(Exception):
	"""Main Exception for the api endpoint errors.
	Thrown when the API can't get the game encryption keys."""
	
	pass

class Client(object):
	"""This is the connection between the server connection and the events.
	It allows you to set events (ex: on_socket_raw_receive) and run your bot."""
	
	def __init__(self):
		# Initializacion values
		
		self.main = ConnectionHandler("main", self.call_event)
		self.bulle = None
		
		self.running_events = []
		self.game_packet_keys = []
		self.events = {}
		self.received_authkey = 0
		self.last_heartbeat = 0
		self.game_auth_key = 0
		self.game_version = 0
		self.game_connection_key = ""
	
	def parse_packet(self, connection, packet):
		"""This is the parse packets function.
		This is called so the most technical stuff (such as parsing auth keys, switching the bulle connection)
		are working by default."""
		
		CCC = (packet.readByte(), packet.readByte())
		# Reads the packet identifiers
		
		if CCC == (26, 3): # Correct handshake identifiers
			online_players = packet.readLong()
			connection.packetID = packet.readByte() # Sets the packet id of the connection
			community = packet.readUTF()
			country = packet.readUTF()
			self.received_authkey = packet.readLong() # Receives an authentication key, this will be parsed
			# when the login function is called
			
			self.last_heartbeat = time.time()
			Thread(target = self.heartbeat_loop).start() # Starts the heartbeat loop
			
			community = ByteArray().writeByte(0).writeByte(0)
			self.main.send([8, 2], community) # Sets the connection community to EN
			
			os_info = ByteArray().writeUTF("en").writeUTF("Linux")
			os_info.writeUTF("LNX 29,0,0,140").writeByte(0)
			self.main.send([28, 17], os_info) # Sends the OS Info
		
		elif CCC == (44, 1): # Switch bulle identifiers
			bulle_id = packet.readLong()
			bulle_ip = packet.readUTF()
			
			self.bulle = ConnectionHandler("bulle", self.call_event)
			self.bulle.connect(bulle_ip, self.main.port)
			
			self.bulle.send(CCC, ByteArray().writeLong(bulle_id))
		
		elif CCC == (44, 22): # PacketId offset identifiers
			connection.packetID = packet.readByte() # Sets the packet id of the connection
	
	def event(self, function):
		"""This is the decorator for setting an event.
		All what this does is to make a wrapper so when any event throws any error, this handles it.
		Also, this registers the event to the `events` dictionary"""
		
		def wrapper(*args, **kwargs):
			try:
				return function(*args, **kwargs)
			except KeyboardInterrupt:
				self.close_all()
			except Exception as exc:
				if function.__name__ == "on_error":
					self.close_all()
					raise exc
				
				else:
					if not self.call_event("on_error", function.__name__, exc):
						self.close_all()
						raise exc
		
		wrapper.__name__ = function.__name__
		self.events[function.__name__] = wrapper
		return wrapper
	
	def login(self, player, password, start_room = "1"):
		"""This is the login function.
		Hashes your password, parses the authentication key, encrypts the packet and sends it to the server."""
		
		packet = ByteArray().writeUTF(player).writeUTF(HashPassword(password))
		packet.writeUTF("app:/TransformiceAIR.swf/[[DYNAMIC]]/2/[[DYNAMIC]]/4").writeUTF(start_room)
		packet.writeLong(self.received_authkey ^ self.game_auth_key)
		
		self.main.send([26, 8], BlockCipher(packet).writeByte(0))
	
	def sendRoomMessage(self, message):
		"""This is the function that sends a message to the room.
		Encrypts the packet and sends it to the server."""
		
		self.bulle.send([6, 6], XorCipher(ByteArray().writeUTF(message), self.bulle.packetID))
	
	def main_receive_loop(self):
		"""Receive loop for the main connection."""
		
		while self.main.open: # While the main connection is open
			packet = self.main.receive()
			
			self.call_event("on_socket_raw_receive", self.main, ByteArray(packet))
			self.parse_packet(self.main, ByteArray(packet))
	
	def bulle_receive_loop(self):
		"""Receive loop for the bulle conenction."""
		
		while self.main.open: # While the main connection is open
			if self.bulle != None and self.bulle.open: # If the bulle connection is open
				packet = self.bulle.receive()
				
				self.call_event("on_socket_raw_receive", self.bulle, ByteArray(packet))
				self.parse_packet(self.bulle, ByteArray(packet))
	
	def heartbeat_loop(self):
		"""Heart beat/Keep alive loop for the conenction."""
		
		while self.main.open: # While the main connection is open
			if (time.time() - self.last_heartbeat) >= 10: # If we are ten seconds or more later of the last heartbeat sent
				self.main.send([26, 26], ByteArray()) # Send another heartbeat
				
				if self.bulle != None and self.bulle.open:
					self.bulle.send([26, 26], ByteArray())
				
				self.last_heartbeat = time.time() # Set the last heartbeat sent to this time
				time.sleep(10)
	
	def close_all(self):
		"""Close function."""
		
		if self.bulle != None and self.bulle.open:
			self.bulle.open = False
			try:
				self.bulle.socket.close()
				self.call_event("on_connection_close", self.bulle)
			except:
				pass
		
		self.main.open = False
		try:
			self.main.socket.close()
			self.call_event("on_connection_close", self.main)
		except:
			pass
	
	def call_event(self, event_name, *args, **kwargs):
		"""This function calls an event.
		Returns True if the event was CALLED (this doesn't mean that the event finished the call)."""
		
		if event_name in self.events:
			Thread(target = self.events[event_name], args = args, kwargs = kwargs).start()
			return True
		return False
	
	def loop_run(self):
		"""Main loop."""
		
		Thread(target = self.main_receive_loop).start()
		Thread(target = self.bulle_receive_loop).start()
		
		while self.main.open:
			pass
		
		self.close_all() # Closes all
	
	def get_keys(self, api_tfmid, api_token):
		"""Get keys function.
		This gets the keys of the tocu.tk API for the transformice connection."""
		
		result = loads(
			urlopen(
				Request(
					"https://api.tocu.tk/get_transformice_keys.php?tfmid=" + str(api_tfmid) + "&token=" + api_token,
					headers = {
						"User-Agent": "Mozilla/5.0"
					}
				)
			).read()
		)
		
		if result["success"]:
			if not result["internal_error"]:
				self.game_version = result["version"]
				self.game_connection_key = result["connection_key"]
				self.game_auth_key = result["auth_key"]
				self.game_packet_keys = result["packet_keys"]
				self.game_identification_keys = result["identification_keys"]
				self.game_msg_keys = result["msg_keys"]
				SetPacketKeys([self.game_packet_keys, self.game_identification_keys, self.game_msg_keys])
			
			else:
				if result["internal_error_step"] == 2:
					mightBeMaintenance = ": The game might be in maintenance mode."
				else:
					mightBeMaintenance = ""
				raise ApiEndpointException("There was an internal API Endpoint error. (" + str(result["internal_error_step"]) + ")" + mightBeMaintenance)
		else:
			raise ApiEndpointException("Can't get the keys. Error info: " + result["error"])
	
	def start(self, api_tfmid, api_token):
		"""Starts the bot.
		Gets the encryption keys, starts a connection, sends the handshake packet and starts the main loop."""
		
		self.get_keys(api_tfmid, api_token)
		
		self.main.connect("164.132.202.12", 5555)
		
		packet = ByteArray().writeShort(self.game_version).writeUTF(self.game_connection_key)
		packet.writeUTF("Desktop").writeUTF("-").writeLong(8125).writeUTF("")
		packet.writeUTF("86bd7a7ce36bec7aad43d51cb47e30594716d972320ef4322b7d88a85904f0ed")
		packet.writeUTF("A=t&SA=t&SV=t&EV=t&MP3=t&AE=t&VE=t&ACC=t&PR=t&SP=f&SB=f&DEB=f&V=LNX 29,0,0,140&M=Adobe Linux&R=1920x1080&COL=color&AR=1.0&OS=Linux&ARCH=x86&L=en&IME=t&PR32=t&PR64=t&LS=en-US&PT=Desktop&AVD=f&LFD=f&WD=f&TLS=t&ML=5.1&DP=72")
		packet.writeLong(0).writeLong(25175).writeUTF("")
		
		self.main.send([28, 1], packet)
		
		self.loop_run()