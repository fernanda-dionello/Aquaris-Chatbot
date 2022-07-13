# Aquaris-Chatbot

Chatbot created for a swimming school that allows students to access a menu of options and chat with other students at the same time (broadcast).

## Entities
- Bot (Server)
- Mural (Client + Mural/Chat interface + Login interface)

## Tech Stack
- Python
- Tkinter

## Architecture
![architecture drawio](https://user-images.githubusercontent.com/74319133/178811579-d74ef94a-5f74-4cc9-90df-639b0ae18cf9.png)

In Mural entity, we have the client and login interface. The login page starts first and we just connect to the server (Bot) when we press the send button in login and we're able to see the chat interface. In the client we have 2 threads, one to receive messages and another to send messages for the Bot (Server). At the same time, when we create the client connection this starts another Thread in server side for each client connected.
Ps: We can connect multiple clients at same time. In addition, all the clients can communicate in real time with a broadcast/multicast system when the chose the option in menu to talk with other students.

## Screens

### Login
<img width="300" alt="image" src="https://user-images.githubusercontent.com/74319133/178811767-89524b2f-c27f-4a24-8411-f05553a688ff.png">

### Chat
<img width="300" alt="image" src="https://user-images.githubusercontent.com/74319133/178811887-c5fbbdac-ebd6-46eb-ac7b-923d6d0ea500.png">

## How to start
- Clone the project
- First run `python3 Bot.py` in your terminal (if you have python3, if not just python should work)
- Then, run `python3 Mural.py` in a new terminal 

