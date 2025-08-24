# NBA Prediction Line Bot 🏀🤖

A **LINE messaging bot** that provides NBA game predictions, player stats, and team insights.  
Built with **Python**, deployed on **Vercel**, and backed by **Neon (Postgres)** and **Vercel Blob Storage**.

---

## 🚀 Features
- 🏀 NBA team and player prediction engine.  
- 📊 Stores and manages data using Postgres (Neon).  
- ☁️ Cloud-deployed via Vercel for seamless performance.  
- 💬 Interactive LINE Bot interface.  

---

## 📦 Installation & Deployment

### 1. Create a LINE Bot
1. Register and login at [LINE Developers Console](https://developers.line.biz/console/).  
2. Create a **Provider**.  
3. Create a **Channel** under the Provider (choose **Messaging API**).  
4. Go to **LINE Official Account Manager** to manage your Bot Account.  

🔗 Reference Guide: [Oxxo Studio - LINE Developer Setup](https://steam.oxxostudio.tw/category/python/example/line-developer.html)  

---

### 2. Clone Repository
```bash
git clone https://github.com/MikeTai1218/NBA-Prediction-Line-Bot.git
cd NBA-Prediction-Line-Bot
# You need to push it onto your own repository
git remote set-url origin <your-repo-url>
git push -u origin main
```

### 3. Set up Vercel Project

1. [Sign up / Log in to Vercel](https://vercel.com/).  
2. Create a new **Project** by importing your GitHub repository.  
3. Add environment variables under  
   **Project Settings → Environment Variables**  
   (see `config.py` for the required keys).  

### 4. Database & Storage Setup

- **Vercel Blob**: used for static assets (e.g., logos, images).  
- **Neon DB (Postgres)**: used for NBA data storage.  

Initialize the database:
```bash
python tools/build_table.py
python tools/player_link.py
```

## ⚙️ Configuration

Update `config.py` with your credentials:

```python
LINE_BOT_API = "your_line_access_token"
HANDLER = "your_line_channel_secret"
GITHUB_NAME = "your_github_username"
DATABASE_URL = "your_neon_postgres_url"
```

## ⚠️ Disclaimer

This project is created **solely for fun and educational purposes**.  
It has **no commercial intent** and is **not affiliated with, endorsed, or sponsored by the NBA, LINE, or any related organization**.
