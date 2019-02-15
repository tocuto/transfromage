# Some extra functions that are imported
---
# Exceptions
>### ApiEndpointException
>Base exception that is thrown when the bot can't get the transformice's encryption keys. Has some descriptive messages.
>
---
# Functions
>### HashPassword
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| password | `string` | ✔ | The password to hash. |
>
>Hashes a password with the transformice's hash algorithm
>
---
>### BlockCipher
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| packet | `ByteArray` | ✔ | The packet to cipher. |
>
>Ciphers a packet with the XXTea algorithm
>
---
>### XorCipher
>| Parameter | Type | Required | Description |
>| :-: | :-: | :-: | - |
>| packet | `ByteArray` | ✔ | The packet to cipher. |
>| fingerprint | `int` | ✔ | The fingerprint to use. |
>
>Ciphers a packet with a XOR cipher algorithm. Fingerprint is the packetID of the connection handler where you're gonna send the packet.
>
