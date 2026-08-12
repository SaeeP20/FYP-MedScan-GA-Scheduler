# Optimising Medical Imaging Scheduling Using Genetic Algorithms

## 📋 Overview

This project implements a **Genetic Algorithm (GA)** to optimise the generation of feasible and efficient patient schedules under real-world medical imaging constraints.

The system includes:

* 🧬 A Genetic Algorithm for schedule optimisation
* 🖥️ A graphical user interface (GUI)
* 📊 Excel schedule exports
* 🔍 Local search optimisation
* 🧪 Automated testing
* 🏗️ A clean **Model-View-Controller (MVC)** architecture designed for maintainability

This project was developed as part of the **MSci Computer Science (Artificial Intelligence)** course at **Royal Holloway, University of London**.

---

## 📁 Project Structure

```text
Optimising-Medical-Imaging-Scheduling/
│
├── GA_code/
│   ├── Test/
│   │   ├── parameters.py
│   │   ├── test_GA.py
│   │   └── test_UI.py
│   │
│   ├── GA_firstPT.py
│   ├── GA_UI.py
│   └── local_search.py
│
├── Supporting_files/
│   ├── Test/
│   │   ├── test_patients.csv
│   │   └── test_schedule.xlsx
│   │
│   ├── patients.csv
│   ├── schedule.xlsx
│   └── requirements.txt
│
├── diary.md
└── README.md
```

## How to Run Program

1. Install dependencies inside terminal using:
    `pip install -r requirements.txt`
2. Ensure all [supporting documents](https://github.com/SaeeP20/FYP-MedScan-GA-Scheduler/tree/main/Code_%26_SupportingDocuments/Requirements%20%2B%20Supporting%20Docs) are in the same working directory
3. Launch applications with:
    `python GA_firstPT.py`
    `python GA_UI.py`
4. Using the GUI:
    - Adjust parameters as needed
    - Using main() in GA_firstPT.py, run GA 
    
    **OR**
    
    - Proceed with employee stream using main() in GA_UI.py, to run GA and generate and export schedule

---

## 🧬 Genetic Algorithm

The optimisation process uses evolutionary techniques to search for efficient patient schedules while satisfying the constraints of the medical imaging environment.

The algorithm includes components such as:

* Population generation
* Fitness evaluation
* Constraint handling
* Selection
* Crossover
* Mutation
* Local search
* Convergence / stopping criteria

The objective is to produce schedules that improve factors such as **patient waiting times, resource utilisation, and overall scheduling efficiency**, while maintaining feasibility under the defined constraints.

---

## 🧪 Testing

The project includes automated tests for both the Genetic Algorithm and the GUI.

Test files are located in:

```text
GA_code/
└── Test/
    ├── parameters.py
    ├── test_GA.py
    └── test_UI.py
```

Run the relevant tests using your preferred Python testing framework.

---

## 📊 Input & Output

### Input

Patient information is provided through:

```text
Supporting_files/patients.csv
```

### Output

Generated schedules can be exported to Excel format:

```text
Supporting_files/schedule.xlsx
```

This allows the optimised schedules to be reviewed and analysed outside of the application.

---

## 🏗️ Architecture

The project follows an **MVC (Model-View-Controller)** architecture to separate the scheduling logic, user interface, and application control.

This structure improves:

* Maintainability
* Modularity
* Testing
* Separation of concerns
* Future extensibility

---

## 📚 Course

Developed as part of the:

**MSci Computer Science (Artificial Intelligence)**
**Royal Holloway, University of London**

---

## 👤 Author

**Saee Pujari**

MSci Computer Science (Artificial Intelligence)
Royal Holloway, University of London

