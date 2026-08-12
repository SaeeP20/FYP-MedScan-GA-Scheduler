from typing import override
import GA_firstPT as ga
import pandas as pd
import unittest

class TestGA(unittest.TestCase):

# First GA prototype tests

    def test_random_geno_length(self):
        """ testing if random_geno generates genotype of correct length """
        result = ga.random_geno()
        self.assertEqual(len(result), ga.get_num_patients())

    def test_new_population_size(self):
        """ testing if new_population generates population of correct size """
        result = ga.new_population()
        self.assertEqual(len(result), 20)

    def test_fitness_no_violations(self):
        """ testing if fitness function returns 0 for genotype with no violations """
        geno = list(range(25))  # no duplicate slots
        result = ga.fitness(geno)
        self.assertEqual(result, 0)

    def test_soft_violations(self):
         # creating a mock patient DataFrame with preferred_time column
        ga.patients = pd.DataFrame({"preferred_time": ["am"]})
        geno = [15]  # PM slot → violation
        result = ga.fitness(geno)
        self.assertEqual(result, -1)
       

    def test_hard_violations(self):
        ga.patients = pd.DataFrame({"preferred_time": [None, None]})
        geno = [1, 1]  # duplicate → hard violation
        result = ga.fitness(geno)
        self.assertEqual(result, -100)

    def test_mixed_violations(self):
        ga.patients = pd.DataFrame({"preferred_time": ["am", "pm"]})
        geno = [3, 3]  # PM slot for patient 1 → soft violation, duplicate → hard violation
        result = ga.fitness(geno)
        self.assertEqual(result, -101)
    
    def test_selection_returns_genotype(self):
        """ testing if selection function returns a genotype from the population """
        pop = ga.new_population()
        fit_scores = [ga.fitness(geno) for geno in pop]
        result = ga.selection(pop, fit_scores ,10)
        self.assertIn(result, pop)
    
    def test_crossover_length(self):
        """ testing if crossover function returns genotype of correct length """
        parent1 = ga.random_geno()
        parent2 = ga.random_geno()
        child1, child2 = ga.crossover(parent1, parent2)
        self.assertEqual(len(child1), ga.get_num_patients())
        self.assertEqual(len(child2), ga.get_num_patients())

    def test_mutation_changes_genotype(self):
        """ testing if mutation function changes at least one gene in the genotype """
        geno = ga.random_geno()
        mutated_geno = ga.mutation(geno.copy())
        self.assertNotEqual(geno, mutated_geno)

    def test_mutation_length(self):
        """ testing if mutation function returns genotype of correct length """ 
        geno = ga.random_geno()
        mutated_geno = ga.mutation(geno.copy())
        self.assertEqual(len(mutated_geno), ga.get_num_patients())

    def test_load_patient_preferences(self):
        """ testing if load_patient_preferences returns list of correct length and types """
        result = ga.load_patient_preferences()
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), ga.get_num_patients())
        for pref in result:
            self.assertTrue(pref is None or (isinstance(pref, int) and 0 <= pref < ga.TOTAL_SLOTS))
        print(result)

    def param_test_unchanged(self):
        unchanged = ga.genetic_algo(10, 0.5, 0.5)

        print("Best score:", unchanged["best_score"])
        print("Best genotype:", unchanged["best_geno"])

        self.assertIn("best_score:", unchanged)
        self.assertIn("best_geno:", unchanged)

