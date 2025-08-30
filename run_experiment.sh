#!/bin/bash

# Initialize retstart

# retrieve data since 2025 01 01 until 2025 05 31

# Infinite loop to run the Python script every 2 seconds
iterations=400
# while IFS= read -r line
# do
#redo 14, 21

for ((i=228; i<=iterations; i++))
do

    python3 query.py --start_day 1 --start_month 1 --position $i
    
    # sleep 30m
done
    # start_month=$((start_month + 1))
# done < input/month_day_2025.txt
