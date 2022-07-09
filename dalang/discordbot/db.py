from collections import defaultdict


class MessageDB:
    data = {}
    links = {}

    def __init__(self, guild_name: str):
        self.data[guild_name] = defaultdict(list)
        self.links[guild_name] = defaultdict(list)

    def add(self, message, guild: str):
        self.data[guild][message.channel.name].append(message)

        # if is link add to links


dbs = {}


def message_db(guild_name):
    if guild_name in dbs:
        return dbs[guild_name]

    guild_db = MessageDB(guild_name)
    dbs[guild_name] = guild_db
    return guild_db
