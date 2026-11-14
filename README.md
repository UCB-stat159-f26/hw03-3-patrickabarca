
# HW 3 Tennis Career Data and Visualization Package

## Description
The motivation behind this project is to create a Python package that retrieves and processes career match data of professional tennis players from Tennis Abstract. This project is a continuation of HW1 and HW2, which aimed to reproduce the New York Times visualization "Serena Williams's Professional Matches, Age 14 to 40" by Ziegler, S., & Dominguez. The package allows users to retrieve career match data by entering a player's name and generate a scatterplot depicting the player's age vs their opponents' age difference, highlighting wins and losses.

### Project Structure
* scripts/player_data.py — Downloads and processes player career data
* scripts/plot.py — Produces the tennis career visualization
* scripts/__init__.py — Exposes the package's functions
* tests/test_career_data.py — Contains unit tests for data extraction and processing
* tests/test_data/ — Contains mock JS data for male and female players
* pyproject.toml — Specifies package configuration and dependencies

### Executing Program

From main directory install package:
* `pip install -e .`

To import package:

    from scripts import get_player_career, plot_career

To retrieve and plot player data:

    serena = get_player_career("Serena Williams")
    plot_career(serena)

    rafa = get_player_career("Rafael Nadal")
    plot_career(rafa)

To run unit tests:
* `python -m pytest -v`

## Reflections
Through this project, I learned the importance of organizing related functions into a package so that code can be easily reused, installed, and shared with others. I also learned how to use pytest to test data extraction and processing using mock JS files without relying on live website requests. One challenge I had difficult with was handling the differences between male and female career data, as female players' files contain opponents' birthdates while male players' files contain opponents' ages. Another challenge was retrieving player birthdates from Tennis Abstract due to website response issues and runtimes.

## Author
Patrick Abarca

## Sources
https://www.nytimes.com/interactive/2022/08/28/sports/tennis/serena-age-opponents.html

https://www.tennisabstract.com/cgi-bin/wplayer-classic.cgi?p=SerenaWilliams

https://www.tennisabstract.com/cgi-bin/player-classic.cgi?p=RafaelNadal

https://www.tennisabstract.com/jsmatches/SerenaWilliamsCareer.js

https://www.tennisabstract.com/jsmatches/RafaelNadalCareer.js
