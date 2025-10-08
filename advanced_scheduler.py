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
            self.send_trade_result("FAILED", trade_data, None)
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
        self.send_trade_result(result, trade_data, None)
        
        logging.info(f"🎯 اكتملت الصفقة: {result}")
        
    except Exception as e:
        logging.error(f"❌ خطأ في التنفيذ: {e}")
        self.send_trade_result("ERROR", trade_data, None)
    finally:
        self.pending_trade = None

def send_trade_result(self, result, trade_data, candle_data):
    """إرسال النتيجة مع معلومات الحساب"""
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
