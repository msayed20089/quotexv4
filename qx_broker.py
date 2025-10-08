import time
import logging
import random
from datetime import datetime
from config import UTC3_TZ

class QXBrokerManager:
    def __init__(self):
        self.is_logged_in = True
        self.demo_balance = 10000.0  # رصيد تجريبي
        self.trade_history = []
        logging.info("🎯 نظام QX Broker جاهز (النظام الوهمي)")
    
    def login(self):
        """تسجيل الدخول الوهمي"""
        try:
            logging.info("🔐 جاري تسجيل الدخول إلى QX Broker...")
            time.sleep(2)
            
            # محاكاة عملية تسجيل الدخول
            self.is_logged_in = True
            logging.info("✅ تم تسجيل الدخول إلى QX Broker بنجاح")
            
            return True
            
        except Exception as e:
            logging.error(f"❌ فشل تسجيل الدخول: {e}")
            return False
    
    def execute_trade(self, pair, direction, amount=1):
        """تنفيذ صفقة وهمية على QX Broker"""
        try:
            if not self.is_logged_in:
                logging.warning("⚠️ لم يتم تسجيل الدخول، جاري التسجيل...")
                self.login()
            
            logging.info(f"📊 تنفيذ صفقة على QX Broker: {pair} - {direction}")
            
            # محاكاة وقت التنفيذ
            time.sleep(1)
            
            # تسجيل الصفقة
            trade_data = {
                'pair': pair,
                'direction': direction,
                'amount': amount,
                'timestamp': datetime.now(UTC3_TZ),
                'status': 'EXECUTED'
            }
            
            self.trade_history.append(trade_data)
            logging.info(f"✅ تم تنفيذ صفقة {direction} على {pair} بنجاح")
            
            return True
            
        except Exception as e:
            logging.error(f"❌ فشل تنفيذ الصفقة: {e}")
            return False
    
    def check_trade_result(self, pair):
        """التحقق من نتيجة الصفقة (محاكاة واقعية)"""
        try:
            if not self.trade_history:
                return "UNKNOWN"
            
            # الحصول على آخر صفقة
            latest_trade = self.trade_history[-1]
            
            # محاكاة نتيجة واقعية (60% فرصة ربح)
            if random.random() < 0.6:
                result = "WIN"
                # زيادة الرصيد
                self.demo_balance += 25.0
            else:
                result = "LOSS" 
                # خصم من الرصيد
                self.demo_balance -= 20.0
            
            # تحديث بيانات الصفقة
            latest_trade['result'] = result
            latest_trade['balance_after'] = self.demo_balance
            
            logging.info(f"📊 نتيجة صفقة {pair}: {result} | الرصيد: ${self.demo_balance:.2f}")
            
            return result
            
        except Exception as e:
            logging.error(f"❌ خطأ في التحقق من النتيجة: {e}")
            return "UNKNOWN"
    
    def enter_verification_code(self, code):
        """إدخال كود التحقق الوهمي"""
        try:
            logging.info(f"🔐 جاري التحقق باستخدام الكود: {code}")
            time.sleep(1)
            
            # محاكاة التحقق الناجح
            if len(code) >= 4:
                self.is_logged_in = True
                logging.info("✅ تم التحقق بنجاح!")
                return True
            else:
                logging.warning("❌ كود التحقق غير صحيح")
                return False
                
        except Exception as e:
            logging.error(f"❌ خطأ في التحقق: {e}")
            return False
    
    def get_account_info(self):
        """الحصول على معلومات الحساب"""
        return {
            'balance': self.demo_balance,
            'currency': 'USD',
            'trades_count': len(self.trade_history),
            'status': 'ACTIVE'
        }
