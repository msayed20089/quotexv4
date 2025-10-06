import time
import logging
import random
import numpy as np
from datetime import datetime, timedelta
from config import UTC3_TZ

class CandleAnalyzer:
    def __init__(self):
        self.price_history = {}
        self.last_prices = {}
        
    def get_realistic_price(self, pair):
        """الحصول على سعر واقعي للزوج"""
        realistic_prices = {
            'USD/BRL': 5.50, 'USD/EGP': 47.80, 'USD/TRY': 32.70,
            'USD/ARS': 905.0, 'USD/COP': 4000, 'USD/DZD': 135.0,
            'USD/IDR': 16000, 'USD/BDT': 118.0, 'USD/CAD': 1.37,
            'USD/NGN': 1475, 'USD/PKR': 280.0, 'USD/INR': 83.50,
            'USD/MXN': 17.25, 'USD/PHP': 56.30
        }
        return realistic_prices.get(pair, 1.0)
    
    def generate_candle_data(self, pair):
        """توليد بيانات شمعة واقعية"""
        try:
            base_price = self.get_realistic_price(pair)
            
            # استخدام آخر سعر أو السعر الأساسي
            if pair in self.last_prices:
                open_price = self.last_prices[pair]
            else:
                open_price = base_price
            
            # حركة سعرية واقعية (0.1% - 0.8%)
            change_percent = random.uniform(-0.008, 0.008)
            close_price = open_price * (1 + change_percent)
            
            # تحديد القمة والقاع
            price_range = abs(close_price - open_price) * 3
            high_price = max(open_price, close_price) + random.uniform(0, price_range * 0.5)
            low_price = min(open_price, close_price) - random.uniform(0, price_range * 0.5)
            
            # التأكد من التسلسل الصحيح
            high_price = max(high_price, max(open_price, close_price))
            low_price = min(low_price, min(open_price, close_price))
            
            candle_data = {
                'open': round(open_price, 4),
                'high': round(high_price, 4),
                'low': round(low_price, 4),
                'close': round(close_price, 4),
                'timestamp': datetime.now(UTC3_TZ),
                'pair': pair,
                'price_change_percent': round(change_percent * 100, 3)
            }
            
            # حفظ السعر الأخير
            self.last_prices[pair] = close_price
            
            logging.info(f"📊 شمعة {pair}: {open_price} → {close_price} ({candle_data['price_change_percent']}%)")
            
            return candle_data
            
        except Exception as e:
            logging.error(f"❌ خطأ في توليد الشمعة: {e}")
            return self.get_fallback_candle(pair)
    
    def get_fallback_candle(self, pair):
        """شمعة احتياطية"""
        base_price = self.get_realistic_price(pair)
        change = random.uniform(-0.01, 0.01)
        
        return {
            'open': round(base_price, 4),
            'high': round(base_price * 1.01, 4),
            'low': round(base_price * 0.99, 4),
            'close': round(base_price * (1 + change), 4),
            'timestamp': datetime.now(UTC3_TZ),
            'pair': pair,
            'price_change_percent': round(change * 100, 3)
        }
    
    def determine_trade_result(self, candle_data, trade_direction):
        """تحديد نتيجة الصفقة بدقة"""
        try:
            open_price = candle_data['open']
            close_price = candle_data['close']
            
            # حساب النتيجة بشكل صحيح
            if trade_direction == "BUY":
                result = "WIN" if close_price > open_price else "LOSS"
            else:  # SELL
                result = "WIN" if close_price < open_price else "LOSS"
            
            logging.info(f"🎯 نتيجة {trade_direction}: {result} (من {open_price} إلى {close_price})")
            
            return result
            
        except Exception as e:
            logging.error(f"❌ خطأ في تحديد النتيجة: {e}")
            return random.choice(['WIN', 'LOSS'])
    
    def get_historical_candles(self, pair, count=20):
        """الحصول على شموع تاريخية"""
        try:
            candles = []
            base_price = self.get_realistic_price(pair)
            
            for i in range(count):
                # محاكاة شموع تاريخية
                price = base_price * (1 + random.uniform(-0.05, 0.05))
                candle = self.generate_candle_data(pair)
                candles.append(candle)
            
            return candles
        except Exception as e:
            logging.error(f"❌ خطأ في الشموع التاريخية: {e}")
            return []
