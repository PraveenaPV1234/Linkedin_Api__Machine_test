import json
import pickle
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import random

def main(return_data=False):
    # Load credentials
    with open("config.json", "r") as file:
        config = json.load(file)
    USERNAME = config["username"]
    PASSWORD = config["password"]
    chrome_driver_path = r"chromedriver.exe" 

    # Chrome options
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")

    # Start WebDriver
    print("Starting WebDriver...")
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    def is_logged_in(driver):
        try:
            # Look for the "Me" text in the span element with the class "global-nav__primary-link-text"
            me_text = driver.find_element(By.XPATH, "//span[contains(text(), 'Me')]")
            return True
        except Exception as e:
            print(f"Login check failed: {e}")
            return False
    # Load cookies if available
    def extract_connections(data):
        connections = []
        for element in data.get("elements", []):
            profile = element.get("connectedMemberResolutionResult", {})
            if not profile:
                print(" Skipped a connection: No profile data")
                continue
            first_name = profile.get("firstName", "")
            last_name = profile.get("lastName", "")
            full_name = f"{first_name} {last_name}".strip()

            headline = profile.get("headline", "")
            public_id = profile.get("publicIdentifier", "")
            profile_url = f"https://www.linkedin.com/in/{public_id}"
            connections.append({
                "name": full_name,
                "Title": headline,
                "profile_url": profile_url,     
                "Email": "Email not Available"
            
            }) # Unable to retrieve email and company details directly via the LinkedIn Voyager API.
        return connections
    def relogin(driver):
        print("Session expired or not logged in. Logging in again...")
        driver.get("https://www.linkedin.com/login")
        time.sleep(20)
        # Optional: Click "Sign in using another account"
        try:
            other_account_btn = driver.find_element(By.XPATH, "//*[@id='rememberme-div']/div[3]/div/button/p")
            other_account_btn.click()
            time.sleep(random.uniform(2, 5))
        except:
            pass  # Button may not appear if it's first time logging in
        driver.find_element(By.ID, "username").send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(random.uniform(2, 5))

        # Save cookies after login
        with open("linkedin_cookies1.pkl", "wb") as f:
            pickle.dump(driver.get_cookies(), f)

        print("Login successful. Session saved.")
    if os.path.exists("linkedin_cookies1.pkl"):
        print("Cookies found, loading session...")
        with open("linkedin_cookies1.pkl", "rb") as f:
            cookies = pickle.load(f)
        driver.get("https://www.linkedin.com/")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(random.uniform(2, 5))  # Allow time for page to settle
        print("Session loaded successfully.")
    else:
        print("No cookies found, logging in...")
        time.sleep(random.uniform(2, 5))
        relogin(driver)

    # Check if logged in by looking for "Me" text
    if not is_logged_in(driver):
        print("Session is invalid or expired. Re-logging...")
        time.sleep(random.uniform(2, 5))
        relogin(driver)
    else:

        # Continue with further tasks once the user is logged in
        print("User is logged in and session is active.") 
    # CSRF Token
    cookies = driver.get_cookies()
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    csrf_token = cookie_dict.get('JSESSIONID', '').strip('"')

    # ============  FETCH USER PROFILE ============
    user_data = driver.execute_script("""
        return fetch("https://www.linkedin.com/voyager/api/me", {
            method: "GET",
            headers: {
                "csrf-token": arguments[0],
                "x-restli-protocol-version": "2.0.0",
                "accept": "application/json"
            }
        }).then(res => res.json());
    """, csrf_token)

    User_data = []
    if user_data:
        mini = user_data.get("miniProfile", {})
        name = f"{mini.get('firstName', '')} {mini.get('lastName', '')}"
        title = mini.get('occupation', '')
        public_id = mini.get("publicIdentifier", "")
        profile_url = f"https://www.linkedin.com/in/{public_id}"
        User_data.append({
            "name": name,
            "Title": title,
            "profile_url": profile_url,
            "Email": "Email not Available"
        }) # Unable retrieve email and company details directly via the LinkedIn Voyager API.
    else:
        print(" Failed to fetch user profile.")

    # ============  FETCH CONNECTIONS ============
    # Loop through paginated connections
    start = 0
    all_connections=[]
    while True:
    
        url = f"https://www.linkedin.com/voyager/api/relationships/dash/connections?decorationId=com.linkedin.voyager.dash.deco.web.mynetwork.ConnectionListWithProfile-16&count=40&q=search&sortType=RECENTLY_ADDED&start={start}"
        data = driver.execute_script("""
            return fetch(arguments[0], {
                method: "GET",
                headers: {
                    "csrf-token": arguments[1],
                    "x-restli-protocol-version": "2.0.0",
                    "accept": "application/json"
                }
            }).then(res => res.ok ? res.json() : null);
        """, url, csrf_token)
        results = extract_connections(data)
        if not results:
                break
        all_connections.extend(results)
        start += 40
        time.sleep(random.uniform(5, 8))  # Helps avoid rate-limiting
        
    print(f"\nTotal connections fetched: {len(all_connections)}")
    result = {
    "profile": User_data,
    "connections": all_connections
}

    if return_data:
        driver.quit()
        return result
    else:
        with open("profile_and_connections.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        driver.quit()

        
if __name__ == "__main__":
    main()