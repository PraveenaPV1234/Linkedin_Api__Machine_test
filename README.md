                                                    LinkedIn Profile & Connection Scraper API

Project Overview


    This project provides an API service to log into LinkedIn, scrape the user's profile and connections, and return the scraped data. Built using Python, Selenium, and Flask, it 
    automates LinkedIn login, retrieves user profile details and connections using LinkedIn’s internal Voyager API, and provides this data through a Flask-based API.


Features

    -LinkedIn login with session persistence (cookies)

    -Fetch user's profile details via Voyager API

    -Fetch all connection details (name, title, profile URL) via Voyager API

    -Handles pagination to retrieve all available connections

    -Flask API endpoint to fetch profile + connection data

    -Basic Authentication to protect API access

    -Anti-bot measures (random delays, session reuse, automation control disabled)

    -Saves output in profile_and_connections.json

    -Defines the /fetch_profiles_connections endpoint for retrieving user's profile and their connection data.

    -Includes basic unit tests

Notes on Data Scraping Limitations

    -Missing Data: The scraper does not retrieve email and company details directly via the LinkedIn Voyager API.

        -The company name may sometimes be inferred from the title, but is not explicitly available in the API.

        -Email addresses are not accessible through the API and are not scraped. 

        -The data collected for each connection includes:

            -Name

            -Title

            -Profile Link

            -The Profile Picture is ignored in the current implementation.

    
Project Structure  

    Linkedin_API (Test) 
    │
    ├── chromedriver.exe               # WebDriver to control Chrome
    ├── config.json                    # Configuration file for LinkedIn login details
    ├── linkedin_cookies1.pkl          # Serialized cookies (session data) --> auto-generated
    ├── profile_and_connections.json   # Output file for scraped profile and connection data --> auto-generated
    ├── app.py                          # Flask application with API routes
    ├── README.md                       # Project documentation
    ├── test_app.py                     # Unit tests for validating the scraper's functionality
    ├── requirements.txt               # List of required Python libraries for the project
    └── Linkedin_scraper.py             # Main Python script for LinkedIn profile and connection scraping


Cloning the Repository

    git clone https://github.com/your-username/linkedin-scraper-api.git

    cd linkedin-scraper-api


Prerequisites

    
    | Tool/Lib                  | Purpose                                  |

    |--------------------------|------------------------------------------|
    | Python 3.x               | Core programming language                |
    | Selenium                 | Browser automation                       |
    | ChromeDriver             | Drives Chrome via Selenium               |
    | WebDriver Manager        | Installs & manages compatible ChromeDriver |
    | Voyager API (internal)   | Access LinkedIn profile/connection data  |
    | JSON, Pickle             | Data serialization                       |
    | LinkedIn Credentials     | Required for login                       |

                         
Setup Instructions

    
    1. Install requirements:

        pip install -r requirements.txt

    2. Add your LinkedIn credentials to config.json:

                {
                "username": "your_email_or_username",
                "password": "your_password"
                }

    3. Run the Flask app:

            python app.py

    4. The API will be accessible at http://127.0.0.1:5000/

API Endpoints

    POST /fetch_profiles_connections

    Fetch the logged-in user's profile details and connections.

Authentication: Basic Authentication (Username: admin, Password: secret)

Response: Returns a JSON object with user's profile and connection data.


Notes on Pagination & Limits

    -LinkedIn's Voyager API returns 40 connections per request

    -The scraper automatically loops with pagination until all connections are fetched

    -Voyager API may limit frequent access — random delays are added to avoid blocked or rate limited

    -Implement random delays using time.sleep(random.uniform(1, 5)) to mimic human behaviour

    -For a large number of connections, API requires pagination to be handled properly to avoid missing data


Unit Tests

    -To ensure the scraper works as expected, basic tests have been included:

        -Test for valid authentication and headers

        -Test for pagination logic to ensure all connections are fetched

        -Test for the JSON response structure
      
              python test_app.py
              python test_app.py           
