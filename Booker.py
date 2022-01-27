from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep, perf_counter



class Booker:

    def __init__(self):

        options = Options()
        options.add_argument("""--headless""")
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def get_booking(self, bad_id, event_id):

        self.driver.get(f"""https://pretix.eu/Baeder/{bad_id}/{event_id}/""")
        self.driver.find_element(By.XPATH, """//*[@id="item_70748"]""").send_keys(1)
        self.driver.find_element(By.XPATH, """//*[@id="item_70748"]""").send_keys(Keys.RETURN)


        continue_butt = self.wait.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/details/div/div/div[3]/form/p/button""")))
        continue_butt.click()

        continue_butt_2 = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, """/html/body/div[1]/main/form/div[2]/div[2]/button""")))
        continue_butt_2.click()

        cont_guest = self.wait.until(EC.visibility_of_element_located((By.XPATH, """//*[@id="input_customer_guest"]""")))
        cont_guest.click()

        continue_butt_3 = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[2]/div[2]/button""")))
        continue_butt_3.click()

        email_1 = self.wait.until(EC.visibility_of_element_located((By.XPATH, """//*[@id="id_email"]""")))
        email_1.send_keys("lbrouwer@live.nl")

        email_2 = self.wait.until(EC.visibility_of_element_located((By.XPATH, """//*[@id="id_email_repeat"]""")))
        email_2.send_keys("lbrouwer@live.nl")
        email_2.send_keys(Keys.RETURN)

        first_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[1]/details[2]/div/div/div[2]/div[1]/div/div/input[1]""")))
        first_name.send_keys("leonard")

        last_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[1]/details[2]/div/div/div[2]/div[1]/div/div/input[2]""")))
        last_name.send_keys("brouwer")

        phone = self.wait.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[1]/details[2]/div/div/div[2]/div[2]/div/div/input""")))
        phone.send_keys(17622359247)

        address = self.wait.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[1]/details[2]/div/div/div[2]/div[3]/div/input""")))
        address.send_keys("Warschauer Str 60, 10243, Berlin")

        continue_butt_4 = self.wait.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[2]/div[2]/button""")))
        continue_butt_4.click()

        vacc_conf = self.wait.until(EC.visibility_of_element_located((By.XPATH, """//*[@id="input_confirm_confirm_text_0"]""")))
        vacc_conf.click()

        final_booking = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[5]/div[2]/button""")))
        final_booking.click()


if __name__ == '__main__':

    start_time = perf_counter()

    bot = Booker()
    bot.get_booking(47, 2644214)

    end_time = perf_counter()

    print(f"""Total booking lasted {round(end_time - start_time, 2)} seconds""")