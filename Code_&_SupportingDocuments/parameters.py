import GA_firstPT as ga

def run_experiment(t_size, cross_prob, mut_prob):
    print("\n=== Running experiment ===")
    print(f"t_size={t_size}, cross_prob={cross_prob}, mut_prob={mut_prob}")

    result = ga.genetic_algo(t_size=t_size,cross_prob=cross_prob,mut_prob=mut_prob)

    print("--------------------------")

    return result


if __name__ == "__main__":
    # Try different tournament sizes
    for t in [2, 5, 10]:
        for c in [0.1, 0.2, 0.5, 0.8]:
            for m in [0.1, 0.2, 0.5, 0.8]:
                run_experiment(t, c, m)