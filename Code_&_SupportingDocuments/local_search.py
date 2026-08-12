import GA_firstPT as ga
import matplotlib.pyplot as plt

def local_search(initial_solution, max_iterations=500):
    """
    Performs hill-climbing local search on an initial solution.
    
    Uses mutation to generate neighbors and accepts improvements.
    Tracks fitness history over iterations.
    
    Args:
        initial_solution (list): Starting genotype.
        max_iterations (int): Maximum number of iterations. Default 500.
    
    Returns:
        tuple: (best_solution, best_fitness, initial_fitness, fitness_history)
    """
    current = initial_solution
    current_fitness = ga.fitness(current)
    first = current_fitness
    history = [current_fitness]

    for _ in range(max_iterations):
        # Generate a neighbour by swapping two positions
        new = ga.mutation(current.copy())
        new_fitness = ga.fitness(new)

        # Accept if better
        if new_fitness > current_fitness:
            current = new
            current_fitness = new_fitness

        history.append(current_fitness)

    return current, current_fitness, first, history

def run_local_search():
    """
    Runs local search starting from a random genotype.
    
    Prints the best fitness found and returns the solution and history.
    
    Returns:
        tuple: (best_solution, fitness_history)
    """
    # Start from a random schedule
    initial = ga.random_geno()
    best_solution, best_fitness, first_solution, history = local_search(initial)

    print("Local Search Best Fitness:", best_fitness)
    return best_solution, history

def plot_results(local, ga):
    """
    Plots fitness scores for GA and local search over generations.
    
    Args:
        local (tuple): Local search results (solution, best_fitness, initial_fitness, history).
        ga (dict): GA results with fitness lists and best generation.
    """

    # Parts that are commented show GA results as well, but focus is on local search for clarity.

    plt.figure(figsize=(8,5))
    # plt.plot(ga["best_fitness"], label='Best GA Fitness', marker='*', color='green')
    # plt.plot(ga["avg_fitness"], label='Average Fitness', marker='o', color='red')
    plt.plot(local[3], label=f'Best LS Fitness = {local[1]}', marker='*', color='blue')

    # circle best overall value
    # plt.scatter([ga["best_generation"]], [max(ga["best_fitness"])], s=100, facecolors='none', edgecolors='black', label=f'Best GA Fitness = {max(ga["best_fitness"])}')

    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    # plt.xlim(0, 105)
    plt.ylim(min(ga["avg_fitness"] + ga["best_fitness"] + [local[1], local[2]]) - 10, 0)
    plt.title("Solution Quality of local search vs GA")
    plt.legend()
    plt.show()

ga_result = ga.genetic_algo(t_size=2, cross_prob=0.9, mut_prob=0.12)
ga_best = max(ga_result["best_fitness"])

# Local search run
ls = local_search(ga.random_geno())

print("First fitness:", ls[2])
print("GA best fitness:", ga_best)
print("Local Search best fitness:", ls[1])
plot_results(ls, ga_result)