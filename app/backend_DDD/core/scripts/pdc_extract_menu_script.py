import json
import requests
from bs4 import BeautifulSoup


# eateries dict
# {
#     'name': 'eatery name',
#     'link': 'eatery link'
# }

# menu dict
# {
#     'name': 'dish name',
#     'image_link': 'menu link'
#     'price': {
#         'Full': '',
#         'Half': '',
#         'Quarter': '',
#         }
# }



base_url = 'https://pdc.lums.edu.pk/'

def get_response(req:str = None, req_url: str = '', retries: int = 3):
    while retries > 0:
        if req:
            response = requests.get(req)
        else:
            response = requests.get(base_url + req_url)
        if response.status_code == 200:
            return response
        retries -= 1
    return None


def get_eateries_names(response: requests.models.Response) -> list[dict]:

    html_content = response.text
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract eateries with names and links
    eateries = []

    

    for item in soup.select(".PriceTag .FoodName a"):

        item_box = item.find_parent('div', class_='PriceTag').find_previous_sibling('div', class_='item-box')
        image = item_box.find('img') if item_box else None

        eateries.append({
            "name": item.get_text(strip=True),
            "image": image['src'] if image else '', 
            "link": item['href']
        })
    return eateries

def get_eateries_menu_pak_cuisine(response: requests.models.Response) -> list[dict]:
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize list to store menu items
    menu = []

    # Select each menu item
    for dish in soup.select(".col"):
        # Extract dish name
        name_div = dish.select_one(".d-flex.flex-column.justify-content-between div[style*='font-weight: 800']")
        name = name_div.get_text(strip=True) if name_div else 'Unknown Dish'
        

        # Extract image link directly within the ".col" container
        image_tag = dish.select_one("img")
        image_link = image_tag['src'] if image_tag else ''
        

    
        # Extract prices
        price_tags = dish.select_one(".d-flex.justify-content-around").get_text(separator="|", strip=True).split("|")
        prices = {"Full": "", "Half": "", "Quarter": ""}
    
        # Assign prices based on tags or default to Full if no tag
        for price in price_tags:
            if "F:" in price:
                prices["Full"] = price.replace("F:", "").strip()
            elif "H:" in price:
                prices["Half"] = price.replace("H:", "").strip()
            elif "Q:" in price:
                prices["Quarter"] = price.replace("Q:", "").strip()
            else:
                prices["Full"] = price.strip()
    
        # Append to menu
        menu.append({
            "name": name,
            "image_link": image_link,
            "price": prices
        })
    return menu

def get_eateries_menu_secondary(response: requests.models.Response) -> list[dict]:
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize list to store menu items
    menu = []

    # Select each menu item
    for dish in soup.select(".row.TopMarg"):
        name_div = dish.select_one(".FoodName")
        name = name_div.get_text(strip=True) if name_div else 'Unknown Dish'

        # Extract image link directly within the ".col" container
        image_tag = dish.select_one("img")
        image_link = image_tag['src'] if image_tag else ''

        # Extract prices
        price_tags = dish.select_one(".Prices-Full").get_text(separator="|", strip=True).split("|")
        prices = {"Full": "", "Half": "", "Quarter": ""}
    
        # Assign prices based on tags or default to Full if no tag
        for price in price_tags:
            if "F:" in price:
                prices["Full"] = price.replace("F:", "").strip()
            elif "H:" in price:
                prices["Half"] = price.replace("H:", "").strip()
            elif "Q:" in price:
                prices["Quarter"] = price.replace("Q:", "").strip()
            else:
                prices["Full"] = price.strip()
    
        # Append to menu
        menu.append({
            "name": name,
            "image_link": image_link,
            "price": prices
        })

    return menu

def get_eateries_menu_bakery(response: requests.models.Response) -> list[dict]:
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize list to store menu items
    menu = []

    # Select each menu item
    for dish in soup.select(".col-lg-2.col-md-3.col-sm-4.col-xs-6.TopMarg"):
        name_div = dish.select_one(".FoodName")
        name = name_div.get_text(strip=True) if name_div else 'Unknown Dish'

        # Extract image link directly within the ".col" container
        image_tag = dish.select_one("img")
        image_link = image_tag['src'] if image_tag else ''

        # Extract prices
        price_tags = dish.select_one(".Prices-Full").get_text(separator="|", strip=True).split("|")
        prices = {"Full": "", "Half": "", "Quarter": ""}
    
        # Assign prices based on tags or default to Full if no tag
        for price in price_tags:
            if "F:" in price:
                prices["Full"] = price.replace("F:", "").strip()
            elif "H:" in price:
                prices["Half"] = price.replace("H:", "").strip()
            elif "Q:" in price:
                prices["Quarter"] = price.replace("Q:", "").strip()
            else:
                prices["Full"] = price.strip()
    
        # Append to menu
        menu.append({
            "name": name,
            "image_link": image_link,
            "price": prices
        })

    return menu

def get_eateries_menu_fastfood(response: requests.models.Response) -> list[dict]:
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize list to store menu items
    menu = []

    # Select each menu item
    for dish in soup.select(".col-lg-2.col-md-3.col-sm-4.col-xs-6"):
        name_div = dish.select_one(".FoodName")
        name = name_div.get_text(strip=True) if name_div else 'Unknown Dish'

        # Extract image link directly within the ".col" container
        image_tag = dish.select_one("img")
        image_link = image_tag['src'] if image_tag else ''

        # Extract prices
        price_tags = dish.select_one(".Prices-Full").get_text(separator="|", strip=True).split("|")
        prices = {"Full": "", "Half": "", "Quarter": ""}
    
        # Assign prices based on tags or default to Full if no tag
        for price in price_tags:
            if "F:" in price:
                prices["Full"] = price.replace("F:", "").strip()
            elif "H:" in price:
                prices["Half"] = price.replace("H:", "").strip()
            elif "Q:" in price:
                prices["Quarter"] = price.replace("Q:", "").strip()
            else:
                prices["Full"] = price.strip()
    
        # Append to menu
        menu.append({
            "name": name,
            "image_link": image_link,
            "price": prices
        })

    return menu

def get_eateries_menu_pan(response: requests.models.Response) -> list[dict]:
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize list to store menu items
    menu = []

    # Select each menu item
    for dish in soup.select(".col-md-3.col-sm-6.TopMarg"):
        name_div = dish.select_one(".FoodName")
        name = name_div.get_text(strip=True) if name_div else 'Unknown Dish'

        # Extract image link directly within the ".col" container
        image_tag = dish.select_one("img")
        image_link = image_tag['src'] if image_tag else ''

        # Extract prices
        price_tags = dish.select_one(".Price").get_text(separator="|", strip=True).split("|")
        prices = {"Full": "", "Half": "", "Quarter": ""}
    
        # Assign prices based on tags or default to Full if no tag
        for price in price_tags:
            if "F:" in price:
                prices["Full"] = price.replace("F:", "").strip()
            elif "H:" in price:
                prices["Half"] = price.replace("H:", "").strip()
            elif "Q:" in price:
                prices["Quarter"] = price.replace("Q:", "").strip()
            else:
                prices["Full"] = price.strip()
    
        # Append to menu
        menu.append({
            "name": name,
            "image_link": image_link,
            "price": prices
        })

    return menu

def get_eateries_menu_healthy(response: requests.models.Response) -> list[dict]:
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize list to store menu items
    menu = []

    # Select each menu item
    for dish in soup.select(".col-md-3.col-sm-6.TopMarg"):
        name_div = dish.select_one(".FoodName")
        name = name_div.get_text(strip=True) if name_div else 'Unknown Dish'

        # Extract image link directly within the ".col" container
        image_tag = dish.select_one("img")
        image_link = image_tag['src'] if image_tag else ''

        # Extract prices
        price_tags = dish.select_one(".Price").get_text(separator="|", strip=True).split("|")
        prices = {"Full": "", "Half": "", "Quarter": ""}
    
        # Assign prices based on tags or default to Full if no tag
        for price in price_tags:
            if "F:" in price:
                prices["Full"] = price.replace("F:", "").strip()
            elif "H:" in price:
                prices["Half"] = price.replace("H:", "").strip()
            elif "Q:" in price:
                prices["Quarter"] = price.replace("Q:", "").strip()
            else:
                prices["Full"] = price.strip()
    
        # Append to menu
        menu.append({
            "name": name,
            "image_link": image_link,
            "price": prices
        })

    return menu


# Function to insert an eatery
def insert_eatery(cursor, eatery_name, eatery_link, eatery_image):
    cursor.execute(
        "INSERT INTO pdc_eateries (name, link, image_link) VALUES (%s, %s, %s) RETURNING id",
        (eatery_name, eatery_link, eatery_image)
    )
    return cursor.fetchone()[0], 

# Function to insert a menu item
def insert_menu_item(cursor, eatery_id, item_name, image_link):
    cursor.execute(
        "INSERT INTO pdc_menu_items (eatery_id, name, image_link) VALUES (%s, %s, %s) RETURNING id",
        (eatery_id, item_name, image_link)
    )
    return cursor.fetchone()[0]

# Function to insert a price
def insert_price(cursor, menu_item_id, price_type, price_value):
    cursor.execute(
        "INSERT INTO pdc_menu_prices (menu_item_id, type, price) VALUES (%s, %s, %s)",
        (menu_item_id, price_type, float(price_value))
    )

def clear_data(cursor):
    cursor.execute("TRUNCATE TABLE pdc_menu_prices, pdc_menu_items, pdc_eateries ;")
    # cursor.execute("TRUNCATE TABLE pdc_menu_items;")
    # cursor.execute("TRUNCATE TABLE pdc_eateries")

    print("Cleared existing data.")


functions = {
'PAKISTANI CUISINE' : get_eateries_menu_pak_cuisine, # Done
'FAST FOOD AND SNACKS' : get_eateries_menu_fastfood, # Done
'PAN ASIAN / MEDITERRANEAN CUISINE' : get_eateries_menu_pan, # Done
'BAKERY & DRINKS' : get_eateries_menu_bakery, # Done
'HEALTHY / SALAD' : get_eateries_menu_healthy, # Done
'Baithak' : get_eateries_menu_pak_cuisine, # Done
'Green Olive' : get_eateries_menu_pak_cuisine, # Done
}

def start_extracting_pdc_menu() -> dict:
    response = get_response(req=base_url)
    data = []
    if response:
        # print('PDC Response received')
        eateries = get_eateries_names(response)
        # print('Eateries extracted')
        
        for eatery in eateries:
            response = get_response(req=eatery['link'])
            if response:
                # print(f"Extracting menu for {eatery['name']}")
                menu = functions[eatery['name']](response)
                data.append({
                    "eatery": eatery['name'],
                    "link": eatery['link'],
                    "image": eatery['image'],
                    "menu": menu
                })
            
    else:
        print('Failed to get response from PDC')
    
    if len(data) > 0:
        return data
    else:
        return None