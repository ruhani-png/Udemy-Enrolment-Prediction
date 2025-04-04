import nbformat
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Define the cleaning function for 'course-num-of-reviews'
def clean_num_of_reviews(value):
    # Remove "review" or "reviews" and strip any extra spaces
    cleaned_value = str(value).replace("reviews", "").replace("review", "").strip()
    try:
        # Convert to integer
        return int(cleaned_value)
    except ValueError:
        return None  # Return None if conversion fails


# Define the cleaning function for 'course-price'
def clean_course_price(value):
    # Remove "Current price:" and "£", then strip any extra spaces
    cleaned_value = str(value).replace("Current price:", "").replace("£", "").strip()
    try:
        # Convert to float
        return float(cleaned_value)
    except ValueError:
        return None  # Return None if conversion fails

# Function to extract and clean the numeric value from course-enrolled-student
def extract_number(value):
    # Check if the value is not NaN or an error message like "N/A" or "Error"
    if str(value).strip().upper() in ['N/A', 'ERROR']:
        return None

    # Use regex to find numbers
    match = re.search(r'[\d.,]+', value)
    if match:
        # Remove commas and periods, assuming they are thousands separators
        number_str = match.group().replace(',', '').replace('.', '')
        try:
            return int(number_str)  # Convert to integer
        except ValueError:
            return None  # If conversion fails, return None
    return None

# Utility function
def transform_columns(df, columns, cap_percentile=0.99):
    """
    Create new columns for only capped, only logged, and capped-then-logged transformations.

    Parameters:
    - df: pandas DataFrame containing the data.
    - columns: list of column names to transform.
    - cap_percentile: percentile for capping outliers (default is 0.99).

    Returns:
    - Updated DataFrame with new columns for transformations.
    """
    for col in columns:
        # Step 1: Cap extreme values at the specified percentile
        upper_bound = df[col].quantile(cap_percentile)
        capped_col = f"{col}_only_capped"
        df[capped_col] = np.where(df[col] > upper_bound, upper_bound, df[col])

        # Step 2: Apply log transformation to the original column
        logged_col = f"{col}_only_logged"
        df[logged_col] = np.log1p(df[col])  # Use log1p to handle zero values if they exist

        # Step 3: Cap and then log transform
        capped_and_logged_col = f"{col}_capped_and_logged"
        df[capped_and_logged_col] = np.log1p(df[capped_col])

    return df

import matplotlib.pyplot as plt


def compare_methods_boxplots_separate(df, variable_groups, title="Comparison of Methods (Separate Graphs)"):
    """
    Create separate box plots for each transformation type in a single figure.

    Parameters:
    - df: DataFrame containing the data
    - variable_groups: list of lists, where each sublist contains three or four variables:
        [original_col, log_col, capped_col, log_capped_col (optional)]
    - title: str, title of the entire plot
    """
    # Determine the number of columns (3 or 4 depending on presence of log_capped_col)
    columns = 4 if any(len(group) == 4 for group in variable_groups) else 3
    rows = len(variable_groups)

    # Create a figure with subplots
    fig, axes = plt.subplots(rows, columns, figsize=(5 * columns, 5 * rows))
    fig.suptitle(title, fontsize=16)

    # Ensure axes is iterable when there's only one row
    if rows == 1:
        axes = [axes]

    for i, group in enumerate(variable_groups):
        # Unpack the variables
        original_col, log_col, capped_col = group[:3]
        log_capped_col = group[3] if len(group) == 4 else None

        # Plot Original
        axes[i][0].boxplot(df[original_col], vert=True, patch_artist=True)
        axes[i][0].set_title(f"Original: {original_col}", fontsize=12)
        axes[i][0].set_ylabel(original_col)

        # Plot Log Transformed
        axes[i][1].boxplot(df[log_col], vert=True, patch_artist=True)
        axes[i][1].set_title(f"Log Transformed: {original_col}", fontsize=12)
        axes[i][1].set_yscale("log")
        axes[i][1].set_ylabel(f"Log of {original_col}")

        # Plot Capped
        axes[i][2].boxplot(df[capped_col], vert=True, patch_artist=True)
        axes[i][2].set_title(f"Capped: {original_col}", fontsize=12)
        axes[i][2].set_ylabel(f"Capped {original_col}")

        # Plot Log Capped (if present)
        if log_capped_col:
            axes[i][3].boxplot(df[log_capped_col], vert=True, patch_artist=True)
            axes[i][3].set_title(f"Log Capped: {original_col}", fontsize=12)
            axes[i][3].set_yscale("log")
            axes[i][3].set_ylabel(f"Log Capped {original_col}")

    # Adjust layout for readability
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()



def save_fig(fig, fig_id, tight_layout=True, fig_extension="png", resolution=300):
    """
    Save a figure to a specific directory.
    
    Parameters:
    fig: The figure to be saved.
    fig_id: The filename to save the figure as.
    tight_layout: If True, apply tight_layout to prevent overlapping.
    fig_extension: File extension for the saved figure (e.g., 'png', 'jpg').
    resolution: The dpi (dots per inch) of the saved image.
    """
    
    # Create the full path to save the figure
    import os
    save_path = os.path.join(IMAGES_PATH, f"{fig_id}.{fig_extension}")
    
    # Apply tight layout if needed
    if tight_layout:
        fig.tight_layout()

    # Save the figure
    fig.savefig(save_path, format=fig_extension, dpi=resolution)
