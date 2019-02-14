# Methods
>### client.\_\_init__ ( max_threads )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| max_threads | `int` | ✕ | The maximum threads that the program can run. Default value: 10 |
>
>Creates a Client object. The max_threads value doesn't just affect the threads the client runs, affect all the threads.<br>
>So if you limit it to 10 threads and your program runs 10 threads, the client can't run and will be waiting until all your threads stop.
>
---
>### client.event ( function )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| function | `function` | ✔ | The function that will be saved as an event |
>
>Decorator function for setting an event
>
>**Returns:**
>
>| Type | Description |
>| :-: | - |
>| `function` | The wrapper that will act as the event. This will throw an on_error event if the event fails and the setted event is not on_error |
>
---
>### client.login ( player, password, start_room )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| player | `str` | ✔ | The player's name |
>| password | `str` | ✔ | The player's password |
>| start_room | `str` | ✕ | The start room of the player. Default value: 1 |
>
>Sends the login packet
>
---
>### client.sendRoomMessage ( message )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| message | `str` | ✔ | The message |
>
>Sends a message to the room
>
---
>### client.sendWhisper ( player_name, message )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| player_name | `str` | ✔ | The player's name to send the whisper |
>| message | `str` | ✔ | The message |
>
>Sends a whisper
>
---
>### client.sendCPPacket ( TC, packet, encrypt )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| TC | `int` | ✔ | The packet identifier |
>| packet | `ByteArray` | ✔ | The packet to send |
>| encrypt | `bool` | ✕ | Whether to encrypt or not the packet. Default value: False |
>
>Sends a packet to the community platform
>
---
>### client.setCommunity ( name )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| name | `str` | ✔ | The community name |
>
>Sets the player community
>
---
>### client.close_all ( )
>Ends the bot
>
---
>### client.start ( api_tfmid, api_token )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| api_tfmid | `int`, `str` | ✔ | Your API Endpoint tfmid |
>| api_token | `str` | ✔ | Your API Endpoint token |
>
>Gets all the transformice keys, starts the connection with the server and runs all the loops
>
---
# Properties
>### client.main
>The `ConnectionHandler` object of the main connection with the server.
>
---
>### client.bulle
>The `ConnectionHandler` object of the bulle connection with the room server. Might be None.
>
---
>### client.onlinePlayers
>An `int` object of the connected players in the server when the connection was established.
>
---
>### client.community
>A `str` object of the community that the client is connected to.
>
---
>### client.country
>A `str` object of the origin country of the client connection.
>
---
>### client.playerName
>A `str` object of the client's player name.
>
---
>### client.pcode
>A `str` object of the client's player code.
>
---
>### client.playerId
>A `int` object of the client's player id.
>
---
>### client.playingTime
>An `int` object of the client's playing time when the login packet was received.
>
---
>### client.connectionTime
>An `int` object of when the login packet was received.
>
---
>### client.player
>A `Player` object of the client's player. Might be None.
>
---
>### client.room
>A `Room` object of the client's player room. Might be None.
>
