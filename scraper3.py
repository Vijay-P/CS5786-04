from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from matplotlib import pyplot as plt
from copy import deepcopy

# this was class modified from alecxe's answer at
# https://stackoverflow.com/questions/30964922/selenium-wait-until-text-in-webelement-changes


def run5k():
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
    return itr, los


class text_to_change(object):

    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        actual_text = driver.find_element(self.locator[0], self.locator[1]).text
        return actual_text != self.text

driver = webdriver.Firefox()
driver.get("http://cs.stanford.edu/people/karpathy/convnetjs/demo/image_regression.html")

layerdef = driver.find_element_by_id("layerdef")
defs = layerdef.get_attribute("value").split("\n")

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
i = 0
itr, los = run5k()
plt.plot(itr, los, color=colors[i])
i += 1

for x in range(2, 9):
    newdef = deepcopy(defs)
    for y in range(2, x + 1):
        newdef[y] = "//" + defs[y]
    newdef = "\n".join(newdef)
    print(newdef)
    print("\n")
    layerdef.clear()
    layerdef.send_keys(newdef)
    driver.find_element_by_id("buttontp").click()

    itr, los = run5k()
    plt.plot(itr, los, color=colors[i])
    i += 1

driver.close()

plt.title("Iterations v Loss")
plt.xlabel("Iterations")
plt.ylabel("Loss")
plt.savefig("nice3.png")
