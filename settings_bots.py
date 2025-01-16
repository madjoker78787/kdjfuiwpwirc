from bots.tiny_verse.work import tiny_verse_func

lst_bots = {
    "tiny_verse": {
        "table_name": "tiny_verse",
        "delay": 1,
        "url": "https://t.me/tverse?startapp",
        "dev": False,
        "function": tiny_verse_func
    },
    "paws_bot": {
        "table_name": "paws_bot",
        "delay": 60 * 24,
        "url": "https://t.me/PAWSOG_bot/PAWS?startapp",
        "dev": False,
        "function": tiny_verse_func
    }
}

# "name": {
#         "table_name": "name",
#         "delay": 60,
#         "url": "https://t.me/",
#         "dev": False,
#         "function": name_function
#     }
