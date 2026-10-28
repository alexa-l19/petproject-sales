import pandas as pd

df = pd.read_csv("orders.csv", parse_dates=["order_date"])

print(df.info())                      # типы колонок, пропуски
print(df.isna().sum())                # пропуски по колонкам
print("дубликатов:", df.duplicated().sum())

df = df.drop_duplicates()
df["region"] = df["region"].fillna("Не указан")

print(df[["quantity", "discount", "revenue", "profit"]].describe())

revenue, profit = df.revenue.sum(), df.profit.sum()
print("Выручка:", round(revenue), "Прибыль:", round(profit), "Маржа, %:", round(profit / revenue * 100, 1))

by_cat = df.groupby("category")[["revenue", "profit"]].sum()
by_cat["margin_%"] = (by_cat.profit / by_cat.revenue * 100).round(1)
print(by_cat)

by_disc = df.groupby("discount")[["revenue", "profit"]].sum()
by_disc["margin_%"] = (by_disc.profit / by_disc.revenue * 100).round(1)
print(by_disc)
pivot = df.pivot_table(index="category", columns="discount",
                       values=["revenue", "profit"], aggfunc="sum")
margin = (pivot["profit"] / pivot["revenue"] * 100).round(1)
print(margin)
print(df.groupby("discount")["quantity"].mean().round(2))
df.to_csv("orders_clean.csv", index=False)