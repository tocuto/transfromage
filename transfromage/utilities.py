import threading
import struct

class enum:
	communities = {
		"EN":  0,  0: "EN",
		"FR":  1,  1: "FR",
		"BR":  2,  2: "BR",
		"ES":  3,  3: "ES",
		"CN":  4,  4: "CN",
		"TR":  5,  5: "TR",
		"VK":  6,  6: "VK",
		"PL":  7,  7: "PL",
		"HU":  8,  8: "HU",
		"NL":  9,  9: "NL",
		"RO": 10, 10: "RO",
		"ID": 11, 11: "ID",
		"DE": 12, 12: "DE",
		"E2": 13, 13: "E2",
		"AR": 14, 14: "AR",
		"PH": 15, 15: "PH",
		"LT": 16, 16: "LT",
		"JP": 17, 17: "JP",
		"CH": 18, 18: "CH",
		"FI": 19, 19: "FI",
		"CZ": 20, 20: "CZ",
		"SK": 21, 21: "SK",
		"HR": 22, 22: "HR",
		"BU": 23, 23: "BU",
		"LV": 24, 24: "LV",
		"HE": 25, 25: "HE",
		"IT": 26, 26: "IT",
		"ET": 27, 27: "ET",
		"AZ": 28, 28: "AZ",
		"PT": 29, 29: "PT"
	}
	cp_communities = {
		"EN":  1,  1: "EN",
		"FR":  2,  2: "FR",
		"RU":  3,  3: "RU",
		"BR":  4,  4: "BR",
		"ES":  5,  5: "ES",
		"CN":  6,  6: "CN",
		"TR":  7,  7: "TR",
		"VK":  8,  8: "VK",
		"PL":  9,  9: "PL",
		"HU": 10, 10: "HU",
		"NL": 11, 11: "NL",
		"RO": 12, 12: "RO",
		"ID": 13, 13: "ID",
		"DE": 14, 14: "DE",
		"AR": 16, 16: "AR",
		"PH": 17, 17: "PH",
		"LT": 18, 18: "LT",
		"JP": 19, 19: "JP",
		"CH": 20, 20: "CH",
		"FI": 21, 21: "FI",
		"CZ": 22, 22: "CZ",
		"HR": 23, 23: "HR",
		"CZ": 24, 24: "CZ",
		"SK": 25, 25: "SK",
		"HR": 26, 26: "HR",
		"BG": 27, 27: "BG",
		"LV": 28, 28: "LV",
		"HE": 29, 29: "HE",
		"IT": 30, 30: "IT",
		"ET": 31, 31: "ET",
		"AZ": 32, 32: "AZ",
		"PT": 33, 33: "PT",
	}

class new(object):
	class SmartThread(object):
		def __init__(self, max_threads):
			self.max_threads = max_threads
			self.tasksQueue = []
		
		def tasksQueueLoop(self, main_connection):
			while main_connection.open:
				if threading.active_count() < self.max_threads and self.tasksQueue != []:
					next_task = self.tasksQueue.pop(0)
					
					threading.Thread(*next_task[0], **next_task[1]).start()
		
		def runParallelTask(self, *args, **kwargs):
			if threading.active_count() < self.max_threads:
				threading.Thread(*args, **kwargs).start()
			
			else:
				self.tasksQueue.append([args, kwargs])
	
	class info:
		class Room(object):
			def __init__(self, isPublic, name):
				self.players = {}
				self.playersSearch = {
					"pcode": {},
					"name": {},
					"object": {}
				}
				
				self.map = None
				self.isPublic = isPublic
				self.isInternational = name[0] == "*"
				if not self.isInternational:
					self.community = name[:2].upper()
					self.name = name[3:]
				else:
					self.community = "XX"
					self.name = name
			
			def remove_player(self, player):
				if player.name in self.players:
					del self.players[player.name]
					for searchMethod in self.playersSearch.copy():
						if searchMethod == "name":
							del self.playersSearch["name"][player.name.lower()]
							continue
						
						del self.playersSearch[searchMethod][getattr(player, searchMethod)]
			
			def update_player(self, player):
				isNew = True
				
				for _player in self.players.copy().values():
					if _player.pcode == player.pcode:
						self.remove_player(_player)
						# Prevent any name change or related things that may cause any bug
						
						isNew = False
						break
				
				self.players[player.name] = player
				for searchMethod in self.playersSearch.copy():
					self.playersSearch[searchMethod][player.name.lower() if searchMethod == "name" else getattr(player, searchMethod)] = player.name
				
				return isNew
			
			def get_player(self, key, search_by = "name"):
				if search_by == "name":
					key = key.lower()
				
				if search_by in self.playersSearch:
					return self.players.get(self.playersSearch[search_by].get(key))
				
				raise Exception("Invalid search at Room.get_player: search_by must be either " + (", ".join(self.playersSearch)) + ", can't be " + str(search_by))
		
		class Player(object):
			def __init__(self, fromPacket, *data):
				if fromPacket == 0:
					self.name = data[0]
					self.pcode = data[1]
					self.isShaman = False
					self.isAlive = False
					self.score = 0
					self.hasCheese = False
					self.title = 0
					self.titleStars = 0
					self.gender = 0
					self.look = "1;0,0,0,0,0,0,0,0,0,0"
					self.mouseColor = 7886906
					self.shamanColor = 9820630
					self.nameColor = -1
				
				elif fromPacket in [1, 2]:
					packet = data[0]
					
					self.name = packet.readUTF()
					self.pcode = packet.readLong()
					self.isShaman = packet.readBool()
					self.isAlive = not packet.readBool()
					self.score = packet.readShort()
					self.hasCheese = packet.readBool()
					self.title = packet.readShort()
					self.titleStars = packet.readByte() - 1
					self.gender = packet.readByte()
					packet.readUTF() # ???
					self.look = packet.readUTF()
					packet.readBool() # ???
					self.mouseColor = packet.readLong()
					self.shamanColor = packet.readLong()
					packet.readLong() # ???
					
					color = packet.readLong()
					self.nameColor = -1 if color == 0xFFFFFFFF else color
				
				self.souris = self.name[0] == "*"
				self.isVampire = False
				
				if fromPacket == 1:
					self.hasWon = False
				
				self.facingRight = True
				self.movingRight = False
				self.movingLeft = False
				
				self.x = 0
				self.y = 0
				self.vx = 0
				self.vy = 0
				self.crouch = False
				self.jumping = False
				
				self.object = self
			
			def syncUpdate(self, syncCC, packet):
				if syncCC == 4: # player movement
					packet.readLong() # round code
					
					self.movingRight = packet.readBool()
					self.movingLeft = packet.readBool()
					
					self.x = int((struct.unpack("!i", packet.readByte(4))[0] * 800 / 2700) + .5)
					self.y = int((struct.unpack("!i", packet.readByte(4))[0] * 800 / 2700) + .5)
					self.vx = struct.unpack("!h", packet.readByte(2))[0]
					self.vy = struct.unpack("!h", packet.readByte(2))[0]
					
					self.jumping = packet.readBool()
					
					return "on_player_movement"

				elif syncCC in [6, 10]: # facing direction
					self.facingRight = packet.readBool()
					
					return "on_player_direction_change"

				elif syncCC == 9: # crouch
					self.crouch = packet.readBool()
					
					return "on_player_crouch"
		
		class Message(object):
			def __init__(self, isWhisper, author, community, content, sentTo=None):
				self.isWhisper = isWhisper
				self.sentTo = sentTo
				self.author = author
				self.community = community
				self.content = content
		
		class Map(object):
			def __init__(self, mapCode, xml, author, perm, isInverted):
				self.code = mapCode
				self.xml = xml
				self.author = author
				self.perm = perm
				self.isInverted = isInverted