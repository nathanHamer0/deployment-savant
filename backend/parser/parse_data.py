import duckdb

with open('backend/parser/parse_data.sql', 'r') as f:
    data = f.read()
    
duckdb.sql(data).to_csv('backend/parser/parsed_data.csv')