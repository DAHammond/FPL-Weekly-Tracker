from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def scrape_fpl_data(team_id, gameweek, driver):
    url = f"https://fantasy.premierleague.com/entry/{team_id}/event/{gameweek}"
    driver.get(url)
    time.sleep(2)  # Adding a small delay to ensure page load

    # Check if cookie acceptance popup is present
    accept_button = driver.find_elements(By.ID, 'onetrust-accept-btn-handler')
    if accept_button:
        accept_button[0].click()  # Click "Accept All Cookies" button

    try:
        # Scrape points
        points_element = driver.find_element(By.CSS_SELECTOR, "div.EntryEvent__PrimaryValue-l17rqm-4.fryVza")
        points = points_element.text
        return points
    except Exception as e:
        print(f"Error while scraping points data for Team ID {team_id}, Gameweek {gameweek}: {e}")
        return None

def scrape_owner_name(team_id, driver):
    url = f"https://fantasy.premierleague.com/entry/{team_id}"
    driver.get(url)
    time.sleep(2)  # Adding a small delay to ensure page load

    try:
        # Scrape owner name
        owner_name_element = driver.find_element(By.CSS_SELECTOR, "div.Entry__EntryName-sc-1kf863-0.cMEsev")
        owner_name = owner_name_element.text
        return owner_name
    except Exception as e:
        print(f"Error while scraping owner name for Team ID {team_id}: {e}")
        return None

def scrape_team_name(team_id, driver):
    url = f"https://fantasy.premierleague.com/entry/{team_id}"
    driver.get(url)
    time.sleep(2)  # Adding a small delay to ensure page load

    try:
        # Scrape team name
        team_name_element = driver.find_element(By.CSS_SELECTOR, "div.Entry__TeamName-sc-1kf863-1.inZJya")
        team_name = team_name_element.text
        return team_name
    except Exception as e:
        print(f"Error while scraping team name for Team ID {team_id}: {e}")
        return None

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
            owner_name = scrape_owner_name(team_id, driver)
            team_name = scrape_team_name(team_id, driver)
            row_data = [team_id, owner_name, team_name]
            # Iterate through gameweeks
            for gameweek in gameweeks:
                points = scrape_fpl_data(team_id, gameweek, driver)
                row_data.append(points if points is not None else '')  # Append empty string if points are None
            # Write data for current team id
            csv_writer.writerow(row_data)
        driver.quit()

if __name__ == "__main__":
    team_ids = [2654272]  # Add more team ids as needed
    gameweeks = range(1, 39)  # Range from 1 to 38 for all gameweeks
    main(team_ids, gameweeks)



