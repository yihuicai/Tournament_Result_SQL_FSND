1. Program Summary

This program uses a PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

2. How to run the program

There are three files in the folder.

tournament.sql: This file instantiates the database called "tournament". run "psql" command and connect to tournament database, then run the tournament.sql (\i tournament.sql) to configure.

tournament.py: This file contains all useful functions needed.

tournament_test.py: This file generates tests for the whole program. You can test program by running "python tournament_test.py".

