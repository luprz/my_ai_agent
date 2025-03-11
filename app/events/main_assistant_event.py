
import logging
from app.celery_app import celery_app
from app.workflows.main_workflow import MainWorkflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery_app.task(name='app.events.main_assistant_event.process_conversation')
def main_assistant_event(session_id: str, input: str):
    logger.info(f"Processing conversation for session_id: {session_id}")
    
    # Process the user input
    assistant = MainWorkflow()
    result = assistant.run(session_id=session_id, input=input)

    return result