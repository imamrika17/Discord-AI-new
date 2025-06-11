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
DISCORD_USER_TOKEN = "MTA4MDAzNzgwMTU4NTgwNzQzMg.Gf58xM.RSt4eHwW0JvmULFRkdJ6_DEaMN5yemPjQjSqEk"
CHANNEL_ID = 1027161980970205225
INTERVAL_MENIT = 2  # Cooldown antar balasan bot (menit)
NO_REPLY_TIMEOUT = 3  # Menit untuk menunggu sebelum balas chat acak
MIN_MESSAGE_LENGTH = 2  # Panjang minimal pesan untuk dibalas (karakter)
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3:8b"
MAX_STORED_MESSAGES = 50  # Batas pesan yang disimpan

# === State ===
last_response_time = datetime.min  # Waktu terakhir bot membalas
last_reply_to_me = datetime.min   # Waktu terakhir seseorang balas ke bot
pending_messages = {}  # Dictionary untuk pesan yang menunggu balasan
recent_messages = []   # List untuk pesan terbaru di channel

# Inisialisasi client sebagai selfbot
client = commands.Bot(command_prefix="!", self_bot=True)

# === Fungsi ambil jawaban dari AI lokal (Ollama) ===
async def get_ai_reply(prompt):
    try:
        crypto_prompt = (
             "You are a friendly, humble and intelligent person from Indonesia who is in the Momentum community looking to level up by greeting more people. "
"Respond with short, concise sentences like a beginner, showing curiosity or basic understanding. "
"Use a relaxed and human tone, stay polite, keep replies very short, 8 words max. "
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
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [❌] Error Ollama: {e}")
        return "Oops, belajar dulu ya!"

# === Event ketika bot siap ===
@client.event
async def on_ready():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [✅] Login sebagai {client.user} (akun pribadi aktif)")
    reply_loop.start()
    random_reply_loop.start()

# === Event ketika pesan baru diterima ===
@client.event
async def on_message(message: Message):
    global pending_messages, last_reply_to_me, recent_messages
    if message.channel.id != CHANNEL_ID:
        return
    if message.author.id == client.user.id:
        return
    
    # Simpan pesan terbaru untuk potensi balasan acak
    recent_messages.append({"message": message, "timestamp": datetime.now()})
    # Hapus pesan lama (lebih dari 10 menit) atau jika melebihi batas
    recent_messages = [
        m for m in recent_messages 
        if (datetime.now() - m["timestamp"]).total_seconds() < 600  # 10 menit
    ][-MAX_STORED_MESSAGES:]
    
    # Cek jika pesan adalah balasan ke bot
    if message.reference and message.reference.resolved and message.reference.resolved.author.id == client.user.id:
        pending_messages[message.author.id] = message
        last_reply_to_me = datetime.now()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [📥] Pesan balasan dari {message.author.name}: {message.content}")

# === Loop interval kirim balasan ke pesan yang membalas bot ===
@tasks.loop(seconds=10)
async def reply_loop():
    global last_response_time, pending_messages

    if not pending_messages:
        return

    now = datetime.now()
    if now - last_response_time < timedelta(minutes=INTERVAL_MENIT):
        return

    for author_id, message in list(pending_messages.items()):
        reply = await get_ai_reply(message.content)
        try:
            await message.reply(reply)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [✅] Balas ke {message.author.name}: {reply}")
            last_response_time = now
            del pending_messages[author_id]  # Hapus setelah balas
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [❌] Gagal kirim ke {message.author.name}: {e}")

# === Loop interval kirim balasan acak jika tidak ada balasan ke bot ===
@tasks.loop(seconds=10)
async def random_reply_loop():
    global last_response_time, last_reply_to_me, recent_messages

    now = datetime.now()
    # Cek jika belum ada balasan ke bot selama NO_REPLY_TIMEOUT menit
    if now - last_reply_to_me < timedelta(minutes=NO_REPLY_TIMEOUT):
        return
    # Cek interval minimal antar balasan bot
    if now - last_response_time < timedelta(minutes=INTERVAL_MENIT):
        return
    # Pastikan ada pesan yang layak untuk dibalas
    if not recent_messages:
        return

    # Pilih pesan terbaru yang valid (bukan dari bot, cukup panjang)
    for entry in reversed(recent_messages):
        message = entry["message"]
        if (message.author.id != client.user.id and 
            message.content and 
            len(message.content) >= MIN_MESSAGE_LENGTH):
            reply = await get_ai_reply(message.content)
            try:
                await message.reply(reply)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [✅] Balas acak ke {message.author.name}: {reply}")
                last_response_time = now
                break  # Hanya balas satu pesan per loop
            except Exception as e:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [❌] Gagal kirim balasan acak ke {message.author.name}: {e}")
                break

# === Jalankan bot ===
client.run(DISCORD_USER_TOKEN)
