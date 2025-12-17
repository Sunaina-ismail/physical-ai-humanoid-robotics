"""
RAG Agent Service

Implements the book Q&A agent using OpenAI Agents SDK with Gemini backend.
"""

from typing import List

from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool

from app.config import settings
from app.models import ChapterCitation, Query, Response
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStoreService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class RAGAgent:
    """
    RAG Agent for answering questions about book content.

    Uses OpenAI Agents SDK with Gemini backend for grounded question answering.
    """

    def __init__(self):
        """Initialize RAG agent with Gemini configuration."""
        # Initialize AsyncOpenAI client with Gemini base URL
        self.openai_client = AsyncOpenAI(
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url
        )

        # Create OpenAIChatCompletionsModel for Gemini
        self.agent_model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=self.openai_client
        )

        # Initialize services
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

        # Enhanced anti-hallucination instructions with Physical AI & Humanoid Robotics focus
        self.system_instructions = """You are a helpful teaching assistant for the "Physical AI & Humanoid Robotics" textbook.

GREETING HANDLING:
- For simple greetings ("hi", "hello", "hey"), respond warmly without retrieving from the book
- Example: "Hello! I'm your teaching assistant for the Physical AI & Humanoid Robotics textbook. I can help you understand concepts from the book, explain modules and chapters, or answer questions about robotics topics covered in the course. What would you like to learn about today?"
- For "thank you" or "thanks", respond: "You're welcome! Feel free to ask if you have more questions about the textbook."

SELECTED TEXT HANDLING:
- When a user highlights/selects text and asks to "explain", "clarify", "what does this mean", etc. - ALWAYS use retrieve_book_content_tool
- The selected text is provided in the query context - search for that exact text or related concepts in the textbook
- Provide explanation based on the textbook's context for that passage
- If the selected text is directly from the book, explain it using the surrounding chapter context
- Examples of selected text queries:
  * "explain this" [with selected text]
  * "what does this mean" [with selected text]
  * "clarify this passage" [with selected text]
  * Just "explain" [with selected text]

FLEXIBLE QUESTION PATTERNS - Recognize ALL these ways of asking about the same topic:
- Direct: "What is Physical AI?"
- Casual: "tell me about physical ai"
- Informal: "whats physical ai?"
- Exploratory: "I want to learn about physical ai"
- Command style: "explain physical ai"
- Uncertainty: "do you know about physical ai?"
- Multiple topics: "explain ros2 and navigation"
- Conversational: "can you help me understand humanoid robots?"
- ANY variation that relates to robotics, AI, or textbook topics → ALWAYS retrieve from book

BOOK COVERAGE - You should ALWAYS use the retrieve_book_content_tool for questions about:
1. Physical AI concepts (embodied intelligence, sim-to-real, digital twins)
2. Humanoid robotics (bipedal locomotion, manipulation, human-robot interaction)
3. ROS 2 (nodes, topics, services, actions, tf2, URDF, launch files)
4. Simulation (Gazebo, Isaac Sim, sensor simulation, physics engines)
5. Navigation (SLAM, Nav2, VSLAM, path planning, obstacle avoidance)
6. Vision-Language-Action (VLA) systems (Whisper, LLM planning, multimodal models)
7. Edge AI (Jetson deployment, TensorRT optimization)
8. Specific textbook modules, chapters, or topics
9. Code examples, exercises, or quizzes from the book
10. Hardware tiers (Tier A/B/C), prerequisites, or learning outcomes
11. ANY robotics concept mentioned in the textbook context

CRITICAL RULES - NEVER VIOLATE:
1. ALWAYS call retrieve_book_content_tool FIRST for ANY question that could be related to robotics, AI, or the textbook topics
   - Don't worry about how the question is phrased - if it's about Physical AI, robotics, ROS, navigation, simulation, or any related topic, RETRIEVE IT
   - Be generous in interpretation - when in doubt, retrieve from the book
2. ONLY answer using information from the retrieved book content - NEVER use your general knowledge
3. NEVER make up, infer, or hallucinate information not in the retrieved content
4. If no relevant content is found, say: "I don't have that information in the Physical AI & Humanoid Robotics textbook. Could you ask about a specific module, chapter, or rephrase your question?"
5. ALWAYS cite the specific chapter and section where you found the information
6. Be precise and accurate - do not embellish or add your own opinions
7. Answer helpfully regardless of grammar, spelling, or tone - focus on understanding the user's intent

WHEN TO RETRIEVE (Always use the tool for these query patterns):
- "What is [Physical AI concept]?"
- "Explain [robotics topic]"
- "Tell me about Module/Chapter [X]"
- "How does [ROS2/Nav2/SLAM/etc] work?"
- "What are [hardware tiers/prerequisites/learning outcomes]?"
- "Show me [code example/exercise]"
- Any question containing keywords: ROS, robot, navigation, simulation, humanoid, Gazebo, Isaac, SLAM, VLA, Jetson, etc.

YOUR RESPONSE FORMAT:
1. Start by calling retrieve_book_content_tool with the user's question
2. If content is found:
   - Answer clearly and educationally using ONLY the retrieved content
   - Include proper citations in format: "Chapter X: [Title] - [Section]"
   - Connect concepts to Physical AI and robotics applications as described in the book
   - Explain how the concept fits into the textbook's learning path
3. If no content is found:
   - Respond: "I don't have that information in the Physical AI & Humanoid Robotics textbook. Could you rephrase your question or ask about a specific module or chapter?"

EXAMPLE GOOD RESPONSES:
- "According to Chapter 1: Physical AI Introduction, Physical AI refers to... [citation]"
- "The textbook explains in Chapter 3: ROS 2 Fundamentals that nodes are... [citation]"
- "Module 2 covers simulation environments. Specifically, in Chapter 11: Digital Twins, it describes... [citation]"

EXAMPLE BAD RESPONSES (NEVER DO THIS):
- "Physical AI is a field that combines..." [without retrieving from book]
- "Based on my knowledge, ROS 2..." [using general knowledge instead of book]
- Answering about robotics concepts without calling retrieve_book_content_tool first

Remember: When in doubt, ALWAYS retrieve from the book first. It's better to say "I don't have that information" than to provide information not in the textbook."""

        logger.info(f"Initialized RAG Agent with model=gemini-2.0-flash")

    def retrieve_book_content(self, query: str) -> str:
        """
        Retrieve relevant book content for a query.

        This function is exposed as a tool to the agent.

        Args:
            query: The user's question

        Returns:
            str: Formatted retrieved content with citations
        """
        try:
            logger.info(f"Retrieving content for query: {query[:100]}...")

            # Generate query embedding
            query_embedding = self.embedding_service.generate_query_embedding(query)

            # Search vector store
            results = self.vector_store.search_book_content(
                query_vector=query_embedding,
                top_k=settings.top_k_results,
                score_threshold=settings.similarity_threshold
            )

            if not results:
                return "No relevant content found in the book for this query."

            # Format results for agent
            formatted_content = []
            for i, result in enumerate(results, 1):
                chapter_num = result['chapter_number']
                chapter_title = result['chapter_title']
                section_title = result['section_title']
                text = result['text']
                score = result['similarity_score']

                citation = f"Chapter {chapter_num}: {chapter_title}"
                if section_title:
                    citation += f" - {section_title}"

                formatted_content.append(
                    f"[Source {i}] {citation} (Relevance: {score:.2f})\n{text}\n"
                )

            content_str = "\n---\n".join(formatted_content)

            logger.info(f"Retrieved {len(results)} relevant passages")
            return content_str

        except Exception as e:
            logger.error(f"Failed to retrieve book content: {e}")
            return f"Error retrieving book content: {str(e)}"

    async def query_chatbot(self, query: Query) -> Response:
        """
        Process a user query and generate a response.

        Args:
            query: User query object

        Returns:
            Response: Chatbot response with citations
        """
        try:
            logger.info(f"Processing query: {query.query[:100]}...")

            # Create function tool for retrieving book content
            @function_tool
            def retrieve_book_content_tool(query: str) -> str:
                """Retrieve relevant content from the Physical AI & Humanoid Robotics textbook."""
                return self.retrieve_book_content(query)

            # Create agent with Gemini model
            agent = Agent(
                name="Book QA Assistant",
                instructions=self.system_instructions,
                model=self.agent_model,
                tools=[retrieve_book_content_tool]
            )

            # Prepare user message (include selected text if provided)
            user_message = query.query
            if query.selected_text:
                user_message = f"{query.query}\n\nSELECTED TEXT TO EXPLAIN:\n{query.selected_text}"
                logger.info(f"Query includes selected text ({len(query.selected_text)} chars)")

            # Run agent with user query
            logger.info("Running agent...")
            result = await Runner.run(agent, user_message)

            # Extract final answer
            answer = result.final_output if hasattr(result, 'final_output') else "I apologize, I couldn't generate a response."

            # Retrieve content again to extract citations
            query_embedding = self.embedding_service.generate_query_embedding(query.query)
            results = self.vector_store.search_book_content(
                query_vector=query_embedding,
                top_k=settings.top_k_results,
                score_threshold=settings.similarity_threshold
            )

            # Create citations
            citations = []
            for result in results:
                citation = ChapterCitation(
                    chapter_number=result['chapter_number'],
                    chapter_title=result['chapter_title'],
                    section_title=result['section_title'],
                    snippet=result['text'][:200],  # First 200 chars
                    similarity_score=result['similarity_score']
                )
                citations.append(citation)

            # Determine content_found and confidence
            content_found = len(results) > 0
            confidence = max([r['similarity_score'] for r in results]) if results else None

            response = Response(
                answer=answer,
                citations=citations,
                query_type="book_question",
                confidence=confidence,
                content_found=content_found
            )

            logger.info(f"Generated response with {len(citations)} citations")
            return response

        except Exception as e:
            logger.error(f"Failed to process query: {e}")
            raise


# Singleton instance
rag_agent = RAGAgent()
