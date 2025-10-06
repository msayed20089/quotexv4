from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram
import logging
import random
from datetime import datetime
from config import UTC3_TZ, TELEGRAM_TOKEN, CHANNEL_ID, QX_SIGNUP_URL

class TelegramBot:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.channel_id = CHANNEL_ID
        self.signup_url = QX_SIGNUP_URL
        try:
            self.bot = telegram.Bot(token=self.token)
            logging.info("✅ تم تهيئة بوت التليجرام بنجاح")
        except Exception as e:
            logging.error(f"خطأ في تهيئة بوت التليجرام: {e}")
            self.bot = None
    
    def get_utc3_time(self):
        """الحصول على وقت UTC+3"""
        return datetime.now(UTC3_TZ).strftime("%H:%M:00")
        
    def create_signup_button(self):
        """إنشاء زر التسجيل"""
        keyboard = [[InlineKeyboardButton("📈 سجل في كيوتكس واحصل على 30% بونص", url=self.signup_url)]]
        return InlineKeyboardMarkup(keyboard)
    
    def send_message(self, text, chat_id=None):
        """إرسال رسالة مع زر التسجيل"""
        if chat_id is None:
            chat_id = self.channel_id
            
        try:
            self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=self.create_signup_button(),
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            logging.info("✅ تم إرسال الرسالة بنجاح")
            return True
        except Exception as e:
            logging.error(f"❌ خطأ في إرسال الرسالة: {e}")
            return False
