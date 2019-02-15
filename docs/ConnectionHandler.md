# Methods
>### conn.\_\_init__( name, call_event )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| name | `str` | ✔ | The connection name. |
>| call_event | `function` | ✔ | The function that we use to call an event. |
>
>Creates a `ConnectionHandler` object.
>
---
>### conn.send( identifiers, alpha_packet )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| identifiers | `list`, `tuple` | ✔ | The connection name. |
>| alpha_packet | `ByteArray`, `bytes`, `int`, `list`, `tuple` | ✔ | The function that we use to call an event. |
>
>Sends a packet to the connection.<br>
>Using `ByteArray` sends the packet to the server, using `bytes` will be the same as doing `ByteArray(bytes)` and using `int` will be the same as using `ByteArray().writeByte(int)`<br>
>Using `list` is the equivalent to using `tuple`, it sends an "old" packet to the server.
>
---
# Properties
>### conn.ip
>A `str` object representing the other side of the connection's ip
>
---
>### conn.port
>An `int` object representing the other side of the connection's port
>
---
>### conn.name
>A `str` object representing the connection's name
>
---
>### conn.open
>A `bool` object representing if the connection is open or not
>
