"""
Semantic Chunking Service

Splits markdown content into semantically coherent chunks for embedding.
"""

import re
from typing import List

from app.models import ContentSegment
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ChunkingService:
    """
    Service for splitting book content into optimal-sized semantic chunks.

    Target: 200-500 words per chunk
    Strategy: Split by markdown headings first, then paragraphs if needed
    """

    def __init__(self, min_words: int = 200, max_words: int = 700):
        """
        Initialize chunking service.

        Args:
            min_words: Minimum words per chunk (default: 200)
            max_words: Maximum words per chunk (default: 500)
        """
        self.min_words = min_words
        self.max_words = max_words

    def chunk_chapter(
        self,
        content: str,
        chapter_number: int,
        chapter_metadata: dict = None
    ) -> List[ContentSegment]:
        """
        Split chapter content into semantic chunks.

        Args:
            content: Full chapter markdown content
            chapter_number: Chapter number
            chapter_metadata: Optional metadata to attach to chunks

        Returns:
            List[ContentSegment]: List of chunked segments ready for embedding
        """
        if not content.strip():
            logger.warning(f"Empty content for chapter {chapter_number}")
            return []

        if chapter_metadata is None:
            chapter_metadata = {}

        # Split by markdown sections (headings)
        sections = self._split_by_headings(content)

        # Further chunk sections if they exceed max_words
        chunks = []
        for section_title, section_content in sections:
            section_chunks = self._chunk_section(section_content, section_title)
            chunks.extend(section_chunks)

        # Final pass: ensure no chunk is below minimum word count
        chunks = self._ensure_minimum_chunks(chunks)

        # Create ContentSegment objects
        segments = []
        for order, (section_title, chunk_text) in enumerate(chunks):
            word_count = len(chunk_text.split())

            segment = ContentSegment(
                text=chunk_text,
                chapter_number=chapter_number,
                section_title=section_title,
                order=order,
                word_count=word_count,
                metadata=chapter_metadata.copy()
            )
            segments.append(segment)

        logger.info(
            f"Chunked chapter {chapter_number} into {len(segments)} segments "
            f"({sum(s.word_count for s in segments)} total words)"
        )

        return segments

    def _split_by_headings(self, content: str) -> List[tuple[str, str]]:
        """
        Split markdown content by headings (##, ###, etc.).

        Args:
            content: Markdown content

        Returns:
            List[tuple[str, str]]: List of (section_title, section_content) pairs
        """
        # Pattern to match markdown headings: ## Title or ### Title
        heading_pattern = re.compile(r'^(#{2,6})\s+(.+)$', re.MULTILINE)

        sections = []
        last_pos = 0
        current_title = ""

        for match in heading_pattern.finditer(content):
            # Extract content before this heading
            if last_pos > 0:
                section_content = content[last_pos:match.start()].strip()
                if section_content:
                    sections.append((current_title, section_content))

            # Update current section title
            current_title = match.group(2).strip()
            last_pos = match.end()

        # Add final section
        if last_pos < len(content):
            section_content = content[last_pos:].strip()
            if section_content:
                sections.append((current_title, section_content))

        # If no headings found, treat entire content as one section
        if not sections:
            sections.append(("", content.strip()))

        return sections

    def _chunk_section(self, content: str, section_title: str) -> List[tuple[str, str]]:
        """
        Chunk a section into smaller pieces if needed.

        Args:
            content: Section content
            section_title: Section heading title

        Returns:
            List[tuple[str, str]]: List of (section_title, chunk_text) pairs
        """
        word_count = len(content.split())

        # If section is within limits, return as-is
        if self.min_words <= word_count <= self.max_words:
            return [(section_title, content)]

        # If section is too small, return as-is (will be merged later if needed)
        if word_count < self.min_words:
            return [(section_title, content)]

        # Section is too large - split by paragraphs
        paragraphs = self._split_by_paragraphs(content)
        chunks = self._merge_small_chunks(paragraphs)

        # Attach section title to all chunks from this section
        return [(section_title, chunk) for chunk in chunks]

    def _split_by_paragraphs(self, content: str) -> List[str]:
        """
        Split content into paragraphs.

        Args:
            content: Text content

        Returns:
            List[str]: List of paragraph texts
        """
        # Split by double newlines (paragraph breaks)
        paragraphs = re.split(r'\n\s*\n', content)

        # Clean and filter empty paragraphs
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        return paragraphs

    def _merge_small_chunks(self, paragraphs: List[str]) -> List[str]:
        """
        Merge small paragraphs to reach target chunk size.

        Args:
            paragraphs: List of paragraph texts

        Returns:
            List[str]: List of merged chunks
        """
        if not paragraphs:
            return []

        chunks = []
        current_chunk = []
        current_words = 0

        for para in paragraphs:
            para_words = len(para.split())

            # If adding this paragraph exceeds max_words, finalize current chunk
            if current_words + para_words > self.max_words and current_chunk:
                # Only finalize if current chunk meets minimum
                if current_words >= self.min_words:
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = [para]
                    current_words = para_words
                else:
                    # Keep adding even if over max to reach minimum
                    current_chunk.append(para)
                    current_words += para_words
            else:
                current_chunk.append(para)
                current_words += para_words

            # If current chunk reaches target, finalize it
            if current_words >= self.min_words and current_words <= self.max_words:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_words = 0

        # Handle remaining content
        if current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            chunk_words = len(chunk_text.split())

            # If last chunk is too small, merge with previous chunk
            if chunk_words < self.min_words and chunks:
                chunks[-1] = chunks[-1] + "\n\n" + chunk_text
            else:
                # Keep it even if small (edge case for very short sections)
                chunks.append(chunk_text)

        return chunks

    def _ensure_minimum_chunks(self, chunks: List[tuple[str, str]]) -> List[tuple[str, str]]:
        """
        Ensure all chunks meet minimum word count by merging small chunks.

        Args:
            chunks: List of (section_title, chunk_text) tuples

        Returns:
            List[tuple[str, str]]: Chunks with all meeting minimum word count
        """
        if not chunks:
            return []

        result = []
        i = 0

        while i < len(chunks):
            section_title, chunk_text = chunks[i]
            word_count = len(chunk_text.split())

            # If chunk meets minimum, keep it
            if word_count >= self.min_words:
                result.append((section_title, chunk_text))
                i += 1
            else:
                # Chunk is too small - merge with next or previous
                if i + 1 < len(chunks):
                    # Merge with next chunk
                    next_title, next_text = chunks[i + 1]
                    merged_text = chunk_text + "\n\n" + next_text
                    # Use the first non-empty title
                    merged_title = section_title if section_title else next_title
                    chunks[i + 1] = (merged_title, merged_text)
                    i += 1
                elif result:
                    # Merge with previous chunk (last chunk in list)
                    prev_title, prev_text = result[-1]
                    merged_text = prev_text + "\n\n" + chunk_text
                    result[-1] = (prev_title, merged_text)
                    i += 1
                else:
                    # Edge case: only one very small chunk, keep it
                    # (will fail validation but better than losing content)
                    result.append((section_title, chunk_text))
                    i += 1

        return result


# Singleton instance
chunking_service = ChunkingService()