import os
import time
import re

# Regular expression to validate ID format
id_pattern = re.compile(r'^\d+$')

class Config(object):
    # Pyrogram client config
    API_ID = os.environ.get("API_ID", "")
    API_HASH = os.environ.get("API_HASH", "")
    
    # Fixing BOT_TOKENS extraction from environment
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # Database config
    DB_NAME = os.environ.get("DB_NAME", "Cluster0")
    DB_URL = os.environ.get("DB_URL", "")
    BOT_UPTIME = time.time()
    GLOBAL_THUMBNAIL_URL = os.environ.get("GLOBAL_THUMBNAIL_URL", "https://i.ibb.co/MDwd1f3D/6087047735061627461.jpg")
    START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/MDwd1f3D/6087047735061627461.jpg")
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1892771262').split()]

    # Channels logs
    FORCE_SUB = os.environ.get("FORCE_SUB", "")
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002345447637"))

    # Webhook response configuration     
    WEBHOOK = bool(int(os.environ.get("WEBHOOK", True)))
    PORT = os.environ.get("PORT", "8080") # Use 1 for True (instead of True/False)
    MAX_CONCURRENT_DOWNLOADS = int(os.environ.get("MAX_CONCURRENT_DOWNLOADS", "3"))
    MAX_CONCURRENT_UPLOADS = int(os.environ.get("MAX_CONCURRENT_UPLOADS", "3"))
    MIN_TRANSFER_SPEED_MBPS = float(os.environ.get("MIN_TRANSFER_SPEED_MBPS", "4"))
    SPEED_CHECK_GRACE_SECONDS = int(os.environ.get("SPEED_CHECK_GRACE_SECONDS", "20"))
class Txt(object):
    PROGRESS_BAR = """
**{0}%**
**Done:** {1}
**Total:** {2}
**Speed:** {3}/s
**ETA:** {4}
"""

    START_TEXT = """
👋 **Hello {0}!**
I am a File Rename Bot. Send me any file and I'll rename it for you.
"""

    HELP_TEXT = """
**Available Commands:**
/start - Start the bot
/help - Show this help message
/about - About this bot
"""

    ABOUT_TEXT = """
**About This Bot**
• **Bot:** File Rename Bot
• **Language:** Python 3
• **Framework:** Pyrogram
"""

    WAIT_MSG = "**Processing...**"
    DOWNLOAD_START = "**Downloading...**"
    UPLOAD_START = "**Uploading...**"
    DOWNLOAD_COMPLETE = "**Download complete! Now uploading...**"
    UPLOAD_COMPLETE = "**Upload complete!** ✅"
    ERROR_MSG = "**An error occurred:** `{}`"
    FILE_TOO_LARGE = "**File too large!** Maximum allowed size is {} GB."
    NO_THUMB = "**No thumbnail set.** Send a photo to set a thumbnail."
    THUMB_SET = "**Thumbnail saved successfully!** ✅"
    THUMB_DELETED = "**Thumbnail deleted successfully!** ✅"
