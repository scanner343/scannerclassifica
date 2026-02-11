from playwright.sync_api import sync_playwright
import time
import os
import requests

class RePanzaClient:
    def __init__(self, session_id, cookies, user_agent):
        self.session_id = session_id
        self.cookies = cookies
        self.user_agent = user_agent

    @staticmethod
    def send_telegram_alert(message):
        token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if token and chat_id:
            try:
                requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                            data={"chat_id": chat_id, "text": message}, timeout=5)
            except: pass

    @staticmethod
    def auto_login(email, password):
        with sync_playwright() as p:
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1280, 'height': 720}, user_agent=ua)
            page = context.new_page()
            capture = {"sid": None}

            def intercept_response(response):
                if "login" in response.url and response.status == 200:
                    try:
                        cookies = context.cookies()
                        for c in cookies:
                            if c['name'] == 'sessionID': capture["sid"] = c['value']
                    except: pass

            page.on("response", intercept_response)
            
            try:
                print("🌐 Caricamento Lords & Knights...")
                page.goto("https://www.lordsandknights.com/", wait_until="networkidle", timeout=90000)
                page.fill('input[placeholder="Email"]', email)
                page.fill('input[placeholder="Password"]', password)
                page.click('button:has-text("LOG IN")')
                
                # --- 🛠️ MODIFICA QUI IL NOME DEL TASTO ---
                nome_tasto = "Italia VII (IT) (consigliato)" 
                # ----------------------------------------
                
                selector_mondo = page.locator(f".button-game-world--title:has-text('{nome_tasto}')").first
                selector_ok = page.locator("button:has-text('OK')")
                
                print(f"⏳ Attesa accesso {nome_tasto}...")
                for i in range(120):
                    if selector_ok.is_visible():
                        selector_ok.click()
                        time.sleep(1)
                    
                    if selector_mondo.is_visible():
                        print("🎯 Trovato! Entro...")
                        selector_mondo.click(force=True)
                        selector_mondo.evaluate("node => node.click()")
                    
                    if capture["sid"]:
                        print(f"✅ Login Successo!")
                        client = RePanzaClient(capture["sid"], context.cookies(), ua)
                        browser.close()
                        return client
                    time.sleep(1)
                    
                print("❌ Timeout Login! Salvo screenshot...")
                page.screenshot(path="debug_timeout.png")
                
            except Exception as e:
                print(f"⚠️ Errore Login: {e}")
                try: page.screenshot(path="debug_error.png")
                except: pass
            
            browser.close()
            return None
