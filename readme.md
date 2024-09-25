# PGTest Benchmarking Tool

A command-line tool to benchmark the performance of pgpool-II, a popular PostgreSQL connection pooling and replication solution.

## Overview
This tool allows you to run a specified number of concurrent queries against a pgpool-II instance and measure the execution time of each query. It also provides statistics on the minimum, maximum, and average execution times, as well as the number of errors encountered during the benchmark.

## Instalation

Install the required python libraries using

```bash
pip install -r requirements.txt
```

## Usage
To run the benchmark, simply execute the app.py script with the following options:

-n or --num_queries: The number of concurrent queries to run (default: 10)
-d or --delay_between_queries: The delay between each query in seconds (default: 0)

## Example:

```bash
python app.py -n 50 -d 0.1
```

This will run 50 concurrent queries with a delay of 0.1 seconds between each query.

## Requirements
- Python 3.7+
- asyncpg 0.29.0+
- a modern PostgreSQL instance

- DB_HOST: The hostname or IP address of the pgpool-II instance (default: localhost)
- DB_PORT: The port number of the pgpool-II instance (default: 5432)
- DB_DB: The name of the PostgreSQL database (default: postgres)
- DB_USER: The username to use for the database connection (default: postgres)
- DB_PASSWORD: The password to use for the database connection (default: postgres)

You can set these environment variables in your shell or in a .env file.

## Contributing
Contributions are welcome! Please submit a pull request with your changes.

## License
This project is licensed under the MIT License.
