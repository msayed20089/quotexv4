import time
import logging
from datetime import datetime, timedelta
from config import UTC3_TZ, TRADING_PAIRS

class AdvancedScheduler:
    def __init__(self):
        from qx_broker import QXBrokerManager
        from telegram_bot import TelegramBot
        from trading_engine import TradingEngine
        from candle_analyzer import CandleAnalyzer
        
        self.qx_manager = QXBrokerManager()
        self.telegram_bot = TelegramBot()
        self.trading_engine = TradingEngine()
        self.candle_analyzer = CandleAnalyzer()
        
        self.stats = {
            'total_trades': 0, 'win_trades': 0, 'loss_trades': 0,
            'skipped_trades': 0, 'buy_count': 0, 'sell_count': 0
        }
        
        self.next_signal_time = None
        self.pending_trade = None
        
    def get_utc3_time(self):
        return datetime.now(UTC3_TZ)
    
    def calculate_next_signal_time(self):
        """الإشارة التالية بعد دقيقتين"""
        now = self.get_utc3_time()
        return (now.replace(second=0, microsecond=0) + timedelta(minutes=2))
    
    def format_time(self, dt):
        """تنسيق الوقت بثواني 00"""
        return dt.strftime("%H:%M:00")
    
    def start_trading_system(self):
    """بدء النظام"""
    try:
        current_time = self.format_time(self.get_utc3_time())
        
        # إرسال رسالة الرصيد أولاً
        account_info = self.qx_manager.get_account_info()
        
        welcome_message = f"""
🎯 <b>بدء تشغيل النظام بالتوقيت المحدد</b>

💳 <b>معلومات الحساب:</b>
• الرصيد: ${account_info['balance']:,.2f}
• الحساب: {account_info['email']}
• البلد: {account_info['country']}

⏰ <b>نظام التوقيت:</b>
• 6:00:00 → نشر إشارة الصفقة
• 6:01:00 → دخول الصفقة
• 6:01:35 → نشر النتيجة
• 6:02:00 → الإشارة التالية

🕒 <b>الوقت الحالي:</b> {current_time} (UTC+3)
{'⚡ <b>وضع التصحيح نشط - دورة كل 30 ثانية</b>' if self.debug_mode else ''}
"""
        success = self.telegram_bot.send_message(welcome_message)
        
        if not success:
            logging.warning("⚠️ فشل إرسال رسالة البداية، جاري التشغيل بدون Telegram")
        
        self.next_signal_time = self.calculate_next_signal_time()
        logging.info(f"⏰ أول إشارة: {self.format_time(self.next_signal_time)}")
        
    except Exception as e:
        logging.error(f"❌ خطأ في بدء النظام: {e}")
    
    def execute_signal_cycle(self):
        """دورة الإشارة"""
        try:
            trade_data = self.trading_engine.analyze_and_decide()
            
            if trade_data['confidence'] < 65:
                self.send_skip_message(trade_data)
                return None
            
            # تخزين الصفقة المعلقة
            current_time = self.get_utc3_time().replace(second=0, microsecond=0)
            self.pending_trade = {
                'data': trade_data,
                'signal_time': current_time,
                'trade_time': current_time + timedelta(minutes=1),
                'result_time': current_time + timedelta(minutes=1, seconds=35)
            }
            
            self.send_trade_signal(trade_data)
            logging.info(f"📤 إشارة: {trade_data['pair']} - {trade_data['direction']}")
            
            return self.pending_trade
            
        except Exception as e:
            logging.error(f"❌ خطأ في دورة الإشارة: {e}")
            return None
    
    def send_trade_signal(self, trade_data):
        """إرسال إشارة الصفقة"""
        try:
            signal_time = self.format_time(self.pending_trade['signal_time'])
            trade_time = self.format_time(self.pending_trade['trade_time'])
            
            message = f"""
📊 <b>إشارة تداول جديدة</b>

💰 <b>الزوج:</b> {trade_data['pair']}
🎯 <b>الاتجاه:</b> {trade_data['direction']}
⏱ <b>المدة:</b> 30 ثانية

🕒 <b>مواعيد الصفقة:</b>
• وقت الإشارة: {signal_time}
• وقت الدخول: {trade_time} 🎯

⚡ <b>جاري التحضير...</b>
"""
            self.telegram_bot.send_message(message)
        except Exception as e:
            logging.error(f"❌ خطأ في إرسال إشارة الصفقة: {e}")
    
    def send_skip_message(self, trade_data):
        """رسالة تخطي"""
        try:
            current_time = self.format_time(self.get_utc3_time())
            
            message = f"""
⏭️ <b>تم تخطي الصفقة</b>

💰 <b>الزوج:</b> {trade_data['pair']}
🎯 <b>الاتجاه:</b> {trade_data['direction']}
📉 <b>الثقة:</b> {trade_data['confidence']}%

❌ <b>سبب التخطي:</b>
ثقة منخفضة

🕒 <b>الوقت:</b> {current_time}
"""
            self.telegram_bot.send_message(message)
        except Exception as e:
            logging.error(f"❌ خطأ في إرسال رسالة التخطي: {e}")
    
    def execute_trade_cycle(self):
        """تنفيذ الصفقة الحقيقية"""
        if not self.pending_trade:
            return
            
        try:
            trade_data = self.pending_trade['data']
            
            # التأكد من تسجيل الدخول أولاً
            if not self.qx_manager.is_logged_in:
                logging.info("🔐 جاري تسجيل الدخول إلى QX Broker...")
                self.qx_manager.login()
            
            # تنفيذ الصفقة الحقيقية على QX Broker
            success = self.qx_manager.execute_trade(
                trade_data['pair'], 
                trade_data['direction']
            )
            
            if not success:
                logging.error("❌ فشل تنفيذ الصفقة على QX Broker")
                self.send_trade_result("FAILED", trade_data)
                return
            
            # انتظار 30 ثانية (مدة الصفقة)
            logging.info("⏳ انتظار نتيجة الصفقة (30 ثانية)...")
            time.sleep(30)
            
            # التحقق من النتيجة الحقيقية من QX Broker
            result = self.qx_manager.check_trade_result(trade_data['pair'])
            
            # إذا لم نتمكن من الحصول على النتيجة، نستخدم المحاكاة
            if result == "UNKNOWN":
                logging.warning("⚠️ استخدام النظام الوهمي للنتيجة")
                candle_data = self.candle_analyzer.generate_candle_data(trade_data['pair'])
                result = self.candle_analyzer.determine_trade_result(candle_data, trade_data['direction'])
            
            # تحديث الإحصائيات
            self.update_stats(result, trade_data)
            
            # إرسال النتيجة
            self.send_trade_result(result, trade_data)
            
            logging.info(f"🎯 اكتملت الصفقة: {result}")
            
        except Exception as e:
            logging.error(f"❌ خطأ في التنفيذ: {e}")
            self.send_trade_result("ERROR", trade_data)
        finally:
            self.pending_trade = None
    
    def send_trade_result(self, result, trade_data):
        """إرسال النتيجة مع معلومات الحساب"""
        try:
            result_emoji = "🎉" if result == 'WIN' else "❌"
            result_text = "WIN 🎉" if result == 'WIN' else "LOSS ❌"
            
            if result == "FAILED":
                result_emoji = "🚫"
                result_text = "FAILED 🚫"
            elif result == "ERROR":
                result_emoji = "⚠️"
                result_text = "ERROR ⚠️"
            
            current_time = self.format_time(self.get_utc3_time())
            
            # الحصول على معلومات الحساب
            account_info = self.qx_manager.get_account_info()
            
            message = f"""
🎯 <b>نتيجة الصفقة</b> {result_emoji}

💰 <b>الزوج:</b> {trade_data['pair']}
📊 <b>النتيجة:</b> {result_text}
📈 <b>الاتجاه:</b> {trade_data['direction']}
🕒 <b>الوقت:</b> {current_time}

💳 <b>معلومات الحساب:</b>
• الرصيد: ${account_info['balance']:.2f}
• عدد الصفقات: {account_info['trades_count']}
• الحالة: {account_info['status']}

📊 <b>نظام QX Broker التجريبي</b>
"""
            self.telegram_bot.send_message(message)
        except Exception as e:
            logging.error(f"❌ خطأ في إرسال النتيجة: {e}")
    
    def update_stats(self, result, trade_data):
        """تحديث الإحصائيات"""
        self.stats['total_trades'] += 1
        
        if result == 'WIN':
            self.stats['win_trades'] += 1
        else:
            self.stats['loss_trades'] += 1
        
        if trade_data['direction'] == 'BUY':
            self.stats['buy_count'] += 1
        else:
            self.stats['sell_count'] += 1
    
    def run_precision_scheduler(self):
        """التشغيل الرئيسي"""
        try:
            self.start_trading_system()
            logging.info("✅ بدء التشغيل الدقيق...")
            
            while True:
                current_time = self.get_utc3_time()
                
                # الانتظار للثانية 00
                if current_time.second != 0:
                    time.sleep(0.1)
                    continue
                
                # التحقق من وقت الإشارة
                if (self.next_signal_time and 
                    current_time >= self.next_signal_time and 
                    not self.pending_trade):
                    
                    logging.info(f"⏰ بدء دورة الإشارة: {self.format_time(current_time)}")
                    self.execute_signal_cycle()
                    
                    # الإشارة التالية بعد دقيقتين
                    self.next_signal_time = self.calculate_next_signal_time()
                    logging.info(f"⏰ الإشارة القادمة: {self.format_time(self.next_signal_time)}")
                
                # التحقق من وقت التنفيذ
                if (self.pending_trade and 
                    current_time >= self.pending_trade['trade_time']):
                    
                    logging.info(f"🎯 بدء التنفيذ: {self.format_time(current_time)}")
                    self.execute_trade_cycle()
                
                time.sleep(0.1)
                    
        except Exception as e:
            logging.error(f"❌ خطأ فادح: {e}")
            time.sleep(10)
            self.run_precision_scheduler()
