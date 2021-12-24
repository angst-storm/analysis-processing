def write_csv(optimized_csv_output_str, create_csv):
    if(create_csv):
        f = open('parser/done.csv', 'w')
        f.write(optimized_csv_output_str)
        f.close()