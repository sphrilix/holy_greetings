# holy_greetings
Discord-Bot to add automatic customizable greetings over voice chat if someone joining the server.
## 1. Init
1. <code>pip install -r requirements.txt</code>
2. Get a token and give the bot access to your Discord (see: https://www.writebots.com/discord-bot-token/). You also have to specify the privileges of the bot. The easiest way is to give him administrator rights. He does not require the full range of this privileges to work, so you can specify more precisely what actually satisfy the needs. The bots must be able to access events, chat and also voice-chat.
3. After getting the token, run: <code>python main.py</code>
4. This should start a webserver on `port: 8080` in the local network.
5. On the first start there you have to enter the gained token and click on start. (Since the config is not deleted the bot starts every time on `main.py` is run.)
6. Also on this configuration page you can specify more behaviour of the bot.
## 2. Usage
After the Init section, the bot is ready and should have joined your Discord (with the name you specified in **1.2**). Begin now to add your customized greetings through typing the commands in any text-channel. 
Be aware that no greetings are defined initially, so you have to add some before it is going to work. See the commands of the bot below. 
- <code>!info -u [Optional: user id]</code>:  
  Print out the saved greetings for the given user id. If no user id is specified, it prints the greetings for the *unknown user*[^1].
- <code>!add -m [new greeting] -u [Optional: user id] -l [Optional: language abbreviation] -o [Optional: START, END, ONLY]</code>:  
   Adds the given greeting in the specified language to the already saved ones of the given user id. If no user id is specified, add it to *unknown user*. You also
   can now play a sound before/after a greet, or only the sound as greet. This can be achieved by appending a `.mp3`to the message.  
- <code>!drop -m [greeting] -u [Optional: user id]</code>:  
  Drops the given greeting from the already saved ones of the given user. If no user id is specified, drop from *unknown user*.
- <code>!lang</code>:  
  Print out the supported languages and their corresponding abbreviation used by the bot.
  
[^1]: Every user for whom no greets are defined.
