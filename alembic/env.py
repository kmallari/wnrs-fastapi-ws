from dotenv import load_dotenv
import os
from alembic import context

load_dotenv()

# Update config section
config = context.config

config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

from ws.src.db.models import Base  # Import your models
target_metadata = Base.metadata  # Update target metadata 
