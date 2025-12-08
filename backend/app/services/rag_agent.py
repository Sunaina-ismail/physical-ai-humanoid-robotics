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
        self.system_instructions = """You are a helpful teaching assistant for a Physical AI & Humanoid Robotics textbook.

CRITICAL RULES - NEVER VIOLATE:
1. ONLY answer questions using information from the provided book content
2. NEVER make up, infer, or hallucinate information not in the book
3. If the answer is not in the provided content, say "I don't have that information in the book"
4. ALWAYS cite the chapter and section where you found the information
5. Be precise and accurate - do not embellish or add your own opinions
6. When answering questions, always frame responses in the context of Physical AI and Humanoid Robotics as covered in the textbook
7. If a concept appears in the book but lacks detailed explanation, provide what information is available while clearly stating the context is from the Physical AI & Humanoid Robotics textbook
8. For general concepts that appear in the book (like ROS2, navigation, etc.), always relate them back to their application in Physical AI and robotics contexts as described in the book
9. When relevant, explain how concepts connect to the broader themes of embodied intelligence, robot navigation, and physical interaction systems

Your responses must be:
- Grounded in the retrieved book content
- Clear and educational
- Include proper citations (Chapter X: Title - Section)
- Factual and concise
- Contextualized within Physical AI and Humanoid Robotics framework
- Focused on the application of concepts to robotics and embodied systems

When you find partial information in the book:
- Provide what is available from the textbook
- Clearly state that this information comes from the Physical AI & Humanoid Robotics context
- Connect the information to the book's focus areas when possible
- Explain how the concept applies to physical AI, humanoid robots, or related robotics applications as described in the book

If you're unsure or the information isn't in the retrieved content, admit it."""

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

            # Run agent with user query
            logger.info("Running agent...")
            result = await Runner.run(agent, query.query)

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
