import numpy as np
import pandas as pd
import logging
import random

class TechnicalAnalyzer:
    def __init__(self):
        self.analysis_methods = [
            "RSI + MACD + Bollinger Bands",
            "Trend Analysis + Support/Resistance", 
            "Price Action + Volume Analysis",
            "Random Market Analysis",
            "Mixed Signals Detection"
        ]
    
    def comprehensive_analysis(self, candle_data):
        """تحليل فني متلخبط بين BUY و SELL"""
        try:
            prices = [candle['close'] for candle in candle_data]
            
            # تحليل عشوائي تماماً مع خلط بين الإشارات
            random_factor = random.random()
            
            # 50/50 فرصة بين BUY و SELL مع خلط
            if random_factor < 0.5:
                direction = "BUY"
                # ثقة عشوائية مع خلط
                confidence = random.randint(60, 85)
                
                # خلط إشارات المؤشرات
                rsi_signal = random.choice(['OVERSOLD', 'NEUTRAL', 'OVERBOUGHT'])
                macd_signal = random.choice(['BULLISH', 'BEARISH', 'MIXED'])
                trend = random.choice(['UPTREND', 'DOWNTREND', 'SIDEWAYS'])
                
            else:
                direction = "SELL"
                # ثقة عشوائية مع خلط
                confidence = random.randint(60, 85)
                
                # خلط إشارات المؤشرات
                rsi_signal = random.choice(['OVERBOUGHT', 'NEUTRAL', 'OVERSOLD'])
                macd_signal = random.choice(['BEARISH', 'BULLISH', 'MIXED'])
                trend = random.choice(['DOWNTREND', 'UPTREND', 'SIDEWAYS'])
            
            # خلط إضافي: 20% فرصة لعكس القرار
            if random.random() < 0.2:
                direction = "BUY" if direction == "SELL" else "SELL"
                confidence = max(55, confidence - 10)
                logging.info("🔄 خلط: تم عكس اتجاه الصفقة")
            
            logging.info(f"📊 تحليل متلخبط: {direction} (ثقة: {confidence}%)")
            
            return {
                'direction': direction,
                'confidence': confidence,
                'analysis_method': random.choice(self.analysis_methods),
                'indicators': {
                    'rsi': round(random.uniform(25, 75), 2),
                    'rsi_signal': rsi_signal,
                    'macd_histogram': round(random.uniform(-0.002, 0.002), 6),
                    'macd_signal': macd_signal,
                    'trend': trend,
                    'bb_position': round(random.uniform(20, 80), 2),
                    'bb_signal': random.choice(['NEUTRAL', 'OVERSOLD', 'OVERBOUGHT'])
                },
                'points_analysis': {
                    'buy_points': random.randint(2, 8),
                    'sell_points': random.randint(2, 8)
                }
            }
            
        except Exception as e:
            logging.error(f"❌ خطأ في التحليل الفني: {e}")
            return self.get_mixed_analysis()
    
    def get_mixed_analysis(self):
        """تحليل مختلط عشوائي"""
        # توزيع 50/50 مع خلط
        direction = random.choice(['BUY', 'SELL'])
        confidence = random.randint(55, 80)
        
        # خلط إشارات المؤشرات
        rsi_signal = random.choice(['OVERSOLD', 'NEUTRAL', 'OVERBOUGHT'])
        macd_signal = random.choice(['BULLISH', 'BEARISH', 'MIXED'])
        
        logging.info(f"🔄 تحليل مختلط: {direction} (ثقة: {confidence}%)")
        
        return {
            'direction': direction,
            'confidence': confidence,
            'analysis_method': "MIXED_RANDOM_ANALYSIS",
            'indicators': {
                'rsi': round(random.uniform(30, 70), 2),
                'rsi_signal': rsi_signal,
                'macd_histogram': round(random.uniform(-0.001, 0.001), 6),
                'macd_signal': macd_signal,
                'trend': random.choice(['UPTREND', 'DOWNTREND', 'SIDEWAYS']),
                'bb_position': round(random.uniform(25, 75), 2),
                'bb_signal': random.choice(['NEUTRAL', 'OVERSOLD', 'OVERBOUGHT'])
            }
        }
