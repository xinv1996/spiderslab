import pandas as pd

df = pd.DataFrame(data=[{"year": 2000, "month": 1, "day": 1, "n_birth": 800},
                        {"year": 2000, "month": 1, "day": 2, "n_birth": 200},
                        {"year": 2001, "month": 1, "day": 1, "n_birth": 1200},
                        {"year": 2001, "month": 1, "day": 2, "n_birth": 800},
                        {"year": 2001, "month": 2, "day": 1, "n_birth": 1000},
                        ]
                  )

year_df = df.groupby(by='year')['n_birth'].sum()
month_df = df.groupby(by=['month', 'year'])['n_birth'].sum()

res_df = month_df/year_df
print(res_df)

