from selenium import webdriver

class Driver:
    @staticmethod
    def setup():
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        return webdriver.Chrome(options=options)
