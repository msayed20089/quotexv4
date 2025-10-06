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
        current_time = self.format_time(self.get_utc3_time())
        
        welcome_message = f"""
🎯 <b>بدء تشغيل النظام بالتوقيت المحدد</b>

⏰ <b>نظام التوقيت:</b>
• 6:00:00 → نشر إشارة الصفقة
• 6:01:00 → دخول الصفقة
• 6:01:35 → نشر النتيجة
• 6:02:00 → الإشارة التالية

🕒 <b>الوقت الحالي:</b> {current_time} (UTC+3)
⚡ <b>جاري التحضير للإشارة الأولى...</b>
"""
        self.telegram_bot.send_message(welcome_message)
        
        self.next_signal_time = self.calculate_next_signal_time()
        logging.info(f"⏰ أول إشارة: {self.format_time(self.next_signal_time)}")
    
    def execute_signal_cycle(self):
        """دورة الإشارة"""
        try:
            trade_data = self.trading_engine.analyze_and_decide()
            self.stats['skipped_trades'] += 1
            
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
        signal_time = self.format_time(self.pending_trade['signal_time'])
        trade_time = self.format_time(self.pending_trade['trade_time'])
        result_time = self.format_time(self.pending_trade['result_time'])
        
        message = f"""
📊 <b>إشارة تداول متقدمة</b>

💰 <b>الزوج:</b> {trade_data['pair']}
🎯 <b>الاتجاه:</b> {trade_data['direction']}
⏱ <b>المدة:</b> 30 ثانية

📈 <b>التحليل:</b>
• الثقة: {trade_data['confidence']}%
• RSI: {trade_data['indicators']['rsi']}

🕒 <b>مواعيد الصفقة:</b>
• وقت الإشارة: {signal_time}
• وقت الدخول: {trade_time} 🎯
• وقت النتيجة: {result_time}

⚡ <b>جاري التحضير...</b>
"""
        self.telegram_bot.send_message(message)
    
    def send_skip_message(self, trade_data):
        """رسالة تخطي"""
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
    
    def execute_trade_cycle(self):
        """تنفيذ الصفقة"""
        if not self.pending_trade:
            return
            
        try:
            trade_data = self.pending_trade['data']
            
            # تنفيذ الصفقة
            self.qx_manager.execute_trade(trade_data['pair'], trade_data['direction'])
            
            # انتظار 30 ثانية
            time.sleep(30)
            
            # توليد الشمعة وتحديد النتيجة
            candle_data = self.candle_analyzer.generate_candle_data(trade_data['pair'])
            result = self.candle_analyzer.determine_trade_result(candle_data, trade_data['direction'])
            
            # تحديث الإحصائيات
            self.update_stats(result, trade_data)
            
            # إرسال النتيجة
            self.send_trade_result(result, trade_data, candle_data)
            
            logging.info(f"🎯 اكتملت الصفقة: {result}")
            
        except Exception as e:
            logging.error(f"❌ خطأ في التنفيذ: {e}")
        finally:
            self.pending_trade = None
    
    def send_trade_result(self, result, trade_data, candle_data):
        """إرسال النتيجة"""
        result_emoji = "🎉" if result == 'WIN' else "❌"
        result_text = "WIN 🎉" if result == 'WIN' else "LOSS ❌"
        current_time = self.format_time(self.get_utc3_time())
        
        message = f"""
🎯 <b>نتيجة الصفقة</b> {result_emoji}

💰 <b>الزوج:</b> {trade_data['pair']}
📊 <b>النتيجة:</b> {result_text}
📈 <b>الاتجاه:</b> {trade_data['direction']}

💹 <b>حركة السعر:</b>
• الافتتاح: {candle_data['open']}
• الإغلاق: {candle_data['close']}
• التغير: {candle_data['price_change_percent']}%

🕒 <b>الوقت:</b> {current_time}

📊 <b>إحصائيات:</b>
• الرابحة: {self.stats['win_trades']}
• الخاسرة: {self.stats['loss_trades']}
"""
        self.telegram_bot.send_message(message)
    
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
                    self.pending_trade = self.execute_signal_cycle()
                    
                    if self.pending_trade:
                        # جدولة التنفيذ بعد دقيقة
                        trade_time = self.pending_trade['trade_time']
                        logging.info(f"⏰ تم جدولة التنفيذ: {self.format_time(trade_time)}")
                    
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
