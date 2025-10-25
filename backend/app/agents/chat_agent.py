# backend/app/agents/chat_agent.py
import time
from typing import List, Dict, Any, Optional
from agent_framework import AssistantsClient, Tool
from ..tools.memory_tool import MemoryTool
from ..tools.rag_tool import RAGTool
from ..tools.attachment_tool import AttachmentTool
from ..tools.escalation_tool import EscalationTool
from ..core.logging import logger
from ..core.config import settings

class ChatAgent:
    """Customer support chat agent using Microsoft Agent Framework"""
    
    def __init__(self):
        # Initialize the Assistants client
        self.client = AssistantsClient(
            endpoint=settings.agent_framework_endpoint,
            api_key=settings.agent_framework_api_key
        )
        
        # Initialize tools
        self.memory_tool = MemoryTool()
        self.rag_tool = RAGTool()
        self.attachment_tool = AttachmentTool()
        self.escalation_tool = EscalationTool()
        
        # Register tools with the agent
        self.tools = [
            Tool(
                name="memory",
                description="Store and retrieve information about the user and conversation",
                function=self.memory_tool.execute
            ),
            Tool(
                name="rag_search",
                description="Search the knowledge base for relevant information",
                function=self.rag_tool.execute
            ),
            Tool(
                name="process_attachment",
                description="Process and extract text from uploaded attachments",
                function=self.attachment_tool.execute
            ),
            Tool(
                name="escalate_to_human",
                description="Escalate the conversation to a human agent",
                function=self.escalation_tool.execute
            )
        ]
        
        # Create or get the assistant
        self.assistant = self._create_or_get_assistant()
    
    def _create_or_get_assistant(self):
        """Create or retrieve the assistant"""
        assistant_instructions = """
        You are a helpful customer support agent. Your goal is to assist customers with their inquiries and issues.
        
        Guidelines:
        1. Be polite, professional, and empathetic
        2. Use the memory tool to remember important information about the customer
        3. Use the rag_search tool to find relevant information from the knowledge base
        4. Process attachments if the customer uploads any documents
        5. Escalate to a human agent if the issue requires human intervention
        6. Always cite your sources when using information from the knowledge base
        7. If you don't know the answer, be honest and try to help the customer find the right resource
        """
        
        # Check if assistant already exists
        assistants = self.client.list_assistants()
        for assistant in assistants:
            if assistant.name == "Customer Support Agent":
                return assistant
        
        # Create new assistant
        return self.client.create_assistant(
            name="Customer Support Agent",
            instructions=assistant_instructions,
            tools=self.tools
        )
    
    def create_thread(self, session_id: str, user_id: Optional[str] = None) -> str:
        """Create a new conversation thread"""
        # Create thread in Agent Framework
        thread = self.client.create_thread()
        
        # Store thread mapping in memory
        self.memory_tool.store_thread_mapping(session_id, thread.id, user_id)
        
        logger.info(
            f"Created new thread {thread.id} for session {session_id}",
            extra={"session_id": session_id, "user_id": user_id, "thread_id": thread.id}
        )
        
        return thread.id
    
    def send_message(
        self, 
        session_id: str, 
        message: str, 
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Send a message to the agent and get a response"""
        start_time = time.time()
        
        # Get thread ID for this session
        thread_id = self.memory_tool.get_thread_id(session_id)
        if not thread_id:
            thread_id = self.create_thread(session_id)
        
        # Process attachments if any
        if attachments:
            for attachment in attachments:
                self.attachment_tool.process_attachment(session_id, attachment)
        
        # Add message to thread
        self.client.create_message(
            thread_id=thread_id,
            role="user",
            content=message
        )
        
        # Run the assistant
        run = self.client.create_run(thread_id=thread_id, assistant_id=self.assistant.id)
        
        # Wait for completion
        while run.status in ["queued", "in_progress"]:
            run = self.client.get_run(thread_id=thread_id, run_id=run.id)
            time.sleep(0.5)
        
        # Get messages
        messages = self.client.list_messages(thread_id=thread_id)
        assistant_message = next((m for m in messages if m.role == "assistant"), None)
        
        # Calculate execution time
        execution_time = (time.time() - start_time) * 1000
        
        # Log the interaction
        logger.info(
            f"Agent response generated for session {session_id}",
            extra={
                "session_id": session_id,
                "thread_id": thread_id,
                "execution_time_ms": execution_time,
                "run_status": run.status
            }
        )
        
        # Return the response
        return {
            "message": assistant_message.content if assistant_message else "I'm sorry, I couldn't generate a response.",
            "sources": self._extract_sources(assistant_message) if assistant_message else [],
            "requires_escalation": self._check_escalation(run)
        }
    
    def _extract_sources(self, message) -> List[Dict[str, Any]]:
        """Extract source citations from a message"""
        # Implementation depends on how the Agent Framework formats citations
        # This is a placeholder implementation
        return []
    
    def _check_escalation(self, run) -> bool:
        """Check if the run resulted in an escalation"""
        # Check if the escalation tool was called
        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            if tool_call.function.name == "escalate_to_human":
                return True
        return False
