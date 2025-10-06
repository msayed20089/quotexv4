import random
import logging
from datetime import datetime
from config import UTC3_TZ, TRADING_PAIRS

class TradingEngine:
    def __init__(self):
        self.pairs = TRADING_PAIRS
        from candle_analyzer import CandleAnalyzer
        from technical_analyzer import TechnicalAnalyzer
        
        self.candle_analyzer = CandleAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
        self.recent_directions = []
    
    def analyze_and_decide(self):
        """اتخاذ قرار تداول متوازن"""
        try:
            pair = random.choice(self.pairs)
            
            # تحليل فني
            historical_candles = self.candle_analyzer.get_historical_candles(pair, 15)
            analysis_result = self.technical_analyzer.comprehensive_analysis(historical_candles)
            
            # تطبيق التوازن
            balanced_direction = self.apply_balance(analysis_result['direction'])
            
            trade_data = {
                'pair': pair,
                'direction': balanced_direction,
                'trade_time': datetime.now(UTC3_TZ).strftime("%H:%M:00"),
                'duration': 30,
                'confidence': analysis_result['confidence'],
                'analysis_method': analysis_result['analysis_method'],
                'indicators': analysis_result['indicators']
            }
            
            logging.info(f"🎯 قرار {pair}: {balanced_direction} (ثقة: {analysis_result['confidence']}%)")
            return trade_data
            
        except Exception as e:
            logging.error(f"❌ خطأ في التحليل: {e}")
            return self.get_fallback_analysis()
    
    def apply_balance(self, direction):
        """تطبيق توازن على الاتجاهات"""
        self.recent_directions.append(direction)
        if len(self.recent_directions) > 5:
            self.recent_directions.pop(0)
        
        # منع التكرار
        if len(self.recent_directions) >= 3:
            last_three = self.recent_directions[-3:]
            if all(d == 'BUY' for d in last_three):
                return 'SELL'
            elif all(d == 'SELL' for d in last_three):
                return 'BUY'
        
        return direction
    
    def get_fallback_analysis(self):
        """تحليل احتياطي"""
        pair = random.choice(self.pairs)
        direction = random.choice(['BUY', 'SELL'])
        
        return {
            'pair': pair,
            'direction': direction,
            'trade_time': datetime.now(UTC3_TZ).strftime("%H:%M:00"),
            'duration': 30,
            'confidence': 70,
            'analysis_method': "FALLBACK_ANALYSIS",
            'indicators': {}
        }
