#!/bin/bash

# Initialize retstart

# retrieve data since 2025 01 01 until 2025 05 31

start_month=1

# Infinite loop to run the Python script every 2 seconds

while IFS= read -r line
do
    iterations=$line
    for ((i=13; i<=iterations; i++))
    do
    
        python3 query.py --start_day $i --start_month $start_month
        
        sleep 30m
    done
    start_month=$((start_month + 1))
done < input/month_day_2025.txt
