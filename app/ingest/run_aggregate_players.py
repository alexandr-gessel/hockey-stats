# ingest/run_aggregate_players.py

import asyncio
from app.ingest.aggregate_players_summary import aggregate_players_summary

if __name__ == "__main__":
    asyncio.run(aggregate_players_summary())
