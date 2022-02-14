import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from time import perf_counter, sleep
from datetime import datetime, timedelta
import pandas as pd


class Booker:

    def __init__(self):

        options = Options()
        # options.add_argument("""--headless""")
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.wait2 = WebDriverWait(self.driver, 1)

    def get_booking(self, bad_id, event_id):

        self.driver.get(f"""https://pretix.eu/Baeder/{bad_id}/{event_id}/""")

        button_id = "71664"

        try:
            self.driver.find_element(By.XPATH, f"""//*[@id="item_{button_id}"]""").send_keys(1)
            self.driver.find_element(By.XPATH, f"""//*[@id="item_{button_id}"]""").send_keys(Keys.RETURN)
        except TimeoutException:
            cart = self.driver.find_element(By.XPATH, f"""//*[@id="item_{button_id}"]""")
            cart.click()

        continue_butt = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                          """/html/body/div[1]/main/details/div/div/div[3]/form/p/button""")))
        continue_butt.click()

        continue_butt_2 = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, """/html/body/div[1]/main/form/div[2]/div[2]/button""")))
        continue_butt_2.click()

        cont_guest = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                       """//*[@id="input_customer_guest"]""")))
        cont_guest.click()

        continue_butt_3 = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[2]/div[2]/button""")))
        continue_butt_3.click()

        """/html/body/div[1]/main/form/div[5]/div[2]/button"""

        email_1 = self.wait.until(EC.visibility_of_element_located((By.XPATH, """//*[@id="id_email"]""")))
        email_1.send_keys("lbrouwer@live.nl")

        email_2 = self.wait.until(EC.visibility_of_element_located((By.XPATH, """//*[@id="id_email_repeat"]""")))
        email_2.send_keys("lbrouwer@live.nl")
        email_2.send_keys(Keys.RETURN)

        sleep(15)

        # first_name = self.wait.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[1]/details[2]/div/div/div[2]/div[1]/div/div/input[1]""")))

        try:
            first_name = self.wait2.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[1]/details[2]/div/div/div[2]/div/div/div/input[1]""")))
            first_name.send_keys("leonard")
        except TimeoutException:
            print("no first name to give")

        # last_name = self.wait.until(EC.visibility_of_element_located(
        #     (By.XPATH, """/html/body/div[1]/main/form/div[1]/details[2]/div/div/div[2]/div[1]/div/div/input[2]""")))

        try:
            last_name = self.wait2.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[1]/details[2]/div/div/div[2]/div/div/div/input[2]""")))
            last_name.send_keys("brouwer")
        except TimeoutException:
            print("no last name to give")

        try:
            phone = self.wait2.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[1]/details[2]/div/div/div[2]/div[2]/div/div/input""")))
            phone.send_keys(17622359247)

            address = self.wait2.until(EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[1]/details[2]/div/div/div[2]/div[3]/div/input""")))
            address.send_keys("Warschauer Str 60, 10243, Berlin")

        except TimeoutException:
            print("No more phone or no address to give")

        try:
            continue_butt_4 = self.wait2.until(
                EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[2]/div[2]/button""")))
            continue_butt_4.click()
        except:
            print("No need to press next")

        try:
            vacc_conf = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[4]/div[2]/div/label""")))
            vacc_conf.click()

        except TimeoutException:
            vacc_conf = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, """//*[@id="input_confirm_confirm_text_0"]""")))
            vacc_conf.click()

        final_booking = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, """/html/body/div[1]/main/form/div[5]/div[2]/button""")))
        final_booking.click()

    def close(self):

        self.driver.close()


def get_id():

    try:
        df = pd.read_csv(r'.\my_dates.csv', sep=';', decimal=',')
    except:
        df = pd.read_csv(r'./my_dates.csv', sep=';', decimal=',')

    df.dropna(inplace=True)

    df['date'] = df['date'].astype('str')
    df['date_id'] = df['date_id'].astype('int')

    date = datetime.today().date() + timedelta(4)

    date = date.strftime('%d/%m/%Y')

    try:

        my_id = df.loc[(df['date'] == date)]['date_id'].to_list()[0]
        print(my_id)

    except IndexError:

        my_id = None

    return my_id


def main():

    name = f"swimlog_{datetime.now().strftime('%d%m%Y_%H%M%S')}.log"
    name = f"swimlog.log"
    logging.basicConfig(filename=name, level=logging.DEBUG)

    swimpool_id = 79
    event_id = get_id()

    if event_id is None:
        logging.info("No Booking to be done today")
    else:

        bot = Booker()
        booking_successful = False
        counter = 1
        start_time_booking = perf_counter()

        while booking_successful is False:

            try:
                start_time = perf_counter()
                bot.get_booking(swimpool_id, event_id)
                end_time = perf_counter()
                logging.info(f"""Total booking lasted {round(end_time - start_time, 2)} seconds""")
                bot.close()
                booking_successful = True

            except NoSuchElementException:
                logging.info(f"Booking attempt # {counter} - {datetime.now().strftime('%Y-%d-%m %H:%M:%S')}")
                pass

            counter += 1
            end_time_booking = perf_counter()

            if (end_time_booking - start_time_booking) > (5*60):
                logging.info(f"All attempts timed out - {datetime.now().strftime('%Y-%d-%m %H:%M:%S')}")
                booking_successful = True



if __name__ == '__main__':

    main()
