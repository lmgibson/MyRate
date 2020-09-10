# Cleaning Strings
import re
from datetime import datetime

# Utilities
import os

# Packages for Data Management
import pandas as pd
import numpy as np

# Importing Data and cleaning
static = pd.read_csv("./data/raw/freelancers.csv")
dynamic = pd.read_csv("./data/raw/freelancers_detail.csv")

static.drop([static.columns[0], 'user_description', 'earnings',
             'city', 'rating'], axis=1, inplace=True)
dynamic.drop([dynamic.columns[0], 'employers', 'invoices_paid',
              'largest_employ'], axis=1, inplace=True)
