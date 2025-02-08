import json
import requests

def captchadetector(data):
    matches = (
        "https://www.google.com/recaptcha/api.js?from=i13_recaptcha&amp;render=",
        "https://www.google.com/recaptcha/api.js?render=",
        "siteKey"
    )
    return 'Captcha' if any(match in data for match in matches) else ''

def woocommercepm_api(domain):
    G = "\033[38;5;82m"
    Y ="\033[38;5;226m"
    R2 = "\033[38;5;202m"
    R = "\033[0m"

    session = requests.Session()

    #requests 1
    try:
        url = f"https://{domain}/wp-json/wc/store/cart"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Pragma": "no-cache",
            "Accept": "*/*",
        }
        response = session.get(url, headers=headers)
    except Exception as e:
        return print(f"[{Y}!{R}] {Y}{domain}{R} requests 1 An error occurred during processing: {e}")

    if "payment_methods" in response.text:
        payment_methods = json.loads(response.text)["payment_methods"]

        if not payment_methods:
            return print(f"[{R2}-{R}] {R2}{domain}{R} No payment methods available.")
        
        payment = ", ".join(payment_methods)

        #requests 2
        try:
            url = f"https://{domain}/?=&post_type=product"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Pragma": "no-cache",
                "Accept": "*/*",
            }
            response = session.get(url, headers=headers)

            split_text = response.text.split('data-product_id="')
            if len(split_text) > 1:
                id = split_text[1].split('"')[0]
            else:
                return print(f"[{R2}-{R}] {R2}{domain}{R} Failed to find product id.")
        except Exception as e:
            return print(f"[{Y}!{R}] {Y}{domain}{R} requests 2 An error occurred during processing: {e}")
            
        #requests 3
        try:
            url = f"https://{domain}/?wc-ajax=add_to_cart"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Pragma": "no-cache",
                "Accept": "*/*",
            }
            data = {
                'quantity': 1,
                'add-to-cart': id
            }
            response = session.post(url, headers=headers, data=data,)
            if response.status_code not in (200, 302):
                return print(f'[{Y}!{R}] {Y}{domain}{R} Failed to add item to cart.')
        except Exception as e:
            return print(f"[{Y}!{R}] {Y}{domain}{R} requests 3 An error occurred during processing: {e}")
        
        #requests 4
        try:
            url = f"https://{domain}/checkout/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                "Pragma": "no-cache",
                "Accept": "*/*",
            }
            response = session.get(url, headers=headers)

            captcha = captchadetector(response.text)

            print(f"[{G}+{R}] {G}{domain}{R} - {payment} {captcha}")
            with open('woocommerce.txt', 'a') as file:
                return file.write(f'{domain} - {payment} {captcha}\n')

        except Exception as e:
            return print(f"[{Y}!{R}] {Y}{domain}{R} requests 4 An error occurred during processing: {e}")
    else:
        return print(f"[{R2}-{R}] {R2}{domain}{R}")
    