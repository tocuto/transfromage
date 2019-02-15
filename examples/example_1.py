import transfromage

client = transfromage.Client()

@client.event
def on_ready():
    client.setCommunity('EN')
    client.login("Username", "Password", "Room name")

@client.event
def on_logged():
    print('Logged in! '+client.player.name)

inTribe = False

@client.event
def on_whisper_message(message):
    global inTribe
    if message.content == '!tribe':
        client.requestJoinRoom('*\x03Tribe name')
        inTribe = True
    elif message.content == '!invite':
        if inTribe:
            client.sendCommand('inv '+message.author)
            client.sendWhisper(message.author, 'You were invited to the tribe house !')
        else:
            client.sendWhisper(message.author, 'I\'m not in the tribe house :(')
    else:
        client.sendWhisper(message.author, 'This command doesn\'t exist !')
        

client.start('api-id', 'token') 