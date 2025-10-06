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
        """اتخاذ قرار تداول مع خلط بين BUY و SELL"""
        try:
            pair = random.choice(self.pairs)
            
            # تحليل فني مختلط
            historical_candles = self.candle_analyzer.get_historical_candles(pair, 15)
            analysis_result = self.technical_analyzer.comprehensive_analysis(historical_candles)
            
            # تطبيق خلط إضافي على الاتجاه
            mixed_direction = self.apply_mixing(analysis_result['direction'])
            
            trade_data = {
                'pair': pair,
                'direction': mixed_direction,
                'trade_time': datetime.now(UTC3_TZ).strftime("%H:%M:00"),
                'duration': 30,
                'confidence': analysis_result['confidence'],
                'analysis_method': analysis_result['analysis_method'],
                'indicators': analysis_result['indicators'],
                'news_impact': {'direction': 'NEUTRAL', 'score': 0, 'events_count': 0},
                'market_sentiment': {'overall_direction': 'NEUTRAL', 'confidence': 50},
                'points_breakdown': analysis_result.get('points_analysis', {'buy_points': 0, 'sell_points': 0})
            }
            
            logging.info(f"🎯 قرار مختلط لـ {pair}: {mixed_direction} (ثقة: {trade_data['confidence']}%)")
            return trade_data
            
        except Exception as e:
            logging.error(f"❌ خطأ في التحليل واتخاذ القرار: {e}")
            return self.get_mixed_fallback_analysis()
    
    def apply_mixing(self, direction):
        """تطبيق خلط على الاتجاهات"""
        # حفظ آخر 4 اتجاهات
        self.recent_directions.append(direction)
        if len(self.recent_directions) > 4:
            self.recent_directions.pop(0)
        
        # خلط: 30% فرصة لعكس الاتجاه
        if random.random() < 0.3:
            mixed_direction = "BUY" if direction == "SELL" else "SELL"
            logging.info(f"🔄 خلط: تحويل من {direction} إلى {mixed_direction}")
            return mixed_direction
        
        # خلط: إذا كان هناك تكرار، غير الاتجاه
        if len(self.recent_directions) >= 2:
            last_two = self.recent_directions[-2:]
            if all(d == 'BUY' for d in last_two):
                logging.info("🔄 خلط: تغيير من BUY إلى SELL بسبب التكرار")
                return 'SELL'
            elif all(d == 'SELL' for d in last_two):
                logging.info("🔄 خلط: تغيير من SELL إلى BUY بسبب التكرار")
                return 'BUY'
        
        return direction
    
    def get_mixed_fallback_analysis(self):
        """تحليل احتياطي مختلط"""
        pair = random.choice(self.pairs)
        # 50/50 فرصة مع خلط
        direction = random.choice(['BUY', 'SELL'])
        confidence = random.randint(60, 80)
        
        return {
            'pair': pair,
            'direction': direction,
            'trade_time': datetime.now(UTC3_TZ).strftime("%H:%M:00"),
            'duration': 30,
            'confidence': confidence,
            'analysis_method': 'MIXED_FALLBACK_ANALYSIS',
            'indicators': {},
            'news_impact': {'direction': 'NEUTRAL', 'score': 0},
            'market_sentiment': {'overall_direction': 'NEUTRAL', 'confidence': 50},
            'points_breakdown': {'buy_points': 0, 'sell_points': 0}
        }
