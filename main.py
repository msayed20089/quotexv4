from advanced_scheduler import AdvancedScheduler
import logging
import sys

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def main():
    """الدالة الرئيسية"""
    try:
        logging.info("🚀 بدء تشغيل البوت الدقيق...")
        
        # تشغيل الجدولة
        scheduler = AdvancedScheduler()
        scheduler.run_precision_scheduler()
        
    except Exception as e:
        logging.error(f"❌ خطأ في التشغيل: {e}")
        logging.info("🔄 إعادة التشغيل بعد 30 ثانية...")
        import time
        time.sleep(30)
        main()

if __name__ == "__main__":
    main()
