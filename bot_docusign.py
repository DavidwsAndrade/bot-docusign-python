import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui


class BotDocuSign:
    def __init__(self, user_email, user_passw, logger, driver):
        self.user_email = user_email
        self.user_passw = user_passw
        self.logger = logger
        self.driver = driver

    def login_to_docusign(self):
        self.driver.get('https://account.docusign.com/')
        time.sleep(1)
        
        email_input = self.driver.find_element(By.NAME, 'email')
        email_input.send_keys(self.user_email)
        
        login_button = self.driver.find_element(By.CLASS_NAME, 'olv-button')
        login_button.click()
        
        time.sleep(1)
        
        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.send_keys(self.user_passw)
        
        password_button = self.driver.find_element(By.CLASS_NAME, 'olv-button')
        password_button.click()
        # Após digitar o token enviado para o email no input, volte ao terminal e pressione ENTER
        input("Pressione enter no terminal após informar o código solicitado pelo docusign para login...") 
        
        login_button = self.driver.find_element(By.CLASS_NAME, 'olv-button')
        login_button.click()
        
        time.sleep(10)

    def navigate_to_cards(self):
        cards_bt = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "css-mr2eww"))
        )
        cards_bt[3].click()
        time.sleep(1)

    def apply_filters(self):
        for _ in range(3):
            pyautogui.hotkey('ctrl', '-')   #zoom para 75% por causa do botão aplicar.
        
        filter_bt = self.driver.find_element(By.CLASS_NAME, 'css-t92vf8')
        filter_bt.click()
        
        filter_all = self.driver.find_element(By.XPATH, "//span[text()='Todo o tempo']")
        filter_all.click()
        
        apply_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Aplicar']]"))
        )
        apply_button.click()
        time.sleep(4)

    def download_files(self,go_page="", attempts=0):
        image_path = 'path_da_imagem.png'
        first_time = False
        current_page = self.driver.find_element(By.XPATH, "//div//strong[contains(text(), 'Page')]")
        next_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Go to next page']]"))
        )
        
        if go_page == "":
            go_page = "Page 1" #setar pagina manual conforme necessidade.
            first_time = True

        while current_page.text != go_page:
            next_button.click()
            time.sleep(3.5)
            current_page = self.driver.find_element(By.XPATH, "//div//strong[contains(text(), 'Page')]")

        while True:
            try:
                time.sleep(1)
                download_buttons = self.driver.find_elements(By.XPATH, "//button[.//span[text()='Baixar']]")
                
                if not download_buttons:
                    raise Exception("Não encontrei os botões para baixar o arquivo.")
                    
                for element in download_buttons:
                    time.sleep(2)
                    self.driver.execute_script('arguments[0].click();', element)
                    if first_time:
                        time.sleep(2)
                        localizacao = pyautogui.locateOnScreen(image_path)
                        first_time = False 
                    time.sleep(4)
                    pyautogui.click(localizacao)
                
                next_button = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Go to next page']]"))
                )

                if not next_button:
                    break
                
                next_button.click()
                time.sleep(2)
            except Exception as e:
                current_page = self.driver.find_element(By.XPATH, "//div//strong[contains(text(), 'Page')]")
                self.logger.error(str(e) + '-->parei na paginacao: ' + current_page.text)
                break

        current_page = self.driver.find_element(By.XPATH, "//div//strong[contains(text(), 'Page')]")
        if not next_button:
            self.logger.debug('Concluido download. Ate a pagina ' + current_page.text)
        else:
            attempts = attempts+1
            if attempts <= 3:
                self.download_files(go_page=current_page.text,attempts=attempts) #tentar mais 3x
    
    def run(self):
        try:
            self.login_to_docusign()
            self.navigate_to_cards()
            self.apply_filters()
            self.download_files()
        finally:
            self.driver.quit()