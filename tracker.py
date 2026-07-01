import database
import config

def checkMessage(message):
    # need this for bot.py
    detected = []
    
    # glup emoji
    count = message.content.count(config.GLUP_EMOJI)
    if count > 0:
        for i in range(count):
            database.add_count("glup_emoji")
        detected.append("glup_emoji")
    
    # glup gif
    if config.GLUP_GIF in message.content:
            database.add_count("glup_gif")
            detected.append("glup_gif")

    # glup sticker
    for sticker in message.stickers:
        if sticker.id == config.GLUP_STICKER:
            database.add_count("glup_sticker")
            detected.append("glup_sticker")

    # steamhappy emojig
    count = message.content.count(config.STEAMHAPPY_EMOJI)
    if count > 0:
        for i in range(count):
            database.add_count("steamhappy_emoji")
        detected.append("steamhappy_emoji")

    # steamhappy gif 
    if "klipy.com" in message.content and config.STEAMHAPPY_GIF in message.content:
        database.add_count("steamhappy_gif")
        detected.append("steamhappy_gif")          

    for attachment in message.attachments:
        if config.STEAMHAPPY_GIF in attachment.filename.lower():
            database.add_count("steamhappy_gif")
            detected.append("steamhappy_gif")

    return detected
