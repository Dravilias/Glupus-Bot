import database
import config

def checkMessage(message):
    # need this for bot.py
    detected = []
    # emoji check
    count = message.content.count(config.GLUP_EMOJI)
    if count > 0:
        for i in range(count):
            database.add_count("glup_emoji")
        detected.append("glup_emoji")

    # gif check
    if config.GLUP_GIF in message.content:
        database.add_count("glup_gif")
        detected.append("glup_gif")
    
    # sticker check
    for sticker in message.stickers:
        if sticker.id == config.GLUP_STICKER:
            database.add_count("glup_sticker")
            detected.append("glup_sticker")

    return detected
