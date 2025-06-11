# Discord-AI-new From Malikendgame

# sistem Requarements
- 4 core cpu
- 8GB ram
  
# Fitur
- auto chat with AI
- Untuk Push level Dscord

**buat screen**
```
sudo apt update && sudo apt install screen
```
```
screen -S AI
```
**install AI lokal**
```
curl -fsSL https://ollama.com/install.sh | sh
```
```
ollama serve
```
```
ollama pull llama3:8b
```
**Keluar screen AI**
- crtl a+d

**buat screen discord**
```
screen -S discord
```
**Install Script**
```
git clone https://github.com/imamrika17/Discord-AI-new.git
cd Discord-auto-with-AI
```
Buat environtment
```
python3 -m venv dc
source dc/bin/activate
```
**install bahan**
```
pip3 install -r requirements.txt
```
```
pip uninstall discord discord.py discord.py-self -y
```
```
pip install git+https://github.com/dolfies/discord.py-self@71609f4f62649d18bdf14f0e286b7e62bc605390
```
**buka script**
```
nano bot.py
```
= isi TOKEN DC & channel ID target (tutorial token : https://www.youtube.com/watch?v=zyl6VGTJ4fY)

= klik ctrl + x -> klik y -> klik enter (untuk keluar)

**Mainkan script**
```
python3 bot.py
```
## Fungsi tambahan
masuk screen AI
```
screen -r AI
```
masuk screen discord
```
screen -r discord
```
## DISCLAIMER
Gunakan dengan bijak, semua risiko dan tanggung jawab ada di tangan pengguna.

## Support malik

## ☕ Donate for Coffee

**EVM Address**  
`0xe462A37f81Fc497F847866e2F7e0d7C4F5ef32d5`

**SOL Address**  
`AjdZNqh9jAnakHYxNx3FZ44amseoePTt3i9tHBmMp31R`

---
© 2025 Airdrop Sambil Rebahan. All rights reserved.
