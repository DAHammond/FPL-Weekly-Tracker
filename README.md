# FPL-Weekly-Tracker
This project aims to create a robust and transferable web-scraping and graph creation combination to be able to show the relative progress of each individual's Fantasy Premier League (FPL) Team throughout the season. 

## Files in this repository
* README
* FPL Points Web-scraper USING INDIVIDUAL TEAM CODES.py - the web-scraping code to get points from each individual team. This code can be used for any individual's team by looking at the string in the url when viewing the team on FPL online and adding it to the team_ids list at the end of the /PY file
* FPL Points Web-scraper FROM A LEAGUE.py - the web-scraping code to get points from each individual team within a given league. This code can be used for any league by looking for the number string in the url bar when viewing the league on FPL online. This id will need to be placed as the league_id at the end of the .py file
* FPL_weekly_tracker.csv - the output file from running either of the web-scraping files

## Replication --> How to use for different teams/leagues
### For the individual team id route
1. Visit the FPL website and select the points view for the team you would like to scrape
2. Look into the URL bar to get the 7 character string (/entry/000000/event)
3. Put the selected character strings into the 'team_ids' list at the end of the appropriate .py file
4. Run the code to get the output file
5. Run the Juptyr notebook to get the graphs 

### For the league route
1. Visit the FPL website and select the league you would like to scrape
2. Look into the URL bar to get the 7 character string (/leagues/000000/standings)
3. Replace the league_id with your 7 character string at the end of the appropriate .py file
4. Run the code to get the output file
5. Run the Juptyr notebook to get the graphs 