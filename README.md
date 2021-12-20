# holy_greetings
Dircord-Bot to add automatic customizable greetings over voice chat if someone joining the server.
## 1. Init
1. <code>pip install requirements.txt</code>
2. Get a token and give the bot access to your Discord (see: https://www.writebots.com/discord-bot-token/).
3. After getting the token, run: <code>python main.py [insert token]</code>
## 2. Usage
After the Init section the bot is ready and should have joined your Discord (with the name you specified in **1.2**). Begin now to add your customized greetings. 
Be aware that no greetings are defined initially, so you have to add some before it is going to work. See the commands of the bot below. 
- <code>!info [Optional: user id]</code>:  
  Print out the saved greetings for the given user id. If no user id is specified it prints the greetings for the *unknown user*.[^1]
- <code>!add [new greeting] [Optional: user id]</code>:  
  Adds the given greeting to the already saved ones of the given user id. If no user id is specified add it to *unknown user*.
- <code>!add [greeting] [Optional: user id]</code>:  
  Drops the given greeting from the already saved ones of the given user. If no user id is specified drop from *unknown user*.
  
  [^1]: Every user for whom no greets are defined.
