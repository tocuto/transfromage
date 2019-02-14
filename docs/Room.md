#Methods
>### room.\_\_init__( isPublic, name )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| isPublic | `bool` | ✔ | Whether if the room is public or not |
>| name | `str` | ✔ | The room's name |
>
>Creates the Room object.
>
---
>### room.remove_player( player )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| player | `Player` | ✔ | The player |
>
>Removes a player from the room's player list
>
---
>### room.update_player( player )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| player | `Player` | ✔ | The player |
>
>Adds/Updates a player from the room's player list
>
---
>### room.get_player( key, search_by )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| key | `str`, `int`, `Player` | ✔ | The player to search |
>| search_by | `str` | ✕ | Where to search |
>
>Searchs a player in the room.
>
>**Returns:**
>
>| Type | Description |
>| :-: | - |
>| `Player`, `None` | The player if it is in the room, otherwise None |
>
---
#Properties
>### room.players
>A `dict` object with the players in the room
>
---
>### room.isPublic
>Whether if the room is public or not (`bool`)
>
---
>### room.isInternational
>Whether if the room is international or not (`bool`)
>
---
>### room.community
>The room community (`str`)
>
---
>### room.name
>The room name (`str`)
>
