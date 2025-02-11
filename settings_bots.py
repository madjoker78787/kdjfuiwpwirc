from bots.tiny_verse.work import tiny_verse_func
from bots.kitty_verse.work import kitty_verse_func
from bots.gold_eagle.work import gold_eagle_func
from bots.trump_farm.work import trump_farm_func

lst_bots = {
    "tiny_verse": {
        "is_work": False,
        "table_name": "tiny_verse",
        "delay": 1,
        "url": "https://t.me/tverse?startapp",
        "dev": False,
        "function": tiny_verse_func,
        "override": {
            "type": "None",
            "file": "",
            "text": ""
        }
    },
    "kitty_verse": {
        "is_work": False,
        "table_name": "kitty_verse",
        "delay": 30,
        "url": "https://t.me/kittyverse_ai_bot/play?startapp=u195901573",
        "dev": True,
        "function": kitty_verse_func,
        "override": {
            "type": "replace",
            "location": "html",
            "file": "index-",
            "text": "if(isDesktopPlatform()), if(!isDesktopPlatform())"
        }
    },
    "gold_eagle": {
        "is_work": False,
        "table_name": "gold_eagle",
        "delay": 60,
        "url": "https://t.me/gold_eagle_coin_bot/main?startapp=r_X1qqHVeqRf",
        "dev": False,
        "function": gold_eagle_func,
        "override": {
            "type": "None",  #replace, remove, None
            "location": "",  #html request
            "file": "",
            "text": ""  #''' текст ''' "текст1, текст2"
        }
    },
    "trump_farm": {
        "table_name": "trump_farm",
        "delay": 60,
        "url": "https://t.me/TrumpFarmBot/app?startapp=62b5d1c7-5e96-4af9-8278-9a367810e4c3",
        "dev": False,
        "function": trump_farm_func,
        "override": {
            "type": "None",  #replace, remove, None
        }
    }
}

# "name": {
#         "table_name": "name",
#         "delay": 60,
#         "url": "https://t.me/",
#         "dev": False,
#         "function": "name_function",
#         "override": {
#             "type": "replace",  #replace, remove, None
#             "location": "",  #html request
#             "file": "index-",
#             "text": '''!== mobile,==mobile'''  #''' текст '' "текст1, текст2"
#         }
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
