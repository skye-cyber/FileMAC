import warnings

warnings.simplefilter("ignore", RuntimeWarning)
with warnings.catch_warnings():
    warnings.filterwarnings(
        "ignore", message="Your system is avx2 capable but pygame was not built with support for it.", category=RuntimeWarning)
