from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from matplotlib import pyplot as plt

# this was class modified from alecxe's answer at
# https://stackoverflow.com/questions/30964922/selenium-wait-until-text-in-webelement-changes


class text_to_change(object):

    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        actual_text = driver.find_element(self.locator[0], self.locator[1]).text
        return actual_text != self.text

driver = webdriver.Firefox()
driver.get("http://cs.stanford.edu/people/karpathy/convnetjs/demo/image_regression.html")

itr = []
los = []

element = driver.find_element_by_id("report")
current = element.text
items = current.split("\n")
loss = float(items[0].split(": ")[1])
iteration = int(items[1].split(": ")[1])
itr.append(iteration)
los.append(loss)

while(iteration < 5000):
    try:
        WebDriverWait(driver, 0.1).until(
            text_to_change((By.ID, "report"), current)
        )
        current = element.text
        items = current.split("\n")
        loss = float(items[0].split(": ")[1])
        iteration = int(items[1].split(": ")[1])
        itr.append(iteration)
        los.append(loss)
    except selenium.common.exceptions.TimeoutException:
        pass

driver.close()

plt.plot(itr, los)
plt.title("Iterations v Loss")
plt.xlabel("Iterations")
plt.ylabel("Loss")
plt.savefig("nice.png")
