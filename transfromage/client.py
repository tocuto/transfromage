from .connection import ConnectionHandler
from .bytearray import ByteArray
from .utilities import enum, new
from .cipher import HashPassword, BlockCipher, XorCipher, SetPacketKeys

from urllib.request import urlopen, Request
from json import loads

import traceback
import time
import zlib

class ApiEndpointException(Exception):
	"""Main Exception for the api endpoint errors.
	Thrown when the API can't get the game encryption keys."""
	
	pass

class Client(object):
	"""This is the connection between the server connection and the events.
	It allows you to set events (ex: on_socket_raw_receive) and run your bot."""
	
	def __init__(self, max_threads = 10):
		# Initializacion values
		
		self.main = ConnectionHandler("main", self.call_event)
		self.bulle = None
		
		self.running_events = []
		self.game_packet_keys = []
		self.events = {}
		self.community_platform_fingerprint = 0
		self.received_authkey = 0
		self.last_heartbeat = 0
		self.game_auth_key = 0
		self.game_version = 0
		self.game_connection_key = ""

		# data
		self.onlinePlayers = 0
		self.community = ""
		self.country = ""
		self.playerId = 0
		self.playingTime = 0
		self.connectionTime = 0
		self.player = None
		self.room = None
		
		self.SmartThread = new.SmartThread(max_threads)
	
	def parse_old_packet(self, connection, CCC, data):
		"""This is the parse old packets function.
		This is called so the most technical stuff are working by default."""
		
		if CCC == (8, 5):
			pcode, score = int(data[0]), int(data[1])
			player = self.room.get_player(pcode, "pcode")
			
			if player != None:
				player.isAlive = False
				player.score = score
				self.call_event("on_player_died", player)
		
		elif CCC == (8, 7):
			player = self.room.get_player(int(data[0]), "pcode")
			
			if player != None:
				self.room.remove_player(player)
				self.call_event("on_player_left", player)
	
	def parse_packet(self, connection, packet):
		"""This is the parse packets function.
		This is called so the most technical stuff (such as parsing auth keys, switching the bulle connection)
		are working by default."""
		
		CCC = (packet.readByte(), packet.readByte())
		# Reads the packet identifiers
		
		if CCC == (1, 1):
			data = packet.readUTF().split("\x01")
			oldCCC = data.pop(0)
			oldCCC = (ord(oldCCC[0]), ord(oldCCC[1]))
			
			self.call_event("on_old_raw_receive", connection, oldCCC, data)
			self.parse_old_packet(connection, oldCCC, data)
		
		elif CCC == (26, 3): # Correct handshake identifiers
			self.onlinePlayers = packet.readLong()
			connection.packetID = packet.readByte() # Sets the packet id of the connection
			self.community = packet.readUTF().upper()
			self.country = packet.readUTF()
			self.received_authkey = packet.readLong() # Receives an authentication key, this will be parsed
			# when the login function is called
			
			self.last_heartbeat = time.time()
			self.SmartThread.runParallelTask(target = self.heartbeat_loop) # Starts the heartbeat loop
			
			self.setCommunity("EN") # Sets the connection community to EN
			
			os_info = ByteArray().writeUTF("en").writeUTF("Linux")
			os_info.writeUTF("LNX 29,0,0,140").writeByte(0)
			self.main.send([28, 17], os_info) # Sends the OS Info
			self.call_event("on_ready")
		
		elif CCC == (44, 1): # Switch bulle identifiers
			bulle_id = packet.readLong()
			bulle_ip = packet.readUTF()
			
			self.bulle = ConnectionHandler("bulle", self.call_event)
			self.bulle.connect(bulle_ip, self.main.port)
			
			self.bulle.send(CCC, ByteArray().writeLong(bulle_id))
		
		elif CCC == (44, 22): # PacketId offset identifiers
			connection.packetID = packet.readByte() # Sets the packet id of the connection

		elif CCC == (26, 2): # Logged in successfully
			self.playerId = packet.readLong()
			name = packet.readUTF()
			self.playingTime = packet.readLong()
			self.connectionTime = time.time()
			self.community = packet.readByte()#enum.communities[packet.readByte()]
			pcode = packet.readLong()
			
			self.player = new.info.Player(0, name, pcode)
			
			self.call_event("on_logged")

		elif CCC == (26, 12):
			self.call_event("on_login_result", packet.readByte(), packet.readUTF())

		elif CCC == (5, 21): # Joined to a room
			previous_room = self.room
			self.room = new.info.Room(packet.readBool(), packet.readUTF())
			self.room.update_player(self.player)
			
			self.call_event("on_room_change", previous_room, self.room)

		elif CCC == (6, 6): # Room message
			author = self.room.get_player(packet.readLong(), "pcode")
			author.name = packet.readUTF()
			community = enum.communities[packet.readByte()]
			content = packet.readUTF().replace("&","&amp;").replace("&lt;","<")
			
			self.call_event("on_room_message", new.info.Message(False, author, community, content))

		elif CCC == (60, 3): # Tribulle packet received
			code = packet.readShort()
			self.call_event("on_community_platform_raw_receive", code, ByteArray(packet.stack))
			
			if code == 3: # Tribulle code
				self.call_event("on_community_platform_connect")

			elif code == 66: # whisper
				author = packet.readUTF()
				community = enum.cp_communities[packet.readLong()]
				sentTo = packet.readUTF()
				content = packet.readUTF().replace("&amp;","&").replace("&lt;","<")
				self.call_event("on_whisper_message", new.info.Message(True, author, community, content, sentTo))

		elif CCC == (144, 1): # Set players' data
			self.room.playersSearch = {
				"pcode": {},
				"name": {},
				"object": {}
			}
			self.room.players = {}
			
			playersQuantity = packet.readShort()
			
			for index in range(playersQuantity):
				player = new.info.Player(1, packet)
				if player.pcode == self.player.pcode:
					self.player = player
				
				self.room.update_player(player)
			
			self.call_event("on_set_player_list")
		
		elif CCC == (144, 2): # Update player data
			_packet = ByteArray(packet.stack)
			_packet.readUTF()
			
			previous_player = self.room.get_player(_packet.readLong(), "pcode")
			new_player = new.info.Player(2, packet)
			if new_player.pcode == self.player.pcode:
				self.player = new_player
			
			self.room.update_player(new_player)
			self.call_event("on_update_player_data", previous_player, new_player)
		
		elif CCC in [(4, 4), (4, 6), (4, 9), (4, 10)]: # Updating a player's data
			player = self.room.get_player(packet.readLong(), "pcode")
			
			if player != None:
				event_name = player.syncUpdate(CCC[1], packet)
				self.call_event(event_name, player)

		elif CCC == (144, 6):
			player = self.room.get_player(packet.readLong(), "pcode")

			if player != None:
				player.hasCheese = packet.readBool()
				self.call_event("on_player_cheese_state_change", player)

		elif CCC == (8, 19):
			player = self.room.get_player(packet.readLong(), "pcode")

			if player != None:
				player.hasCheese = False
				self.call_event("on_player_cheese_state_change", player)
		
		elif CCC == (8, 7):
			player = self.room.get_player(packet.readLong(), "pcode")
			
			if player != None:
				player.score = packet.readShort()
				self.call_event("on_player_score_change", player)
		
		elif CCC == (8, 6):
			packet.readBool() # is defilante?
			player = self.room.get_player(packet.readLong(), "pcode")
			
			if player != None:
				player.score = packet.readShort()
				player.hasWon = [packet.readByte(), packet.readShort() / 100]
				self.call_event("on_player_score_change", player)
				self.call_event("on_player_win", player)
		
		elif CCC == (8, 11):
			blueShaman = self.room.get_player(packet.readLong(), "pcode")
			pinkShaman = self.room.get_player(packet.readLong(), "pcode")
			
			if blueShaman != None:
				blueShaman.isShaman = True
			if pinkShaman != None:
				pinkShaman.isShaman = True
			
			self.call_event("on_selected_shamans", blueShaman, pinkShaman)
		
		elif CCC == (8, 12):
			player = self.room.get_player(packet.readLong(), "pcode")
			
			if player != None:
				player.isShaman = True
				self.call_event("on_new_shaman", player)
		
		elif CCC == (8, 66):
			player = self.room.get_player(packet.readLong(), "pcode")
			
			if player != None:
				player.isVampire = packet.readBool()
				self.call_event("on_player_vampire_state_change", player)
		
		elif CCC == (144, 7):
			player = self.room.get_player(packet.readLong(), "pcode")
			
			if player != None:
				player.isShaman = False
				self.call_event("on_shaman_remove", player)
		
		elif CCC == (5, 2):
			mapCode = packet.readLong()
			packet.readShort() # room players?
			packet.readByte() # round code
			packet.readShort() # ???
			xml = zlib.decompress(packet.readByte(packet.readShort())).decode('utf-8')
			author = packet.readUTF()
			perm = packet.readByte()
			isInverted = packet.readBool()
			
			previous_map = self.room.map
			self.room.map = new.info.Map(mapCode, xml, author, perm, isInverted)
			
			self.call_event("on_map_change", previous_map, self.room.map)

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

	def sendWhisper(self, player_name, message):
		"""This is the function that sends a whisper to a player."""
		
		self.sendCPPacket(52, ByteArray().writeUTF(player_name).writeUTF(message))

	def sendCommand(self, command):
		"""This is the function that sends a command."""

		self.main.send([6, 26], XorCipher(ByteArray().writeUTF(command), self.main.packetID))
	
	def requestJoinRoom(self, room_name):
		"""This function sends a request to the server to join a room."""
		
		packet = ByteArray().writeByte(255)
		packet.writeUTF(room_name).writeByte(0)
		self.main.send([5, 38], packet)

	def sendCPPacket(self, TC, packet):
		"""This is the function that sends a packet to the community platform."""
		
		self.community_platform_fingerprint = (self.community_platform_fingerprint % 0x100000000) + 1
		_packet = ByteArray().writeShort(TC).writeLong(self.community_platform_fingerprint)
		_packet.stack += packet.stack
		
		self.main.send([60, 3], XorCipher(_packet, self.main.packetID))

	def setCommunity(self, name):
		"""This is the function that sets the connection community id."""

		communityID = enum.communities.get(name.upper())
		if communityID == None:
			communityID = 0
		community = ByteArray().writeByte(communityID).writeByte(0)
		self.main.send([8, 2], community) 
	
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
			self.SmartThread.runParallelTask(target = self.events[event_name], args = args, kwargs = kwargs)
			return True
		return False
	
	def loop_run(self):
		"""Main loop."""
		
		self.SmartThread.runParallelTask(target = self.main_receive_loop)
		self.SmartThread.runParallelTask(target = self.bulle_receive_loop)
		
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
		
		self.SmartThread.runParallelTask(target = self.SmartThread.tasksQueueLoop, args = (self.main,))
		self.loop_run()