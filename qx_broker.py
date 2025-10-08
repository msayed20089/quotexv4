import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from config import QX_SIGNIN_URL, QX_DEMO_URL, QX_EMAIL, QX_PASSWORD

class QXBrokerManager:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        self.setup_driver()
        self.login()
    
    def setup_driver(self):
        """إعداد متصفح Chrome"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # للتشغيل في الخلفية
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        logging.info("🌐 تم إعداد متصفح QX Broker")
    
    def login(self):
        """تسجيل الدخول إلى QX Broker"""
        try:
            self.driver.get(QX_SIGNIN_URL)
            
            # إدخال البريد الإلكتروني
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_field.send_keys(QX_EMAIL)
            
            # إدخال كلمة المرور
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(QX_PASSWORD)
            
            # النقر على تسجيل الدخول
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # الانتظار والتحقق من نجاح التسجيل
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
            )
            
            self.is_logged_in = True
            logging.info("✅ تم تسجيل الدخول إلى QX Broker بنجاح")
            
        except Exception as e:
            logging.error(f"❌ فشل تسجيل الدخول: {e}")
            self.handle_login_verification()
    
    def handle_login_verification(self):
        """معالجة طلب كود التحقق"""
        try:
            # التحقق إذا كان هناك طلب لكود تحقق
            code_field = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "verification_code"))
            )
            
            logging.warning("🔐 النظام يطلب كود تحقق - إرسال /code في البوت")
            
            # هنا سننتظر إدخال الكود من خلال البوت
            # سيتم معالجته في دالة منفصلة
            
        except:
            logging.error("❌ فشل في معالجة تسجيل الدخول")
    
    def enter_verification_code(self, code):
        """إدخال كود التحقق"""
        try:
            code_field = self.driver.find_element(By.NAME, "verification_code")
            code_field.send_keys(code)
            
            verify_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Verify')]")
            verify_button.click()
            
            # الانتظار للتحقق من النجاح
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
            )
            
            self.is_logged_in = True
            logging.info("✅ تم إدخال كود التحقق بنجاح")
            return True
            
        except Exception as e:
            logging.error(f"❌ فشل إدخال كود التحقق: {e}")
            return False
    
    def execute_trade(self, pair, direction, amount=1):
        """تنفيذ صفقة حقيقية على QX Broker"""
        try:
            if not self.is_logged_in:
                logging.error("❌ غير مسجل الدخول - لا يمكن تنفيذ الصفقة")
                return False
            
            # الانتقال لصفحة التداول
            self.driver.get(QX_DEMO_URL)
            
            # البحث عن الزوج
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search trading pair']"))
            )
            search_box.clear()
            search_box.send_keys(pair)
            
            time.sleep(2)
            
            # اختيار الزوج من النتائج
            pair_element = self.driver.find_element(By.XPATH, f"//div[contains(text(), '{pair}')]")
            pair_element.click()
            
            # إعداد الصفقة
            if direction == "BUY":
                buy_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'buy')]"))
                )
                buy_button.click()
            else:  # SELL
                sell_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'sell')]"))
                )
                sell_button.click()
            
            # تأكيد الصفقة
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
            )
            confirm_button.click()
            
            logging.info(f"✅ تم تنفيذ صفقة {direction} على {pair}")
            return True
            
        except Exception as e:
            logging.error(f"❌ فشل تنفيذ الصفقة: {e}")
            return False
    
    def check_trade_result(self, pair):
        """التحقق من نتيجة الصفقة الأخيرة"""
        try:
            # الانتقال لصفحة التاريخ
            self.driver.get("https://qxbroker.com/en/trade-history")
            
            # الحصول على آخر صفقة
            latest_trade = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//tr[1]"))
            )
            
            result_element = latest_trade.find_element(By.XPATH, ".//td[contains(@class, 'result')]")
            result_text = result_element.text
            
            if "profit" in result_text.lower() or "win" in result_text.lower():
                return "WIN"
            elif "loss" in result_text.lower():
                return "LOSS"
            else:
                return "UNKNOWN"
                
        except Exception as e:
            logging.error(f"❌ فشل التحقق من النتيجة: {e}")
            return "UNKNOWN"
    
    def close(self):
        """إغلاق المتصفح"""
        if self.driver:
            self.driver.quit()
