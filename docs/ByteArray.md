# Methods
>All the "write" methods listed here return the ByteArray object, so a `packet.writeShort(5).writeShort(4)` must work.
>
---
>### packet.\_\_init__ ( stack )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| stack | `bytes` | ✕ | The packet stack if you need to load a packet from bytes. |
>
>Creates a ByteArray object
>
---
>### packet.writeByte ( *byte )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| *byte | `int` | ✕ | The bytes to write in the stack. |
>
>Adds some bytes to the stack, all of them MUST be a positive integer
>
---
>### packet.writeShort ( short )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| short | `string` | ✔ | The name of the event. |
>
>Writes a short integer (0 - 65535) in the packet. Can't be negative.
>
---
>### packet.writeInt ( integer )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| integer | `string` | ✔ | The name of the event. |
>
>Writes an integer (0 - 16777215) in the packet. Can't be negative.
>
---
>### packet.writeLong ( long )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| long | `string` | ✔ | The name of the event. |
>
>Writes a long integer (0 - 4294967295) in the packet. Can't be negative.
>
---
>### packet.writeUTF ( utf )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| utf | `str`, `bytes` | ✔ | The name of the event. |
>
>Writes a string in the packet. The max length is 65535.
>
---
>### packet.writeBigUTF ( big_utf )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| big_utf | `str`, `bytes` | ✔ | The name of the event. |
>
>Writes a big string in the packet. The max length is 16777215.
>
---
>### packet.writeBool ( boolean )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| boolean | `bool` | ✔ | The boolean to write. |
>
>Writes a boolean in the packet.
>
---
>### packet.readByte ( bytesQuantity )
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| bytesQuantity | `int` | ✕ | The quantity of bytes to read. Default value: 1 |
>
>Reads and remove `bytesQuantity` bytes from the packet stack. If the packet stack doesn't have the `bytesQuantity` bytes, the function autocompletes the stack with \x00 bytes.
>
>**Returns:**
>
>| Type | Description |
>| :-: | - |
>| `int`, `bytes` | The bytes that the function got. |
>
---
>### packet.readShort ( )
>Reads and remove 2 bytes from the packet stack.
>
>**Returns:**
>
>| Type | Description |
>| :-: | - |
>| `int` | The short integer that the function got. |
>
---
>### packet.readInt ( )
>Reads and remove 3 bytes from the packet stack.
>
>**Returns:**
>
>| Type | Description |
>| :-: | - |
>| `int` | The integer that the function got. |
>
---
>### packet.readLong ( )
>Reads and remove 4 bytes from the packet stack.
>
>**Returns:**
>
>| Type | Description |
>| :-: | - |
>| `int` | The long integer that the function got. |
>
---
>### packet.readUTF ( bytesQuantity )
>Uses `packet.readShort()` to know the string length. Then reads and remove the string from the packet stack.
>
>**Returns:**
>
>| Type | Description |
>| :-: | - |
>| `str` | The string that the function got. |
>
---
>### packet.readBigUTF ( )
>Uses `packet.readInt()` to know the string length. Then reads and remove the string from the packet stack.
>
>**Returns:**
>
>| Type | Description |
>| :-: | - |
>| `str` | The string that the function got. |
>
---
>### packet.readBool ( )
>Reads and remove 1 byte from the packet stack.
>
>**Returns:**
>
>| Type | Description |
>| :-: | - |
>| `bool` | The boolean that the function got. |
>
---
# Properties
>### packet.stack
>The packet stack. Always a `bytes` object.
