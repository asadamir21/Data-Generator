import pandas as pd
import random

def GenerateData(df, Count):
    for i in range(Count):
        Row = []
        for col in df.columns:
            if df[col].dtype == 'int64' or df[col].dtype == 'float64':
                choice = random.randint(1, 4)

                if choice == 1:
                    Row.append(int(df[col].mean()))
                elif choice == 2:
                    Row.append(int(df[col].median()))
                elif choice == 3:
                    Row.append(int(df[col].mode()[0]))
                else:
                    Row.append(random.randint(df[col].min(), df[col].max()))

            elif df[col].dtype == 'object' or df[col].dtype == 'datetime64[ns]':
                Row.append(df[col][random.randint(1,len(df)-1)])

        # Inserting on Last Row
        df.loc[len(df)] = Row
    return df

