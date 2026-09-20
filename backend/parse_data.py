import duckdb

with open('backend/data/parse_data.sql', 'r') as f:
    data = f.read()
    
duckdb.sql(data).to_csv('backend/data/parsed_data.csv')