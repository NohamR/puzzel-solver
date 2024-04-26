import json
from pprint import pprint
import websocket

def decode_sentence(sentence):
    decoded_words = []
    words = sentence.split()
    for word in words:
        try:
            decoded_word = word.encode('latin1').decode('utf-8')
            decoded_words.append(decoded_word)
        except UnicodeDecodeError:
            decoded_words.append(word)
    return ' '.join(decoded_words)

pageid = '-NwO-VUAR1gKHH_buvut'

ws = websocket.WebSocket()
ws.connect("wss://s-usc1b-nss-2107.firebaseio.com/.ws?v=5&ns=puzzelorg")

initial_message = ws.recv()

request_message = {"t": "d", "d": {"r": 3, "a": "g", "b": {"p": f"/index/{pageid}", "q": {}}}}
ws.send(json.dumps(request_message))
response = ws.recv()
id = json.loads(response)['d']['b']['d']

request_message = {"t":"d","d":{"r":7,"a":"g","b":{"p":f"/fields/{id}/{pageid}","q":{}}}}
ws.send(json.dumps(request_message))
nbres = ws.recv()
mess = ''
for i in range(len(nbres)+1):
    mess += ws.recv()
ws.close()

dict = json.loads(mess)

answers = dict['d']['b']['d']['grid']

def getanswer(x,y):
    try :
        return answers[f'{y}'][f'{x}'].encode('latin1').decode('utf-8')
    except:
        return answers[f'{y}'][f'{x}']

words = dict['d']['b']['d']['wordsPlaced']
for i in range(len((dict['d']['b']['d']['wordsPlaced']))):
    desc = words[f'{i}']['description']
    word = ''
    for j in range(len(words[f'{i}']['coords'])):
        word += getanswer(words[f'{i}']['coords'][f'{j}']['1'], words[f'{i}']['coords'][f'{j}']['0'])

    print(f'{i+1} : {decode_sentence(desc)} : ||{word}||')