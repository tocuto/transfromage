import transfromage

client = transfromage.Client()

@client.event
def on_ready():
    client.setCommunity('EN')
    client.login("Username", "Password", "Room name")

@client.event
def on_logged():
    print('Logged in! '+client.player.name)

@client.event
def on_room_message(message):
    if message.content == 'hi':
        client.sendRoomMessage(message.author.name+', Hello !')

client.start('api-id', 'token') 
