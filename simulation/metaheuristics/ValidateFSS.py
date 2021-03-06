# from src.optimization.metaheuristics.single_objective.FSS import FSS
# from src.optimization.metaheuristics.single_objective.FSS_ST import FSS_ST
from src.optimization.metaheuristics.single_objective.FSS import FSS
from src.optimization.problems.ObjectiveFunction import *
from src.optimization.problems.SearchSpaceInitializer import UniformSSInitializer, OneQuarterDimWiseSSInitializer
from src.simulation.metaheuristics.Utils import create_dir
import numpy as np
import os

def main():
    search_space_initializer = OneQuarterDimWiseSSInitializer()
    file_path = "/home/clodomir/Desktop/Executions1/"
    num_exec = 30
    school_size = 30
    num_iterations = 5000
    step_individual_init = 0.1
    step_individual_final = 0.001
    step_volitive_init = 0.001
    step_volitive_final = 0.0001
    min_w = 1
    w_scale = num_iterations / 2.0

    # Notice that for CEC Functions only the following dimensions are available:
    # 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100
    dim = 30

    regular_functions = [SphereFunction, RosenbrockFunction, RastriginFunction, SchwefelFunction, SchafferFunction,
                         GriewankFunction, AckleyFunction, CigarFunction, HimmelblauFunction]

    cec_functions = [CompositionFunction6, CompositionFunction7, CompositionFunction8]

    for benchmark_func in cec_functions:
        func = benchmark_func(dim)
        run_experiments(num_iterations, school_size, num_exec, func, search_space_initializer, step_individual_init,
                        step_individual_final, step_volitive_init, step_volitive_final, min_w, w_scale, file_path)


def run_experiments(n_iter, school_size, num_runs, objective_function, search_space_initializer, step_individual_init,
                    step_individual_final, step_volitive_init, step_volitive_final, min_w, w_scale, save_dir):
    alg_name = "FSS"
    console_out = "Algorithm: {} Function: {} Execution: {} Best Cost: {}"
    if save_dir:
        create_dir(save_dir)
        f_handle_cost_iter = file(save_dir + "/FSS_" + objective_function.name + "_cost_iter.txt", 'w+')
        f_handle_cost_eval = file(save_dir + "/FSS_" + objective_function.name + "_cost_eval.txt", 'w+')

    for run in range(num_runs):
        # opt1 = FSS_ST
        opt1 = FSS(objective_function=objective_function, search_space_initializer=search_space_initializer,
                   n_iter=n_iter, school_size=school_size, step_individual_init=step_individual_init,
                   step_individual_final=step_individual_final, step_volitive_init=step_volitive_init,
                   step_volitive_final=step_volitive_final, min_w=min_w, w_scale=w_scale)

        opt1.optimize()
        print console_out.format(alg_name, objective_function.name, run+1, opt1.best_fish.cost)

        temp_optimum_cost_tracking_iter = np.asmatrix(opt1.optimum_cost_tracking_iter)
        temp_optimum_cost_tracking_eval = np.asmatrix(opt1.optimum_cost_tracking_eval)

        if save_dir:
            np.savetxt(f_handle_cost_iter, temp_optimum_cost_tracking_iter, fmt='%.4e')
            np.savetxt(f_handle_cost_eval, temp_optimum_cost_tracking_eval, fmt='%.4e')

    if save_dir:
        f_handle_cost_iter.close()
        f_handle_cost_eval.close()


if __name__ == '__main__':
    main()
