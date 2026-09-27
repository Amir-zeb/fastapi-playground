from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///test.db"

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine)