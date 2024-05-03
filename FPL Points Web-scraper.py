import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_fpl_data(team_id, gameweek, driver):
    url = f"https://fantasy.premierleague.com/entry/{team_id}/event/{gameweek}"
    driver.get(url)
    # Wait for the points element to load
    points_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.EntryEvent__PrimaryValue-l17rqm-4.fryVza"))
    )
    points = points_element.text
    return points

def main(team_ids, gameweeks):
    # Initialize CSV writer
    with open('FPL_weekly_tracker.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header row
        csv_writer.writerow(['Team ID'] + [f'Gameweek {gw}' for gw in gameweeks])
        # Set up Selenium with ChromeDriverManager
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.maximize_window()
        # Iterate through team ids
        for team_id in team_ids:
            row_data = [team_id]
            # Iterate through gameweeks
            for gameweek in gameweeks:
                points = scrape_fpl_data(team_id, gameweek, driver)
                row_data.append(points)
            # Write data for current team id
            csv_writer.writerow(row_data)
        driver.quit()

if __name__ == "__main__":
    team_ids = [2654272]  # Add more team ids as needed
    gameweeks = range(1, 39)  # Range from 1 to 38 for all gameweeks
    main(team_ids, gameweeks)


