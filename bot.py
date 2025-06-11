import os
import time
import asyncio
import requests
from datetime import datetime, timedelta
from discord.ext import tasks, commands
from discord import Message

print(r'''
                      .^!!^.
                  .:~7?7!7??7~:.
               :^!77!~:..^^~7?J?!^.
           .^!7??!^..  ..^^^^^~JJJJ7~:.
           7?????: ...^!7?!^^^~JJJJJJJ?.
           7?????:...^???J7^^^~JJJJJJJJ.
           7?????:...^??7?7^^^~JJJJJJJ?.
           7?????:...^~:.^~^^^~JJJJJJJ?.
           7?????:.. .:^!7!~^^~7?JJJJJ?.
           7?????:.:~JGP5YJJ?7!^^~7?JJ?.
           7?7?JY??JJ5BBBBG5YJJ?7!~7JJ?.
           7Y5GBBYJJJ5BBBBBBBGP5Y5PGP5J.
           ^?PBBBP555PBBBBBBBBBBBB#BPJ~
              :!YGB#BBBBBBBBBBBBGY7^
                 .~?5BBBBBBBBPJ~.
                     :!YGGY7:
                        ..

 🚀 join channel Airdrop Sambil Rebahan : https://t.me/kingfeeder
''')

# === Konfigurasi ===
DISCORD_USER_TOKEN = "your_discord_token"
CHANNEL_ID = ISI channel ID
INTERVAL_MENIT = 3
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3:8b"

# === State ===
last_response_time = datetime.min
pending_message = None

# Inisialisasi client sebagai selfbot
client = commands.Bot(command_prefix="!", self_bot=True)

# === Fungsi ambil jawaban dari AI lokal (Ollama) ===
async def get_ai_reply(prompt):
    try:
        crypto_prompt = (
            "You are a chill and lazy friend replying to a message with a short, casual sentence. "
            "No formal tone, no overthinking. Never repeat the question. Never add explanation. "
            "Sometimes add 'yeah', 'lol', 'same', 'true', etc. Keep it random.\n\n"
            f"Message: {prompt}\n"
            "Reply:"
        )

        response = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": OLLAMA_MODEL,
            "prompt": crypto_prompt,
            "stream": False
        })
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except Exception as e:
        print(f"[❌] Error Ollama: {e}")
        return "males ahh"

# === Event ketika bot siap ===
@client.event
async def on_ready():
    print(f"[✅] Login sebagai {client.user} (akun pribadi aktif)")
    reply_loop.start()

# === Event ketika pesan baru diterima ===
@client.event
async def on_message(message: Message):
    global pending_message
    if message.channel.id != CHANNEL_ID:
        return
    if message.author.id == client.user.id:
        return

    # print(f"[📥] Pesan dari {message.author.name}: {message.content}")
    pending_message = message

# === Loop interval kirim balasan ===
@tasks.loop(seconds=10)
async def reply_loop():
    global last_response_time, pending_message

    if not pending_message:
        return

    now = datetime.now()
    if now - last_response_time < timedelta(minutes=INTERVAL_MENIT):
        # print(f"[⏳] Tunggu {INTERVAL_MENIT} menit. Abaikan pesan dari {pending_message.author.name}")
        return

    reply = await get_ai_reply(pending_message.content)
    try:
        await pending_message.channel.send(reply)
        print(f"[✅] Balas ke {pending_message.author.name}: {reply}")
        last_response_time = now
        pending_message = None
    except Exception as e:
        print(f"[❌] Gagal kirim: {e}")

# === Jalankan bot ===
client.run(DISCORD_USER_TOKEN)
