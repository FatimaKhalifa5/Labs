import numpy as np
import pandas as pd

def skew_calc(df):
    """
    Diagnoses skewness for every numeric column in a DataFrame and recommends a transformation based on the column's skewness and
    minimum value. Binary, encoded, and ID columns are excluded, since skewness isn't a meaningful for them.
    It returns a DataFrame with the following columns:
    Feature, Skewness, Degree, Direction, Recommended Transformation
    """
    # Your code here 

    results = []

    # Select numeric columns only
    numeric_columns = df.select_dtypes(include=np.number).columns

    # Skip binary indicators (0/1) or columns ending with '_id'
    if 'id' in str(col).lower() or df[col].nunique() <= 2:
        continue

    for column in numeric_columns:

        # Skip binary columns
        if df[column].nunique() <= 2:
            continue

        skewness = df[column].skew()
        minimum = df[column].min()



        # Classify degree and direction
        if skewness < -1:
            degree = 'Highly Skewed'
            direction = 'Left'

        elif -1 <= skewness < -0.5:
            degree = 'Moderately Skewed'
            direction = 'Left'

        elif -0.5 <= skewness <= 0.5:
            degree = 'Normal'
            direction = 'Symmetrical'

        elif 0.5 < skewness <= 1:
            degree = 'Moderately Skewed'
            direction = 'Right'

        else:
            degree = 'Highly Skewed'
            direction = 'Right'

        # Recommend transformation
        if -0.5 <= skewness <= 0.5:
            transformation = 'None'

        elif minimum < 0:
            transformation = 'Yeo-Johnson'

        elif minimum == 0 and skewness > 1:
            transformation = 'Log Plus One'

        elif minimum > 0:
            transformation = 'Box-Cox'

        else:
            transformation = 'Yeo-Johnson'

        results.append({
            'Feature': column,
            'Skewness': skewness,
            'Degree': degree,
            'Direction': direction,
            'Recommended Transformation': transformation
        })

    return pd.DataFrame(results)
