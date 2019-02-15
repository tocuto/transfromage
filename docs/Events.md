# Events
>### on_ready (  )
>
>Triggered when the client has been connected to the server.
>
---
>### on_logged (  )
>
>Triggered when the account is logged and ready to perform actions.
>
---
>### on_player_died ( player )
>
>Triggered when the account is logged and ready to perform actions.
>
---
>### on_player_left ( player )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| player | `Player` | The player |
>
>Triggered when a player leaves the room that the bot is currently in.
>
---
>### on_old_raw_receive ( connection, oldCCC, data )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| connection | `ConnectionHandler` | The connection that has received the old packet. |
>| oldCCC | `list` | The packet identifiers. |
>| data | `list` | The packet data. |
>
>Triggered when the client receives an old packet.
>
---
>### on_login_result ( result_id, result_message )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| result_id | `int` | The result id. |
>| result_message | `str` | The message. |
>
>Triggered when the login was not successful.
>
---
>### on_room_change ( previous_room, new_room )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| previous_room | `Room`, `None` | The room that the bot left. |
>| new_room | `Room` | The room that the bot is currently in (might have not loaded all the players). |
>
>Triggered when the client changes the room.
>
---
>### on_room_message ( message )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| message | `Message` | The message. |
>
>Triggered when the client receives/sends a room message.
>
---
>### on_community_platform_raw_receive ( TC, packet )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| TC | `int` | The community platform packet identifiers. |
>| packet | `ByteArray` | The packet. |
>
>Triggered when the client receives a community platform packet.
>
---
>### on_community_platform_connect (  )
>
>Triggered when the client connects to the community platform.
>
---
>### on_whisper_message ( message )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| message | `Message` | The whisper. |
>
>Triggered when the client receives/sends a whisper.
>
---
>### on_set_player_list (  )
>
>Triggered when the player list is set (generally when there is a new map).
>
---
>### on_update_player_data ( previous_player, new_player )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| previous_player | `Player`, `None` | The player there was before the data update. |
>| new_player | `Player` | The player with the updated data. |
>
>Triggered when a big change has been performed to a player's data (not always called).
>
---
>### on_player_cheese_state_change ( player )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| player | `Player` | The player. |
>
>Triggered when a player gets a cheese or throws it.
>
---
>### on_player_score_change ( player )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| player | `Player` | The player. |
>
>Triggered when a player's score has been changed.
>
---
>### on_player_win ( player )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| player | `Player` | The player. |
>
>Triggered when a player has entered the hole.
>
---
>### on_selected_shamans ( blueShaman, pinkShaman )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| blueShaman | `Player`, `None` | The selected blue shaman. |
>| pinkShaman | `Player`, `None` | The selected pink shaman. |
>
>Triggered when the shamans has been selected.
>
---
>### on_new_shaman ( player )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| player | `Player` | The player. |
>
>Triggered when a player has been turned into a shaman.
>
---
>### on_player_vampire_state_change ( player )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| player | `Player` | The player. |
>
>Triggered when a player has been turned into a vampire or into a player again.
>
---
>### on_shaman_remove ( player )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| player | `Player` | The player. |
>
>Triggered when a player is not a shaman anymore.
>
---
>### on_error ( eventName, exception )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| eventName | `str` | The event name. |
>| exception | `Exception` | The exception that the event threw. |
>
>Triggered when an event (that is not this one) throws an exception (that is not `KeyboardInterrupt`). The exception will be ignored if this event is set.
>
---
>### on_socket_raw_receive ( connection, packet )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| connection | `ConnectionHandler` | The connection that received the packet. |
>| packet | `ByteArray` | The packet that has been received. |
>
>Triggered when a connection receives a packet
>
---
>### on_connection_close ( connection )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| connection | `ConnectionHandler` | The connection that received the packet. |
>
>Triggered when a connection is closed
>
---
>### on_connection_made ( connection )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| connection | `ConnectionHandler` | The connection that received the packet. |
>
>Triggered when a connection is made (not the same as on_ready)
>
---
>### on_socket_raw_send ( connection, identifiers, packet )
>| Parameter | Type | Description |
>| :-: | :-: | - |
>| connection | `ConnectionHandler` | The connection that sent the packet. |
>| identifiers | `list`, `tuple` | The packet identifiers. |
>| packet | `ByteArray` | The packet that has been sent. |
>
>Triggered when the `connection.send` method is called.
>
