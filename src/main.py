import asyncio
import os
import sys

from fastapi import FastAPI

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import src.queries.database