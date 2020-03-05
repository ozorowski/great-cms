from io import BytesIO

import allure
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

from tests.browser.common_selectors import Selector


def convert_png_to_jpg(screenshot_png: bytes) -> bytes:
    raw_image = Image.open(BytesIO(screenshot_png))
    image = raw_image.convert('RGB')
    with BytesIO() as f:
        image.save(f, format='JPEG', quality=90)
        return f.getvalue()


def attach_jpg_screenshot(
        browser: WebDriver, page_name: str, *, selector: Selector = None
):
    if selector:
        element = find_element(browser, selector)
        screenshot_png = element.screenshot_as_png
    else:
        screenshot_png = browser.get_screenshot_as_png()
    screenshot_jpg = convert_png_to_jpg(screenshot_png)
    allure.attach(
        screenshot_jpg,
        name=page_name,
        attachment_type=allure.attachment_type.JPG,
        extension='jpg'
    )


def is_element_present(browser: WebDriver, selector: Selector) -> bool:
    """Check if sought element is present.

    If selector returns more than 1 element then find_element() will return the first
    element from the list.
    """
    found = True
    try:
        browser.find_element(by=selector.by, value=selector.selector)
    except NoSuchElementException:
        found = False
    return found
