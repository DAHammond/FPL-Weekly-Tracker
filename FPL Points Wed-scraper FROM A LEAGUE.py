from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def scrape_team_ids(league_id):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    url = f"https://fantasy.premierleague.com/leagues/{league_id}/standings/c"
    driver.get(url)

    try:
        # Wait for cookie acceptance button to appear
        cookie_button = driver.find_elements(By.ID, 'onetrust-accept-btn-handler')
        if cookie_button:
            cookie_button[0].click()  # Click "Accept All Cookies" button
            time.sleep(2)  # Adding a delay after accepting cookies

        # Scrape team ids
        team_ids = []
        team_links = driver.find_elements(By.XPATH, "//a[@class='Link-a4a9pd-1 kofttw']")
        for link in team_links:
            team_url = link.get_attribute('href')
            # Extract team id from URL
            team_id = team_url.split('/')[-3] if team_url else None
            if team_id:
                team_ids.append(team_id)
        
        print("Scraped team IDs:", team_ids)  # Debugging statement
        
        driver.quit()
        return team_ids
    except Exception as e:
        print(f"Error while scraping team ids for league ID {league_id}: {e}")
        driver.quit()
        return []

def scrape_fpl_data(team_id, gameweek, driver):
    url = f"https://fantasy.premierleague.com/entry/{team_id}/event/{gameweek}"
    driver.get(url)

    try:
        # Check for cookie acceptance button
        cookie_button = driver.find_elements(By.ID, 'onetrust-accept-btn-handler')
        if cookie_button:
            cookie_button[0].click()  # Click "Accept All Cookies" button
            time.sleep(2)  # Adding a delay after accepting cookies
        
        time.sleep(1)  # You can adjust the delay time as needed
        
        # Scrape points
        points_element = driver.find_element(By.CSS_SELECTOR, "div.EntryEvent__PrimaryValue-l17rqm-4.fryVza")
        points = points_element.text
        return points
    except Exception as e:
        print(f"Error while scraping points data for Team ID {team_id}, Gameweek {gameweek}: {e}")
        return None
    
def scrape_owner_and_team_name(team_id, driver):
    url = f"https://fantasy.premierleague.com/entry/{team_id}/event/1"
    driver.get(url)

    try:
        # Check for cookie acceptance button
        cookie_button = driver.find_elements(By.ID, 'onetrust-accept-btn-handler')
        if cookie_button:
            cookie_button[0].click()  # Click "Accept All Cookies" button
            time.sleep(2)  # Adding a delay after accepting cookies
        
        # Scrape owner name
        owner_name_element = driver.find_element(By.XPATH, "//div[@class='Entry__EntryName-sc-1kf863-0 cMEsev']")
        owner_name = owner_name_element.text
        
        # Scrape team name
        team_name_element = driver.find_element(By.XPATH, "//div[@class='Entry__TeamName-sc-1kf863-1 inZJya']")
        team_name = team_name_element.text
        
        return owner_name, team_name
    except Exception as e:
        print(f"Error while scraping owner name and team name for Team ID {team_id}: {e}")
        return None, None

def main(team_ids, gameweeks):
    # Initialize CSV writer
    with open('FPL_weekly_tracker.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header row
        csv_writer.writerow(['Team ID', 'Owner Name', 'Team Name'] + [f'Gameweek {gw}' for gw in gameweeks])
        # Set up Selenium with Chrome webdriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        
        # Iterate through team ids
        for team_id in team_ids:
            owner_name, team_name = scrape_owner_and_team_name(team_id, driver)
            if owner_name is None or team_name is None:
                print(f"Skipping Team ID {team_id} due to missing owner name or team name")
                continue
            row_data = [team_id, owner_name, team_name]
            # Iterate through gameweeks
            for gameweek in gameweeks:
                points = scrape_fpl_data(team_id, gameweek, driver)
                row_data.append(points if points is not None else '')  # Append empty string if points are None
            # Write data for current team id
            csv_writer.writerow(row_data)
        
        driver.quit()

if __name__ == "__main__":
    league_id = 1927352  ###################### Enter the league id here ###########################################
    gameweeks = range(1, 39)  # Range from 1 to 38 for all gameweeks
    team_ids = scrape_team_ids(league_id)
    main(team_ids, gameweeks)

