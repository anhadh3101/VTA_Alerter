import pandas as pd

url = "https://www.vta.org/go/routes/rapid-500#weekday-sb"
tables = pd.read_html(url)
print(tables)
