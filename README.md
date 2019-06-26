<p align='center'><a href='https://atelier801.com/topic?f=5&t=917024'><img src="http://images.atelier801.com/168e7d7a07d.png" title="Fromage"></a></p>

<sub><s>sh dont tell anyone but this is just an edit of [this](https://github.com/Lautenschlager-id/Transfromage/blob/master/README.md) readme</s></sub>

**Transformice's API written in Python 3.6 using threads**

## About

[Transformice](https://www.transformice.com/) is an online independent multiplayer free-to-play platform video game created by the french company [Atelier801](http://societe.atelier801.com/).

**TransFromage API** is a [documented API](https://github.com/Tocutoeltuco/transfromage/tree/master/docs) that allows developers to make bots for the mentioned game.

Join the **_[Fifty Shades of Lua](https://discord.gg/quch83R)_** [discord](https://discordapp.com/) to discuss about this API and to have special support.

This API had many indirect contributors, including [@Lautenschlager-id](https://github.com/Lautenschlager-id), [@Turkitutu](https://github.com/Turkitutu) and [@Athesdrake](https://github.com/Athesdrake).

## Keys Endpoint

This API depends on an [endpoint](https://api.tocu.tk/get_transformice_keys.php) that gives you access to the Transformice encryption keys.

To get access to it you need to request a token, after explaining your project, to one of the following players:
- **[Tocutoeltuco](https://github.com/Tocutoeltuco)** @discord=> `Tocutoeltuco#0018`;
- **[tlbl4nk](https://github.com/tlbl4nk)** @discord=> `󠂪󠂪 󠂪󠂪 󠂪󠂪󠂪󠂪 󠂪󠂪 󠂪󠂪󠂪󠂪 󠂪󠂪 󠂪󠂪#8737`;
- **[Bolodefchoco](https://github.com/Lautenschlager-id)** @discord=> `Lautenschlager#2555`.

## Installation

- The module is in the PyPI so all you need to run is `pip install --upgrade transfromage`

### API Update

To update the api all you need to do is run the same installation command.

### Contribution

The best way to contribute for this API is creating pull requests with bug fixes and new events / methods (like joining the map editor, getting a map XML, loading Lua...)

## Base example

```Python
import transfromage

client = transfromage.Client()

@client.event
def on_ready():
	client.login("Username#0000", "password", "start room")

client.start("Owner ID", "API Token")
```
