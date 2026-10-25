import os
import discord
from discord.ext import commands
from keep_alive import keep_alive  # Render用のおきっぱなし機能

# ボットの準備
intents = discord.Intents.default()
intents.message_content = True  # メッセージを読むために必須
intents.members = True          # タイムアウトなどのメンバー操作に必要

bot = commands.Bot(command_prefix="!", intents=intents)

# 【ここを自分好みに変更してね！】
# NGワードのリスト（含まれていると言葉を消してタイムアウトするよ）
NG_WORDS = ["ばか", "アホ", "死ね"]

# 特定の言葉と、それに返信するGIFのURLの組み合わせ
TRIGGER_GIFS = {
    "おはよう": "https://media.giphy.com/media/3oKIPnAiaMCws8nOsE/giphy.gif",
    "お疲れ": "https://media.giphy.com/media/l0HlVJw6nEXzd3rsY/giphy.gif"
}

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user.name}")

@bot.event
async def on_message(message):
    # ボット自身の発言には反応しないようにする
    if message.author == bot.user:
        return

    content = message.content

    # 1. NGワードチェック
    for word in NG_WORDS:
        if word in content:
            try:
                # メッセージを削除する
                await message.delete()
                
                # 60秒間タイムアウトする（時間は秒数で自由に変えられるよ）
                from datetime import timedelta
                time_duration = timedelta(seconds=60)
                await message.author.timeout(time_duration, reason="NGワードの発言のため")
                
                # 警告メッセージを送る
                await message.channel.send(f"{message.author.mention}さん、NGワードが含まれていたため60秒間のタイムアウトにしました。")
            except Exception as e:
                print(f"エラーが発生しました: {e}")
            return  # NGワードが見つかったらここで処理を終わる

    # 2. 特定の言葉に反応してGIFを送るチェック
    for keyword, gif_url in TRIGGER_GIFS.items():
        if keyword in content:
            await message.channel.send(gif_url)
            return

    # これがないと、ほかのコマンド（もし追加した場合）が動かなくなるよ
    await bot.process_commands(message)

# ボットを起動（DiscordのパスワードはRenderの「環境変数」から読み込むよ）
keep_alive()  # Render用サーバーを起動
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)