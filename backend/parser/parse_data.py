import duckdb

with open('parsed_data.sql', 'r') as f:
    data = f.read()
    
duckdb.sql(data).to_csv('parsed_data.csv')