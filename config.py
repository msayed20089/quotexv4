import os
from pytz import timezone

# إعدادات البوت
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', "7920984703:AAHkRNpgzDxBzS61hAe7r7cO_fATlAB8oqM")
CHANNEL_ID = os.getenv('CHANNEL_ID', "@Kingelg0ld")
QX_SIGNUP_URL = "https://broker-qx.pro/sign-up/?lid=1376472"

# بيانات الدخول لـ QX Broker (للتحليل فقط)
QX_EMAIL = os.getenv('QX_EMAIL', 'mohamedels928@gmail.com')
QX_PASSWORD = os.getenv('QX_PASSWORD', 'Mrvip@219')

# الأزواج المطلوبة
TRADING_PAIRS = [
    'USD/BRL', 'USD/EGP', 'USD/TRY', 'USD/ARS', 'USD/COP',
    'USD/DZD', 'USD/IDR', 'USD/BDT', 'USD/NGN',
    'USD/PKR', 'USD/INR', 'USD/MXN', 'USD/PHP'
]
# إضافة إلى config.py
QX_DEMO_URL = "https://qxbroker.com/en/demo-trade"
QX_SIGNIN_URL = "https://qxbroker.com/en/sign-in"
QX_EMAIL = "mohamedels928@gmail.com"
QX_PASSWORD = "Mrvip@219"

# إعدادات التداول
TRADE_DURATION = 30
TRADE_INTERVAL = 2  # كل دقيقتين

# توقيت UTC+3 (توقيت مصر)
UTC3_TZ = timezone('Africa/Cairo')

# إعدادات التحليل الفني
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
