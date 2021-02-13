import telebot
import glob
import json

bot = telebot.TeleBot('1762338268:AAGZ-sXVZjHK9nm2nEXSgBPIbxZxEdUwTWA')

skipped = 0

currentProfile = ''
settingLikes = False

@bot.message_handler(commands = ['get_post'])
def get_post(message):
    check_owner(message)
    global skipped
    bot.send_chat_action(message.chat.id, 'typing')

    filename = glob.glob('telegram_bot/db_proto/content/*.mp4')[0]
    video = open(filename, 'rb')
    bot.send_video(message.chat.id, video)
    skipped += 1

@bot.message_handler(commands = ['add_profile'])
def add_profile(message):
    check_owner(message)
    bot.send_chat_action(message.chat.id, 'typing')

    with open('telegram_bot/db_proto/profiles.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        data['profiles'].append({'name': message.text.split()[1], 'likes': 0})

    with open('telegram_bot/db_proto/profiles.json', 'w') as jsonFile:
        json.dump(data, jsonFile)

    bot.reply_to(message, '*profile added*')
    

@bot.message_handler(commands = ['remove_profile'])
def remove_profile(message):
    check_owner(message)
    bot.send_chat_action(message.chat.id, 'typing')

    found = False
    with open('telegram_bot/db_proto/profiles.json', 'r') as jsonFile:
        data = json.load(jsonFile)         
        for i in range(len(data['profiles'])):
            if data['profiles'][i]['name'] == message.text.split()[1]:
                found = True
                data['profiles'].pop(i)
                break
        
    if found:
        with open('telegram_bot/db_proto/profiles.json', 'w') as jsonFile:
            json.dump(data, jsonFile)

        bot.reply_to(message, '*profile removed*')
    else:
        bot.reply_to(message, '*profile not found*')

@bot.message_handler(commands = ['set_likes'])
def set_likes(message):
    global settingLikes
    check_owner(message)
    bot.send_chat_action(message.chat.id, 'typing')
    settingLikes = True
    bot.reply_to(message, '*write the profile name*')

@bot.message_handler()
def test_message_handler(message):
    global settingLikes, currentProfile
    check_owner(message)
    if settingLikes:
        if message.text == '':
            settingLikes = False
            currentProfile = False
            bot.reply_to(message, 'input cannot be empty')
            exit()

        if currentProfile == '':
            currentProfile = message.text
            bot.reply_to(message, 'write likes')
        else:
            found = False
            with open('telegram_bot/db_proto/profiles.json', 'r') as jsonFile:
                data = json.load(jsonFile)
                for profile in data['profiles']:
                    if (profile["name"] == currentProfile):
                        found = True
                        profile["likes"] = message.text
                        break
            
            settingLikes = False
            currentProfile = False
            if found:
                with open('telegram_bot/db_proto/profiles.json', 'w') as jsonFile:
                    json.dump(data, jsonFile)

                bot.reply_to(message, 'likes set')
            else:
                bot.reply_to(message, 'profile not found')
    else:
        bot.reply_to(message, 'message_handler invoked')




def check_owner(message):
    if message.from_user.username != 'troobadure':
        warning = ('!!!STRANGER DETECTED!!!\n'
        'username={0} chat_id={1}').format(message.chat.username, message.chat.id)
        print(warning)
        bot.send_message('402027899', warning)
        bot.stop_polling()
        exit()

# with open('telegram_bot/db_proto/profiles.json', 'r') as jsonFile:
#     data = json.load(jsonFile)

#     data['profiles'].append({'name': 'name2', 'likes': 0})

#     for profile in data['profiles']:
#         if (profile["name"] == 'name2'):
#             profile["likes"] = 5
#             break

#     with open('telegram_bot/db_proto/profiles.json', 'w') as jsonFile:
#         json.dump(data, jsonFile)
bot.polling(none_stop = True)