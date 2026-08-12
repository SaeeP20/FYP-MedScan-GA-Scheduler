# Optimising Medical Imaging Scheduling using Genetic Algorithms

## Overview

This project implements a Genetic Algorithm (GA) to optimise the generation of feasible and efficient patient schedules under real-world constraints. It includes a graphical user interface (GUI), Excel exports, and a clean MVC architecture to ensure maintainability.

This project has been developed as a part of the **MSci Computer Science (Artificial Intelligence) course at Royal Holloway, University of London**

## Project Structure

├── GA_code
│   ├── Test
│   │   ├── parameters.py
│   │   ├── test_GA.py
│   │   ├── test_UI.py
│   ├── GA_firstPT.py
│   ├── GA_UI.py
│   ├── local_search.py
├── Supporting_files
│   ├── Test
│   │   ├── test_patients.csv
│   │   ├── test_schedule.xlsx
│   ├── patients.csv
│   ├── schedule.xlsx
│   ├── requirements.txt
├── diary.md
├── README.md

## How to Run Program

1. Install dependencies inside terminal using:
    `pip install -r requirements.txt`
2. Ensure all [supporting documents](https://gitlab.cim.rhul.ac.uk/zlac324/PROJECT/-/tree/24054feaddd822f876c71b42c8d2dd095840e5b4/Supporting%20Files) are in the same working directory
3. Launch applications with:
    `python GA_firstPT.py`
    `python GA_UI.py`
4. Using the GUI:
    - Adjust parameters as needed
    - Using main() in GA_firstPT.py, run GA 
    
    **OR**
    
    - Proceed with employee stream using main() in GA_UI.py, to run GA and generate and export schedule

## Author

**Saee Pujari**

MSci Computer Science (Artificial Intelligence)

Royal Holloway, University of London
