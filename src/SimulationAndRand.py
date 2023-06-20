import random
import math
import sympy as smp
import numpy as np
from scipy import stats


def random_mixed_congruential_generator(a, c, m, x_zero, upper_bound):
    """Calculates all the numbers generated by a mixed congruential random number
    generators.
    param: a is a constant
    param: c is a constant
    param: m is the modulo
    param: x_zero is the seed
    param: is an upper bound for the cycle
    returns a list of all numbers generated"""
    numbers_generated = []
    it = 0
    current_x = x_zero
    while it <= upper_bound:
        next_x = (a * current_x + c) % m
        numbers_generated.append(next_x)
        if next_x == x_zero:
            break
        current_x = next_x
        it += 1
    return numbers_generated


def uniform_random_from_mixed_congruential_generator(a, c, m, x_zero, upper_bound):
    """Calculates all the numbers generated by a mixed congruential random number
    generators and divides them by the modulo to get a uniform distribution.
    param: a is a constant
    param: c is a constant
    param: m is the modulo
    param: x_zero is the seed
    param: is an upper bound for the cycle
    returns a list of all numbers generated"""
    numbers_generated = []
    it = 0
    current_x = x_zero
    while it <= upper_bound:
        next_x = (a * current_x + c) % m
        numbers_generated.append((next_x + (1 / 2)) / m)
        if next_x == x_zero:
            break
        current_x = next_x
        it += 1
    return numbers_generated


"""
    Example:
    a = 10
    b = 20
    m = 1.0/50.0 * (20.0 - 10.0)
    function = "1.0/50.0 * (x - 10.0)"
    print(generate_acceptance_rejection(m, a, b, function, 100))
"""


def generate_acceptance_rejection(m, a, b, function, upper_limit):
    """Calculates a random observation from a function that has a range [a,b]
    using the acceptance
    rejection method
    param: m is the highest image of the funcion
    param: a is a constant
    param: b is a constant
    param: function is the desired function written as a string
    param: upper_limit the amount of times the simulation is run
    returns the random image generated"""
    for i in range(0, upper_limit):
        first_random = random.uniform(0, 1)
        second_random = random.uniform(0, 1)
        x = a + (b - a) * first_random
        evaluation_image = eval(function)
        if second_random <= evaluation_image / m:
            print("The evaluation image was found correctly")
            break
    print("First random " + str(first_random))
    print("Second random " + str(second_random))
    return evaluation_image


def integrate_and_find_inverse(function):
    """Computes integral and inverse of a given function

    Parameters:
    function (sympy expression): function expression
    n_variables_to_generate (int): number of random variables to generate

    Returns:
    integrated, inverse
    """
    x = smp.symbols("x", real=True)
    print("Function f(x): ")
    smp.pprint(function)
    integrated = smp.integrate(function, x)
    print("Integral F(x)")
    smp.pprint(integrated)
    r = smp.symbols("r", real=True)
    eq = smp.Eq(integrated, r)

    try:
        inverse = smp.solve(eq, x)
        inverse = smp.sympify(inverse)
        print("Inverse")
        smp.pprint(inverse)
        return [integrated, inverse]
    except smp.PolynomialError:
        print("Error: The inverse of the function cannot be calculated.")
        return


def generate_acceptance_rejection_with_symp(a, b, function, upper_limit):
    """
    Generates a random observation from a function within the range [a,b]
    using the acceptance-rejection method.

    Args:
        a (float): Lower bound of the range.
        b (float): Upper bound of the range.
        function (str): The desired function written as a string.
        upper_limit (int): The maximum number of iterations to run the simulation.

    Returns:
        float: The random number generated or None if no suitable number was found within upper_limit iterations.
    """
    x = smp.symbols("x", real=True)
    f = smp.sympify(function)

    # Compute maximum of function
    x_values = np.linspace(a, b, 10000)
    m = max([f.subs(x, val).evalf() for val in x_values])
    print(f"\nM is = {m}")

    for i in range(upper_limit):
        first_random = random.uniform(a, b)
        second_random = random.uniform(0, 1)
        x_value = a + (b - a) * first_random
        evaluation_image = f.subs(x, x_value).evalf()

        if second_random <= evaluation_image / m:
            print("The evaluation image was found correctly")
            print("First random: ", first_random)
            print("Second random: ", second_random)
            return evaluation_image

    print("No suitable random number found within upper_limit iterations.")
    return None


def inverse_transform_sampling(
    n_samples, dist_name="norm", lower_bound=None, upper_bound=None, *args, **kwargs
):
    """
    Function to generate random observations based on the inverse transform method

    Parameters:
    - n_samples: int, number of random variables to generate
    - dist_name: str, name of the distribution to sample from (default is 'norm')
    - lower_bound: float, minimum value for generated numbers (default is None)
    - upper_bound: float, maximum value for generated numbers (default is None)
    - *args, **kwargs: distribution-specific parameters

    Returns:
    - rvs: array of generated random variables
    """
    # Define the distribution
    dist = getattr(stats, dist_name)
    rvs = []
    while len(rvs) < n_samples:
        # Generate a uniform random variable
        U = np.random.uniform(0, 1)
        # Transform the uniform random variable
        rv = dist.ppf(U, *args, **kwargs)
        # Check if the generated number is in the desired range
        if (lower_bound is not None and rv < lower_bound) or (
            upper_bound is not None and rv > upper_bound
        ):
            continue
        print(f"radom number used = {U}, used to generated random sampling = {rv}")
        rvs.append(rv)
    return np.array(rvs)


def user_inverse_transform_sampling_from_inverse(
    n_samples, inverse, lower_bound=None, upper_bound=None
):
    """
    Function to generate random observations based on the inverse transform method with user-defined inverse function.

    Parameters:
    - n_samples: int, number of random variables to generate
    - inverse: sympy expression, inverse of the cumulative distribution function
    - lower_bound: float, minimum value for generated numbers (default is None)
    - upper_bound: float, maximum value for generated numbers (default is None)

    Returns:
    - rvs: array of generated random variables
    """

    # Convert sympy expression into a callable function
    r = smp.symbols("r")
    inverse_func = smp.lambdify(r, inverse, "numpy")

    rvs = []
    while len(rvs) < n_samples:
        # Generate a uniform random variable
        U = random.uniform(0, 1)

        # Transform the uniform random variable
        rv = inverse_func(U)

        # Check if the generated number is in the desired range
        if (lower_bound is not None and rv < lower_bound) or (
            upper_bound is not None and rv > upper_bound
        ):
            continue
        print(f"radom number used = {U}, used to generated random sampling = {rv}")
        rvs.append(rv)

    return np.array(rvs)
