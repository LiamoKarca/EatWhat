import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError


def scroll_restaurants_list(page):
    """
    Scroll through the restaurant list.
    """
    print("Scroll: Is at bottom:", is_at_page_bottom(page))
    if is_at_page_bottom(page):
        print("Scroll: Reached bottom.")
    else:
        print("Scroll: Not yet reached!!!")
    for _ in range(1):  # Can adjust scrolling times
        if page.is_closed():
            break
        html = page.inner_html('body')
        soup = BeautifulSoup(html, 'html.parser')
        categories = soup.select('.hfpxzc')
        if categories:
            last_category_in_page = categories[-1].get('aria-label')
            last_category_location = page.locator(f"text={last_category_in_page}")
            try:
                last_category_location.scroll_into_view_if_needed(timeout=10000)
            except TimeoutError:
                print("Timeout occurred while scrolling.")
                break
            page.wait_for_load_state("networkidle")


def get_restaurants():
    """
    First, set up browser and map location for restaurants.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch browser
        context = browser.new_context(geolocation={"longitude": 120.5966694, "latitude": 22.6427084},
                                      permissions=["geolocation"])
        page = context.new_page()

        # Listen for dialogs and accept them
        page.on('dialog', lambda dialog: dialog.accept())

        # Open specified URL in Google Maps
        page.goto(
            "https://www.google.com.tw/maps/search/%E9%99%84%E8%BF%91%E5%90%83%E7%9A%84/@22.6427084,120.5966694,"
            "15.33z/data=!4m4!2m3!5m1!2e1!6e5?entry=ttu")

        # Wait for page to load
        page.wait_for_selector('.hfpxzc')

        # Click the update button
        page.click(".D6NGZc")

        # Click the locate button
        page.click('//*[@id="sVuEFc"]/div')

        # Wait for map to finish locating (Wait for network to idle)
        page.wait_for_load_state("networkidle")

        """
        Second, get restaurants and their addresses.
        """
        restaurants = []
        count = 0

        while True:
            try:
                div_aifcqe = page.query_selector(
                    '.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd')  # Find div elements with class 'aIFcqe'
                hfpxzc_elements = div_aifcqe.query_selector_all('.hfpxzc')  # Find elements with specific class in that div

                for item in hfpxzc_elements:
                    link = item.get_attribute('href')
                    name = item.get_attribute('aria-label')

                    if (name, link) not in restaurants:
                        restaurants.append((name, link))

                        count += 1
                        print(f'Count {count}: {name}')

                if not is_at_page_bottom(page):
                    scroll_restaurants_list(page)

                if is_at_page_bottom(page):
                    for item in hfpxzc_elements:
                        link = item.get_attribute('href')
                        name = item.get_attribute('aria-label')
                        print(f'Count {count}: {name}')
                        if (name, link) and (name, link) not in restaurants:
                            restaurants.append((name, link))
                            count += 1
                            print(f'Count {count}: {name}')

                    print("GetRest: Reached bottom.")
                    return restaurants

            except TimeoutError:
                print("TimeoutError occurred. Returning collected restaurants.")
                return restaurants


def is_at_page_bottom(page):
    """
    Check if bottom of page is reached.
    """
    css_selector = 'p.fontBodyMedium:has-text("你已看完所有搜尋結果。")'
    elements = page.query_selector_all(css_selector)
    if len(elements) > 0:
        time.sleep(3)  # Wait for 3 seconds
        elements = page.query_selector_all(css_selector)
        return len(elements) > 0
    return False


# Main program
if __name__ == "__main__":
    restaurants = get_restaurants()
    print(restaurants)
