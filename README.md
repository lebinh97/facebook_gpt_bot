I. This respiratory contains the code to run a facebook bot intergrate with ChatGPT API:

1. The name of the page that I'm using is Netflix OTP
2. You can send the message to the page, the page will send bach an immediate response using GPT API
3. The bot will remember all of your messages and its response in your previous conversation with it
4. The recipient_prompt.json file allows you to config the GPT prompt for each individual message sender (you can tell GPT to respond like a boyfriend for an individual, and act like a teacher for a different individual)

II. Respiratory structure and technical explanation

1. This bot is constructed based on facebook graph API, which allows you to get immediate notification when someone text your page using Facebook webhook
2. Then, the message of sender is send to OpenAPI for processing using GPT API, then send back to the message sender
3. Finally, I build this bot using flask, and exposed my local server using ngrok. The expose step is essential since it allows facebook to send realtime message to your local server, and to integrate with facebook

III. File in respiratory explanation

1. .gitignore => I included all the files being ignored bi git push (such as api key)
2. facebook_response.py => this is the library I constructed specifically for sending a message back to the responder in Facebook
3. gpt_api.py => this is the library I constructed specifically for getting a responde for chatgpt with the message that I have send
4. message_log.json => this is the db for all messages received, from anyones having conversation with the bot
5. recipient_prompt.json => this file is used to customize prompt for each separate message sender
