import urllib.request
import json

output_file = "E:\\RIFT\\datamine\\livestream\\apr21-dev-chat.txt"
output_all_file = "E:\\RIFT\\datamine\\livestream\\apr21-chat.txt"
video_id = "v137137262"
timestamp_start =   1492803262 + (60 * 60 * 2) + (60 * 40)
timestamp_end =     1492817339

dev_list = ['archonix', 'dev_trion_vladd', 'dev_tacitus', 'roughraptors',
            'trionworlds', 'dev_trion_keyens', 'captaincursor', ' dev_darkmoon']

timestamp_current = timestamp_start
f = open(output_file, 'w')
fa = open(output_all_file, 'w')

while (timestamp_current < timestamp_end):
    response = urllib.request.urlopen("https://rechat.twitch.tv/rechat-messages?start=" + str(timestamp_current) + "&video_id=" + video_id)
    data = response.read()

    json_data = json.loads(data)

    for x in json_data['data']:
        if (x['type'] == 'rechat-message'):
            sent_from = ""
            message = ""
            complete = ""
            try:
                sent_from = x['attributes']['from'].lower()
                message = x['attributes']['message'].lower()
                complete = sent_from + ": " + message + "\n"

                if ((sent_from in dev_list) or any(dev_name in message for dev_name in dev_list)):
                    print(complete)
                    f.write(complete)

                fa.write(complete)
            except Exception as e:
                print(" error: ", str(e))

    timestamp_current += 30

f.close()
fa.close()
