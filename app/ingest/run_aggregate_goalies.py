# ingest/run_aggregate_goalies.py

import asyncio
from app.ingest.aggregate_goalies_summary import aggregate_goalies_summary

if __name__ == "__main__":
    asyncio.run(aggregate_goalies_summary())