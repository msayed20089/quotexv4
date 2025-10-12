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
        self.group_id = "@Alahly_Bank"  # تم إضافة ID الجروب
        self.signup_url = QX_SIGNUP_URL
        self.tutorial_url = "https://t.me/Kingelg0ld/3802"  # تم إضافة رابط الشرح
        try:
            self.bot = telegram.Bot(token=self.token)
            logging.info("✅ تم تهيئة بوت التليجرام بنجاح")
        except Exception as e:
            logging.error(f"خطأ في تهيئة بوت التليجرام: {e}")
            self.bot = None
    
    def get_utc3_time(self):
        """الحصول على وقت UTC+3"""
        return datetime.now(UTC3_TZ).strftime("%H:%M:00")
        
    def create_keyboard_buttons(self):
        """إنشاء أزرار التسجيل والشرح"""
        keyboard = [
            [InlineKeyboardButton("📈 سجل في كيوتكس واحصل على 30% بونص", url=self.signup_url)],
            [InlineKeyboardButton("📖 كيفية التداول ودخول الصفقة", url=self.tutorial_url)]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def send_message(self, text, chat_id=None, send_to_group=False):
        """إرسال رسالة مع أزرار التسجيل والشرح"""
        try:
            # إرسال للقناة الأساسية
            if chat_id is None:
                chat_id = self.channel_id
                
            self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=self.create_keyboard_buttons(),
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            logging.info("✅ تم إرسال الرسالة للقناة بنجاح")
            
            # إرسال للجروب إذا كان مطلوب
            if send_to_group:
                self.bot.send_message(
                    chat_id=self.group_id,
                    text=text,
                    reply_markup=self.create_keyboard_buttons(),
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )
                logging.info("✅ تم إرسال الرسالة للجروب بنجاح")
                
            return True
        except Exception as e:
            logging.error(f"❌ خطأ في إرسال الرسالة: {e}")
            return False
    
    def send_to_channel_only(self, text):
        """إرسال للقناة فقط"""
        return self.send_message(text, self.channel_id, False)
    
    def send_to_group_only(self, text):
        """إرسال للجروب فقط"""
        try:
            self.bot.send_message(
                chat_id=self.group_id,
                text=text,
                reply_markup=self.create_keyboard_buttons(),
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            logging.info("✅ تم إرسال الرسالة للجروب بنجاح")
            return True
        except Exception as e:
            logging.error(f"❌ خطأ في إرسال الرسالة للجروب: {e}")
            return False
    
    def send_to_both(self, text):
        """إرسال للقناة والجروب معاً"""
        return self.send_message(text, self.channel_id, True)
