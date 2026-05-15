# helper/utils.py

import math
import time
import aiohttp
from config import Txt
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# throttle threshold: 100 MiB
_THROTTLE_BYTES = 100 * 1024 * 1024
_THROTTLE_SECONDS = 2
_last_update: dict[int, int] = {}
_last_update_time: dict[int, float] = {}
_low_speed_hits: dict[int, int] = {}

async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message: Message,
    start,
    min_speed_bps: float = 0.0,
    grace_seconds: int = 20,
):
    """
    Progress callback for pyrogram download/upload operations.
    Handles None message gracefully.
    """
    # If message is None, skip progress updates
    if message is None:
        return
    
    now = time.time()
    diff = now - start

    # Use message.id for tracking
    msg_id = getattr(message, 'id', None)
    if msg_id is None:
        # If message doesn't have id, skip progress update
        return
    
    last = _last_update.get(msg_id, 0)
    
    # Only update if enough data/time passed or if transfer is complete
    last_t = _last_update_time.get(msg_id, start)
    if (current - last >= _THROTTLE_BYTES) or ((now - last_t) >= _THROTTLE_SECONDS) or (current >= total):
        _last_update[msg_id] = current
        _last_update_time[msg_id] = now

        percentage = current * 100 / total if total else 0
        speed = current / diff if diff > 0 else 0
        elapsed_ms = round(diff) * 1000
        eta_ms = (round((total - current) / speed) * 1000) if speed > 0 else 0
        total_eta_ms = elapsed_ms + eta_ms

        elapsed_str = TimeFormatter(elapsed_ms)
        eta_str = TimeFormatter(total_eta_ms)

        # Build progress bar
        filled = math.floor(percentage / 5)
        bar = "▣" * filled + "▢" * (20 - filled)

        tmp = bar + Txt.PROGRESS_BAR.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            eta_str or "0 s"
        )

        try:
            await message.edit(
                text=f"{ud_type}\n\n{tmp}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("✖️ 𝖢𝖺𝗇𝖼𝖾𝗅 ✖️", callback_data="close")]]
                )
            )
        except Exception as e:
            # Silently ignore edit errors (message might be deleted, etc.)
            print(f"[DEBUG] Progress update failed: {e}")

        # Guardrail for consistently slow transfers (monitor-only; never abort transfer)
        if min_speed_bps > 0 and current < total and diff >= grace_seconds:
            if speed < min_speed_bps:
                _low_speed_hits[msg_id] = _low_speed_hits.get(msg_id, 0) + 1
            else:
                _low_speed_hits[msg_id] = 0

            # Track low-speed streak for observability in logs
            if _low_speed_hits.get(msg_id, 0) >= 3:
                print(
                    "[WARN] Transfer speed is below threshold for multiple checks: "
                    f"{humanbytes(speed)}/s < {humanbytes(min_speed_bps)}/s"
                )
                _low_speed_hits[msg_id] = 0

        # Clean up tracking when complete
        if current >= total:
            _last_update.pop(msg_id, None)
            _last_update_time.pop(msg_id, None)
            _low_speed_hits.pop(msg_id, None)


def humanbytes(size):
    """Convert bytes to human readable format"""
    if not size:
        return ""
    power = 2**10
    n = 0
    units = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power and n < 4:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}B"


def TimeFormatter(ms: int) -> str:
    """Format milliseconds to human readable time string"""
    secs, ms = divmod(ms, 1000)
    mins, secs = divmod(secs, 60)
    hrs, mins = divmod(mins, 60)
    days, hrs = divmod(hrs, 24)
    
    parts = []
    if days:
        parts.append(f"{days}d")
    if hrs:
        parts.append(f"{hrs}h")
    if mins:
        parts.append(f"{mins}m")
    if secs:
        parts.append(f"{secs}s")
    if ms and not parts:  # Only show ms if no larger units
        parts.append(f"{ms}ms")
    
    return ", ".join(parts) if parts else "0s"


async def download_thumbnail(image_url, save_path):
    """Asynchronously download an image to save_path."""
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(image_url, timeout=30) as resp:
                if resp.status == 200:
                    with open(save_path, 'wb') as f:
                        while True:
                            chunk = await resp.content.read(1024 * 1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    return save_path
    except Exception as e:
        print(f"[ERROR] Thumbnail download failed: {e}")
    return None
