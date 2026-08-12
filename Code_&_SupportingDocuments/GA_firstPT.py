import numpy as np
import GA_UI as ui
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple

genotype = List[int]
population = List[genotype]

np.random.seed(37)  # for reproducibility - ONLY FOR TESTING PURPOSES

patients = ui.load_patients("patients.csv")
wb, sheet = ui.load_schedule("schedule.xlsx")

day_map = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4}

# PRE-COMPUTED CONSTANTS (for efficiency in fitness function)
NUM_MACHINES = 1
TOTAL_SLOTS = (sheet.max_row - 1) * (sheet.max_column - 1) * NUM_MACHINES

PREF_SLOT = patients["preferred_slot"].tolist()
PREF_TIME = patients["preferred_time"].tolist()
PREF_DAY  = patients["preferred_day"].tolist()

DAY_INDEX = [s // 12 for s in range(60)]
TIME_INDEX = [s % 12 for s in range(60)]

IS_AM = [idx < 3 for idx in TIME_INDEX]   # 0–2
IS_PM = [idx >= 3 for idx in TIME_INDEX]  # 3–11

#==================================================

def get_num_patients() -> int:
    """
    Returns the number of patients based on the loaded patient data.
    
    Returns:
        int: The total number of patients.
    """
    return len(patients)

def load_patient_preferences() -> list:
    """
    Loads patient preferred slots from the patient data.
    
    Attempts to load from UI module, falls back to CSV if unavailable.
    Handles missing or invalid values by setting to None.
    
    Returns:
        list: List of preferred slots, padded with None if necessary.
    """
    
    prefs = []
    if "preferred_slot" in patients.columns:
        for i in range(min(len(patients), get_num_patients())):
            val = patients.iloc[i]["preferred_slot"]
            if pd.isna(val):
                prefs.append(None)
            else:
                try:
                    prefs.append(int(val))
                except Exception:
                    prefs.append(None)
    # pad with None if fewer rows than NUM_PATIENTS
    while len(prefs) < get_num_patients():
        prefs.append(None)
    return prefs

def random_geno() -> genotype:
    """
    Generates a random genotype (list of slot assignments) for all patients.
    
    Returns:
        genotype: A list of random slot indices for each patient.
    """
    return [np.random.randint(0,TOTAL_SLOTS-1) for _ in range(get_num_patients())]

def new_population(size = 100) -> population:
    """
    Creates a new population of random genotypes.
    
    Args:
        size (int): Number of genotypes in the population. Default is 100.
    
    Returns:
        population: A list of genotypes.
    """
    return [random_geno() for _ in range(size)]

fitness_values = {} # dict for fitness scores to avoid redundant calculations

def fitness(geno) -> int:
    """
    Calculates the fitness of a genotype based on hard and soft constraints.
    
    Fitness is negative penalty: lower penalty (higher fitness) is better.
    Uses memoization to cache results.
    
    Args:
        geno (genotype): The genotype to evaluate.
    
    Returns:
        int: The fitness score (negative penalty).
    """
    key = tuple(geno)

    if key in fitness_values:
        return fitness_values[key]

    SOFT_W = 10
    HARD_W = 100

    penalty, soft_violations, hard_violations = 0, 0, 0

    # soft constraint: patient preferences (day and time)
    for i, slot in enumerate(geno):
            
        pref_slot = PREF_SLOT[i]
        pref_time = PREF_TIME[i]
        time_idx = slot % (sheet.max_row-1) # 0-2 = AM

        if pref_time == "am" and not IS_AM[time_idx]:
            soft_violations += 1
        elif pref_time == "pm" and not IS_PM[time_idx]:
            soft_violations += 1

        if pd.notna(pref_slot) and isinstance(pref_slot, (int, float)):
            if slot != int(pref_slot):
                soft_violations += 1

    # hard constraint: no double booking
    used_slot = set(geno)
    hard_violations = len(geno) - len(used_slot)

    penalty = SOFT_W * soft_violations + HARD_W * hard_violations
    fitness_values[key] = -(penalty) # store in dict

    return -(penalty)

# three operator functions of GA (selection, crossover, mutation)

# larger k = more competetitive, takes less time to converge
def selection(population, fitnesses, k) -> genotype: 
    """
    Selects the best genotype from k random candidates using tournament selection.
    
    Args:
        population (population): List of genotypes.
        fitnesses (list): Corresponding fitness scores.
        k (int): Tournament size.
    
    Returns:
        genotype: The selected genotype.
    """
    index = np.random.choice(len(population), k)
    best_candidates = max(index, key=lambda i: fitnesses[i])
    return population[best_candidates].copy()

def crossover(a,b) -> Tuple[genotype, genotype]:
    """
    Performs two-point crossover between two genotypes.
    
    Args:
        a (genotype): First parent.
        b (genotype): Second parent.
    
    Returns:
        Tuple[genotype, genotype]: Two offspring genotypes.
    """
    a = np.array(a)
    b = np.array(b)

    point1 = np.random.randint(1, len(a)-1)
    point2 = np.random.randint(point1, len(a)-1)

    cross = np.zeros(len(a), dtype=bool)
    cross[point1:point2] = True

    new_a = np.where(cross, a, b)
    new_b = np.where(cross, b, a)

    return new_a.tolist().copy(), new_b.tolist().copy()

def mutation(geno) -> genotype:
    """
    Mutates a genotype by swapping two random genes.
    
    Args:
        geno (genotype): The genotype to mutate.
    
    Returns:
        genotype: The mutated genotype.
    """
    geno_mutate = np.array(geno)
    point1, point2 = np.random.randint(0, len(geno_mutate), size=2)
    # swap two genes
    geno_mutate[point1], geno_mutate[point2] = geno_mutate[point2], geno_mutate[point1]
    return geno_mutate.tolist().copy()

def plot_results(best_fitness, avg_fitness, best_geno, best_generation):
    """
    Plots the fitness scores over generations and prints summary.
    
    Args:
        best_fitness (list): Best fitness per generation.
        avg_fitness (list): Average fitness per generation.
        best_geno (genotype): Best genotype found.
        best_generation (int): Generation where best was found.
    """
    plt.figure(figsize=(7,5))
    plt.plot(best_fitness, label='Best Fitness', marker='*', color='green')
    plt.plot(avg_fitness, label='Average Fitness', marker='o', color='red')

    # circle best overall value
    if best_fitness:
        plt.scatter(best_generation, [max(best_fitness)], s=100, facecolors='none', edgecolors='black', label=f'Best Fitness = {max(best_fitness)}')

    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    plt.ylim(min(avg_fitness + best_fitness) - 10, 0)
    plt.title("Fitness Scores over Generations")
    plt.legend()
    plt.show()

    # summary
    if best_fitness:
        print("Best Overall Fitness:", max(best_fitness))
        print("Best Generation:", best_generation)
        print("Best Genotype:", best_geno)

def genetic_algo(t_size, cross_prob, mut_prob, generations=100):
    """
    Runs the genetic algorithm to optimize patient scheduling.
    
    Args:
        t_size (int): Tournament size for selection.
        cross_prob (float): Crossover probability.
        mut_prob (float): Mutation probability.
        generations (int): Maximum number of generations. Default 100.
    
    Returns:
        dict: Results including best score, genotype, generation, and fitness lists.
    """
    
    initial_pop = new_population()
    
    # track the best individual/score seen across all generations
    best_generation = -1
    best_score = float('-inf') # fitness is maximized
    best_geno = None # store corresponding genotype
    no_improvement = 0 # early stopping if no improvement for 5 generations
    stopping_counter = 40

    best_fitness = []
    avg_fitness = []

    for gen in range(generations):
        # main loop - includes selection, and population update
        new_pop = []
        fit_scores = []

        prev_best_score = best_score # store previous best score for improvement check

        # calculating fitness of each genotype in population
        for geno in initial_pop:
            score = fitness(geno)
            fit_scores.append(score)
            # update overall best if this individual is superior
            if score >= best_score:
                best_score = score
                best_geno = geno.copy()
                best_generation = gen
            
        # check for improvement and update no_improvement counter
        if best_score > prev_best_score:
            no_improvement = 0
        else:
            no_improvement += 1

        # storing fitness stats for plotting (this is for 1st/initial generation)
        best_fitness.append(max (fit_scores))
        avg_fitness.append(np.average(fit_scores))

        # creating new population via selection, crossover and mutation
        while len(new_pop) < len(initial_pop):
            # selection
            parent_1, parent_2 = selection(initial_pop, fit_scores, t_size), selection(initial_pop, fit_scores, t_size)
            # crossover
            if np.random.random() < cross_prob:
                child_1, child_2 = crossover(parent_1, parent_2)
            else:
                child_1, child_2 = parent_1.copy(), parent_2.copy()
            # mutation
            if np.random.random() < mut_prob:
                child_1 = mutation(child_1)
            if np.random.random() < mut_prob:
                child_2 = mutation(child_2)

            new_pop.extend([child_1, child_2]) # extend adds both as separate elements

        # early stopping check
        if no_improvement >= stopping_counter:
            print(f"No improvement for {stopping_counter} generations. Stopping early at generation {gen+1}.")
            break

        new_pop = new_pop[:len(initial_pop)] # trim to original population size
        initial_pop = new_pop

    return {"best_score": best_score,
            "best_geno": best_geno,
            "best_generation": best_generation,
            "best_fitness": best_fitness,
            "avg_fitness": avg_fitness
    }

if __name__ == "__main__":
    ga_run = genetic_algo(2,0.9,0.1)
    plot_results(ga_run["best_fitness"], ga_run["avg_fitness"], ga_run["best_geno"], ga_run["best_generation"]) 