import numpy as np
import pandas as pd

rng = np.random.default_rng(42)   # seed: у всех будут одинаковые числа
N = 10_000

cats = {"Электроника": (900, 0.15), "Мебель": (600, 0.04), "Канцелярия": (40, 0.12)}
regions = ["Минск", "Брест", "Гродно", "Гомель", "Могилёв", "Витебск"]
segments = ["Розница", "Корпоративные", "Малый бизнес"]

# даты за 2 года, в ноябре-декабре продаж вдвое больше
days = pd.date_range("2023-01-01", "2024-12-31")
w = np.where(days.month.isin([11, 12]), 2.0, 1.0)
order_date = rng.choice(days, size=N, p=w / w.sum())

category = rng.choice(list(cats), size=N, p=[0.25, 0.20, 0.55])
base_price = np.array([cats[c][0] for c in category])
base_margin = np.array([cats[c][1] for c in category])

price = base_price * rng.uniform(0.7, 1.3, N)
quantity = rng.integers(1, 6, N)
discount = rng.choice([0, 0.05, 0.1, 0.2, 0.3], size=N, p=[0.5, 0.15, 0.15, 0.12, 0.08])

revenue = price * quantity * (1 - discount)
margin = base_margin - discount * 0.6 + rng.normal(0, 0.02, N)
profit = revenue * margin

df = pd.DataFrame({
    "order_id": np.arange(100000, 100000 + N),
    "order_date": order_date,
    "customer_id": rng.integers(1, 3001, N),
    "region": rng.choice(regions, size=N, p=[0.38, 0.12, 0.12, 0.16, 0.10, 0.12]),
    "segment": rng.choice(segments, size=N, p=[0.5, 0.3, 0.2]),
    "category": category,
    "quantity": quantity,
    "discount": discount,
    "revenue": revenue.round(2),
    "profit": profit.round(2),
})

# "грязь", чтобы было что чистить
df.loc[rng.choice(N, 200, replace=False), "region"] = None
df = pd.concat([df, df.sample(50, random_state=1)], ignore_index=True)

df.to_csv("orders.csv", index=False)
print("Готово:", df.shape)