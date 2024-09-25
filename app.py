import argparse
import asyncio
import os
import time
from statistics import mean

import asyncpg
from dotenv import load_dotenv

# Database connection details for pgpool-II
try:
 
    load_dotenv()
    DATABASE_HOST = os.getenv("DB_HOST")
    DATABASE_PORT = int(os.getenv("DB_PORT"))
    DATABASE_NAME = os.getenv("DB_DB")
    DATABASE_USER = os.getenv("DB_USER")
    DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
except ImportError:
    DATABASE_HOST = "host"
    DATABASE_PORT = 5432
    DATABASE_NAME = "postgres"
    DATABASE_USER = "user"
    DATABASE_PASSWORD = "password"

# Async function to establish a database connection
async def get_db_connection():
    try:
        conn = await asyncpg.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
        )
        return conn
    except Exception as e:
        raise Exception(f"Database connection failed: {e}")

# Function to perform a query and measure its execution time
async def execute_query():
    try:
        conn = await get_db_connection()
        query = "SELECT inet_server_addr() AS server_ip, inet_server_port() AS server_port"
        start_time = time.time()
        result = await conn.fetchrow(query)
        execution_time = time.time() - start_time
        await conn.close()
        return {
            "server_ip": result["server_ip"],
            "server_port": result["server_port"],
            "execution_time": execution_time
        }
    except Exception as e:
        return {"error": str(e)}

# Function to perform benchmarking
async def run_benchmark(num_queries, delay_between_queries):
    results = []
    try:
        # Run the queries concurrently
        start_time = time.time()
        tasks = [execute_query() for _ in range(num_queries)]

        if delay_between_queries > 0:
            for task in tasks:
                await asyncio.sleep(delay_between_queries)

        responses = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        # Extract execution times from the results
        exec_times = [res['execution_time'] for res in responses if 'execution_time' in res]
        server_ips = {res['server_ip'] for res in responses if 'server_ip' in res}
        error_count = len([res for res in responses if 'error' in res])

        # Calculate statistics
        if exec_times:
            min_time = min(exec_times)
            max_time = max(exec_times)
            avg_time = mean(exec_times)
        else:
            min_time = max_time = avg_time = 0

        # Print the benchmark statistics
        print(f"Benchmark complete:")
        print(f"  Number of queries: {num_queries}")
        print(f"  Servers hit: {list(server_ips)}")
        print(f"  Total time: {total_time:.4f} seconds")
        print(f"  Min time: {min_time:.4f} seconds")
        print(f"  Max time: {max_time:.4f} seconds")
        print(f"  Avg time: {avg_time:.4f} seconds")
        print(f"  Errors: {error_count}")

    except Exception as e:
        print(f"Benchmarking failed: {e}")

# Main function to handle command-line arguments and run the benchmark
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="pgpool-II Benchmarking Tool")
    parser.add_argument(
        "-n", "--num_queries", type=int, default=10, 
        help="Number of concurrent queries to run (default: 10)"
    )
    parser.add_argument(
        "-d","--delay_between_queries", type=float, default=0, 
        help="Delay between each query in seconds (default: 0)"
    )
    args = parser.parse_args()

    # Run the benchmark using asyncio
    asyncio.run(run_benchmark(args.num_queries, args.delay_between_queries))

if __name__ == "__main__":
    main()
