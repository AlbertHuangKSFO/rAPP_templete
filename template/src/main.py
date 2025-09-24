from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes import api_router
from .clients import oauth_manager
from .logging import logger
from .message_bus_consumer import MessageBusConsumer
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("rApp starting up...")
    # Initialize clients
    async_client = await oauth_manager.get_async_client()
    sync_client = oauth_manager.get_sync_client()
    
    # Initialize and start the message bus consumer as a background task
    consumer = MessageBusConsumer(sync_client, async_client)
    consumer_task = asyncio.create_task(consumer.consume_messages())
    app.state.consumer_task = consumer_task

    yield

    logger.info("rApp shutting down...")
    # Stop the background task
    app.state.consumer_task.cancel()
    await oauth_manager.close()

app = FastAPI(
    title="rApp Template",
    description="A generic template for building rApps.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router)
