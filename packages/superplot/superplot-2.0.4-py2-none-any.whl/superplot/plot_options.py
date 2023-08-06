"""
This module provides a named tuple plot_options to represent the options as
selected in the UI. Also loads default values from config.yml and makes them available.

TODO: This module should also do a reasonable amount of validation
      of config variables.
"""
import os
import appdirs
from collections import namedtuple
import simpleyaml as yaml
import numpy as np


plot_options = namedtuple("plot_options", (
    # Data
    "xindex",  # Index of x axis data
    "yindex",  # Index of y axis data
    "zindex",  # Index of z axis data
    "logx",  # Apply log scale to xdata
    "logy",  # Apply log scale to ydata
    "logz",  # Apply log scale to zdata

    # Limits, bins, ticks
    "plot_limits",  # Plot limits [xmin, xmax, ymin, ymax]
    "bin_limits",  # Bin limits [[xmin, xmax], [ymin, ymax]]
    "nbins",  # Number of bins
    "xticks",  # Number of x ticks
    "yticks",  # Number of y ticks

    "alpha",  # Values of alpha in asc. order [float, float]
    "tau",  # Theoretical error width on delta chi-squared plots.

    # Labels
    "xlabel",  # Label for x axis
    "ylabel",  # Label for y axis
    "zlabel",  # Label for z axis
    "plot_title",  # Title of plot
    "title_position", # Location of plot title
    "leg_title",    # Plot legend
    "leg_position",  # Location of plot legend

    # Whether to show optional plot elements (all True / False)
    "show_best_fit",
    "show_posterior_mean",
    "show_posterior_median",
    "show_posterior_mode",
    "show_conf_intervals",
    "show_credible_regions",
    "show_posterior_pdf",
    "show_prof_like",
    
    # Whether to use KDE for PDF, and if so, band-width method
    "kde_pdf",
    "bw_method"
))


def get_config(yaml_file="config.yml"):
    """
    Load the config file, either from the user data
    directory, or if that is not available, the installed
    copy.
    
    :param yaml_file: Name of yaml file
    :type yaml_file: str
    
    :returns: config
    :rtype: dict
    """

    # First check whether the user has a custom home directory.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    home_dir_locfile = os.path.join(script_dir, "user_home.txt")

    config_path = None

    if os.path.exists(home_dir_locfile):
        with open(home_dir_locfile, "rb") as f:
            home_dir_path = f.read()
            config_path = os.path.join(home_dir_path, yaml_file)

    # If it doesn't exist, use the installed copy
    if config_path is None or not os.path.exists(config_path):
        config_path = os.path.join(
            os.path.split(os.path.abspath(__file__))[0],
            yaml_file
        )
    # Load & return config
    with open(config_path) as cfile:
        return yaml.load(cfile)


CONFIG = get_config()


def default(option):
    """
    Retrieve the default value of a plot option.

    If no default is available, prints an error message and raises
    a KeyError.

    :param option: Name of the option
    :type option: string

    :returns: Default value of specified option.
    """
    _defaults = CONFIG["plot_options"]

    # Fix the types of a few options. It would also be
    # possible to directly specify the types in the YAML file,
    # but that might confuse users / be messy.
    if _defaults["alpha"] is not None:
        _defaults["alpha"] = np.array(_defaults["alpha"])
        _defaults["alpha"].sort()
    if _defaults["plot_limits"] is not None:
        _defaults["plot_limits"] = np.array(_defaults["plot_limits"])
    
    try:
        return _defaults[option]
    except KeyError:
        print "plot_options: No default specified for option: {}".format(option)
        raise
