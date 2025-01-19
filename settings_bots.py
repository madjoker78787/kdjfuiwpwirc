from bots.tiny_verse.work import tiny_verse_func
from bots.kitty_verse.work import kitty_verse_func

lst_bots = {
    # "tiny_verse": {
    #     "table_name": "tiny_verse",
    #     "delay": 1,
    #     "url": "https://t.me/tverse?startapp",
    #     "dev": False,
    #     "function": tiny_verse_func,
    #     "override": {
    #         "type": "None",
    #         "file": "",
    #         "text": ""
    #     }
    # },
    "kitty_verse": {
            "table_name": "kitty_verse",
            "delay": 1,
            "url": "https://t.me/kittyverse_ai_bot/play?startapp=u195901573",
            "dev": True,
            "function": kitty_verse_func,
            "override": {
                        "type": "replace",
                        "location": "html",
                        "file": "index-",
                        "text": "if(isDesktopPlatform()), if(!isDesktopPlatform())"
                    }
        }
    # "paws_bot": {
    #     "table_name": "paws_bot",
    #     "delay": 60 * 24,
    #     "url": "https://t.me/PAWSOG_bot/PAWS?startapp",
    #     "dev": False,
    #     "function": tiny_verse_func
    # }
}

# "name": {
#         "table_name": "name",
#         "delay": 60,
#         "url": "https://t.me/",
#         "dev": False,
#         "function": name_function
#         "override": {
#                     "type": "replace", #replace, remove, none
#                     "location": "" #html request
#                     "file": "index-",
#                     "text": '''!== mobile,==mobile'''  #''' текст ''' "текст1, текст2"
#                 }
#     }


# for bot_name, bot_info in lst_bots.items():
#     print('bot_name: ', bot_name)
#     print('table_name: ', bot_info['table_name'])
#     print('delay: ', bot_info['delay'])
#     print('url: ', bot_info['url'])
#     print('dev: ', bot_info['dev'])
#     print('function: ', bot_info['function'])
#     override_info = bot_info.get("override")
#     print('type: ', override_info['type'])
#     print('file: ', override_info['file'])
#     print('text: ', override_info['text'])