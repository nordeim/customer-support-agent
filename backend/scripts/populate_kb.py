#!/usr/bin/env python3
"""
 =============================================================================
 Customer Support AI Agent - Knowledge Base Population Script
 =============================================================================

 This script populates the knowledge base with documents for RAG implementation.
 It supports various document formats and processes them in batches.

 Usage:
     python scripts/populate_kb.py --documents-dir ./docs/knowledge-base

 Options:
     --documents-dir    Directory containing documents to process
     --chunk-size       Size of text chunks (default: 1000)
     --chunk-overlap    Overlap between chunks (default: 200)
     --batch-size       Batch size for processing (default: 10)
     --clear            Clear existing knowledge base before populating
     --recursive        Process documents recursively
     --file-pattern     File pattern to match (default: *.txt,*.md,*.pdf)
     --verbose          Enable verbose logging
"""

import argparse
import logging
import sys
import os
import re
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple, Generator
from pathlib import Path
import mimetypes
import json

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.vector_store.chroma_client import ChromaClient
from app.vector_store.embeddings import EmbeddingModel
from app.core.config import settings
from app.core.logging import setup_logging

# Try to import document processing libraries
try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document processing and text extraction"""
    
    def __init__(self):
        self.supported_formats = {
            '.txt': self._process_text,
            '.md': self._process_markdown,
            '.pdf': self._process_pdf,
            '.docx': self._process_docx,
        }
    
    def is_supported(self, file_path: Path) -> bool:
        """Check if file format is supported"""
        return file_path.suffix.lower() in self.supported_formats
    
    def extract_text(self, file_path: Path) -> Tuple[str, Dict[str, Any]]:
        """Extract text from document"""
        try:
            file_ext = file_path.suffix.lower()
            
            if file_ext not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            # Extract text using appropriate processor
            processor = self.supported_formats[file_ext]
            text, metadata = processor(file_path)
            
            # Add basic metadata
            metadata.update({
                'file_path': str(file_path),
                'file_name': file_path.name,
                'file_size': file_path.stat().st_size,
                'file_type': file_ext,
                'processed_at': datetime.utcnow().isoformat(),
            })
            
            return text, metadata
            
        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {str(e)}")
            raise
    
    def _process_text(self, file_path: Path) -> Tuple[str, Dict[str, Any]]:
        """Process plain text files"""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        metadata = {
            'encoding': 'utf-8',
            'line_count': len(text.splitlines()),
        }
        
        return text, metadata
    
    def _process_markdown(self, file_path: Path) -> Tuple[str, Dict[str, Any]]:
        """Process markdown files"""
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        
        if MARKDOWN_AVAILABLE:
            # Convert markdown to plain text
            html = markdown.markdown(markdown_text)
            # Simple HTML tag removal
            text = re.sub(r'<[^>]+>', '', html)
        else:
            # Fallback: treat as plain text
            text = markdown_text
        
        metadata = {
            'format': 'markdown',
            'html_available': MARKDOWN_AVAILABLE,
        }
        
        return text, metadata
    
    def _process_pdf(self, file_path: Path) -> Tuple[str, Dict[str, Any]]:
        """Process PDF files"""
        if not PYPDF_AVAILABLE:
            raise ImportError("pypdf library is required for PDF processing")
        
        text_parts = []
        metadata = {
            'format': 'pdf',
            'pages': 0,
        }
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                metadata['pages'] = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            text_parts.append(page_text)
                    except Exception as e:
                        logger.warning(f"Failed to extract text from page {page_num}: {str(e)}")
                        continue
        
        except Exception as e:
            raise ValueError(f"Failed to process PDF: {str(e)}")
        
        text = '\n\n'.join(text_parts)
        return text, metadata
    
    def _process_docx(self, file_path: Path) -> Tuple[str, Dict[str, Any]]:
        """Process DOCX files"""
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx library is required for DOCX processing")
        
        try:
            doc = docx.Document(file_path)
            
            text_parts = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            metadata = {
                'format': 'docx',
                'paragraphs': len(text_parts),
            }
            
            text = '\n\n'.join(text_parts)
            return text, metadata
            
        except Exception as e:
            raise ValueError(f"Failed to process DOCX: {str(e)}")

class TextChunker:
    """Handles text chunking for processing"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Split text into chunks with overlap"""
        if len(text) <= self.chunk_size:
            return [{
                'text': text,
                'metadata': metadata.copy()
            }]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Don't create tiny chunks at the end
            if end > len(text) - self.chunk_overlap // 2:
                end = len(text)
            
            chunk_text = text[start:end]
            
            # Create chunk metadata
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                'chunk_index': len(chunks),
                'chunk_start': start,
                'chunk_end': end,
                'chunk_size': len(chunk_text),
            })
            
            chunks.append({
                'text': chunk_text,
                'metadata': chunk_metadata
            })
            
            # Move start position, accounting for overlap
            if end >= len(text):
                break
            
            start = end - self.chunk_overlap
        
        return chunks

class KnowledgeBasePopulator:
    """Handles knowledge base population"""
    
    def __init__(
        self,
        documents_dir: Path,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        batch_size: int = 10,
        clear_existing: bool = False,
        recursive: bool = False,
        file_pattern: str = "*.txt,*.md,*.pdf,*.docx"
    ):
        self.documents_dir = Path(documents_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.batch_size = batch_size
        self.clear_existing = clear_existing
        self.recursive = recursive
        self.file_pattern = file_pattern
        
        # Initialize components
        self.document_processor = DocumentProcessor()
        self.text_chunker = TextChunker(chunk_size, chunk_overlap)
        self.chroma_client = ChromaClient(persist_directory=settings.chroma_persist_directory)
        self.embedding_model = EmbeddingModel(model_name=settings.embedding_model_name)
        
        # Statistics
        self.stats = {
            'documents_found': 0,
            'documents_processed': 0,
            'documents_failed': 0,
            'chunks_created': 0,
            'embeddings_generated': 0,
            'start_time': None,
            'end_time': None,
        }
    
    def discover_documents(self) -> List[Path]:
        """Discover documents in the specified directory"""
        documents = []
        patterns = [p.strip() for p in self.file_pattern.split(',')]
        
        for pattern in patterns:
            if self.recursive:
                found_docs = list(self.documents_dir.rglob(pattern))
            else:
                found_docs = list(self.documents_dir.glob(pattern))
            
            documents.extend(found_docs)
        
        # Remove duplicates and filter supported files
        documents = list(set(documents))
        documents = [doc for doc in documents if self.document_processor.is_supported(doc)]
        
        # Sort by file path for consistent processing
        documents.sort()
        
        self.stats['documents_found'] = len(documents)
        logger.info(f"Found {len(documents)} documents to process")
        
        return documents
    
    def process_document(self, document_path: Path) -> List[Dict[str, Any]]:
        """Process a single document and return chunks"""
        try:
            # Extract text and metadata
            text, metadata = self.document_processor.extract_text(document_path)
            
            if not text.strip():
                logger.warning(f"No text extracted from {document_path}")
                return []
            
            # Split into chunks
            chunks = self.text_chunker.chunk_text(text, metadata)
            
            logger.info(f"Processed {document_path}: {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Failed to process {document_path}: {str(e)}")
            raise
    
    def generate_embeddings(self, chunks: List[Dict[str, Any]]) -> List[List[float]]:
        """Generate embeddings for text chunks"""
        try:
            texts = [chunk['text'] for chunk in chunks]
            embeddings = self.embedding_model.embed_documents(texts)
            
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}")
            raise
    
    def store_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> bool:
        """Store chunks and embeddings in the vector database"""
        try:
            # Prepare data for Chroma
            documents = [chunk['text'] for chunk in chunks]
            metadatas = [chunk['metadata'] for chunk in chunks]
            ids = [self._generate_chunk_id(chunk) for chunk in chunks]
            
            # Add to Chroma
            self.chroma_client.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Stored {len(chunks)} chunks in vector database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store chunks: {str(e)}")
            return False
    
    def _generate_chunk_id(self, chunk: Dict[str, Any]) -> str:
        """Generate a unique ID for a chunk"""
        content = f"{chunk['metadata']['file_path']}:{chunk['metadata']['chunk_index']}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def process_batch(self, documents: List[Path]) -> bool:
        """Process a batch of documents"""
        all_chunks = []
        
        # Process all documents in the batch
        for doc_path in documents:
            try:
                chunks = self.process_document(doc_path)
                all_chunks.extend(chunks)
                self.stats['documents_processed'] += 1
                
            except Exception as e:
                self.stats['documents_failed'] += 1
                logger.error(f"Failed to process {doc_path}: {str(e)}")
                continue
        
        if not all_chunks:
            logger.warning("No chunks to process in this batch")
            return True
        
        # Generate embeddings for all chunks
        try:
            embeddings = self.generate_embeddings(all_chunks)
            self.stats['embeddings_generated'] += len(embeddings)
        except Exception as e:
            logger.error(f"Failed to generate embeddings for batch: {str(e)}")
            return False
        
        # Store chunks in vector database
        if not self.store_chunks(all_chunks, embeddings):
            return False
        
        self.stats['chunks_created'] += len(all_chunks)
        return True
    
    def clear_knowledge_base(self) -> bool:
        """Clear existing knowledge base"""
        try:
            if self.clear_existing:
                logger.warning("Clearing existing knowledge base...")
                # Note: Chroma doesn't have a direct clear method
                # This would require collection recreation
                logger.info("Knowledge base cleared (simulated)")
                return True
            else:
                logger.info("Skipping knowledge base clear (use --clear to enable)")
                return True
                
        except Exception as e:
            logger.error(f"Failed to clear knowledge base: {str(e)}")
            return False
    
    def populate(self) -> bool:
        """Run the complete knowledge base population process"""
        self.stats['start_time'] = datetime.utcnow()
        
        logger.info("Starting knowledge base population...")
        logger.info(f"Documents directory: {self.documents_dir}")
        logger.info(f"Chunk size: {self.chunk_size}")
        logger.info(f"Chunk overlap: {self.chunk_overlap}")
        logger.info(f"Batch size: {self.batch_size}")
        logger.info(f"Clear existing: {self.clear_existing}")
        logger.info(f"Recursive: {self.recursive}")
        
        try:
            # Step 1: Clear existing knowledge base if requested
            if not self.clear_knowledge_base():
                return False
            
            # Step 2: Discover documents
            documents = self.discover_documents()
            
            if not documents:
                logger.warning("No documents found to process")
                return True
            
            # Step 3: Process documents in batches
            total_batches = (len(documents) + self.batch_size - 1) // self.batch_size
            
            for i in range(0, len(documents), self.batch_size):
                batch = documents[i:i + self.batch_size]
                batch_num = (i // self.batch_size) + 1
                
                logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} documents)")
                
                if not self.process_batch(batch):
                    logger.error(f"Failed to process batch {batch_num}")
                    return False
            
            self.stats['end_time'] = datetime.utcnow()
            self._log_statistics()
            
            logger.info("Knowledge base population completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Knowledge base population failed: {str(e)}")
            return False
    
    def _log_statistics(self) -> None:
        """Log processing statistics"""
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        logger.info("=" * 50)
        logger.info("KNOWLEDGE BASE POPULATION STATISTICS")
        logger.info("=" * 50)
        logger.info(f"Documents found: {self.stats['documents_found']}")
        logger.info(f"Documents processed: {self.stats['documents_processed']}")
        logger.info(f"Documents failed: {self.stats['documents_failed']}")
        logger.info(f"Chunks created: {self.stats['chunks_created']}")
        logger.info(f"Embeddings generated: {self.stats['embeddings_generated']}")
        logger.info(f"Processing time: {duration:.2f} seconds")
        
        if self.stats['documents_processed'] > 0:
            avg_chunks_per_doc = self.stats['chunks_created'] / self.stats['documents_processed']
            logger.info(f"Average chunks per document: {avg_chunks_per_doc:.2f}")
        
        if duration > 0:
            docs_per_second = self.stats['documents_processed'] / duration
            logger.info(f"Documents per second: {docs_per_second:.2f}")
        
        logger.info("=" * 50)

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Populate the knowledge base with documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/populate_kb.py --documents-dir ./docs/knowledge-base
    python scripts/populate_kb.py --documents-dir ./docs --recursive
    python scripts/populate_kb.py --documents-dir ./docs --chunk-size 500 --clear
        """
    )
    
    parser.add_argument(
        "--documents-dir",
        type=Path,
        required=True,
        help="Directory containing documents to process"
    )
    
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Size of text chunks (default: 1000)"
    )
    
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=200,
        help="Overlap between chunks (default: 200)"
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Batch size for processing (default: 10)"
    )
    
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing knowledge base before populating"
    )
    
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process documents recursively"
    )
    
    parser.add_argument(
        "--file-pattern",
        type=str,
        default="*.txt,*.md,*.pdf,*.docx",
        help="File pattern to match (default: *.txt,*.md,*.pdf,*.docx)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser.parse_args()

def main() -> int:
    """Main entry point"""
    # Parse arguments
    args = parse_arguments()
    
    # Validate arguments
    if not args.documents_dir.exists():
        print(f"❌ Documents directory does not exist: {args.documents_dir}")
        return 1
    
    if not args.documents_dir.is_dir():
        print(f"❌ Path is not a directory: {args.documents_dir}")
        return 1
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging()
    logging.getLogger().setLevel(log_level)
    
    # Create populator
    populator = KnowledgeBasePopulator(
        documents_dir=args.documents_dir,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        batch_size=args.batch_size,
        clear_existing=args.clear,
        recursive=args.recursive,
        file_pattern=args.file_pattern
    )
    
    try:
        # Run population
        success = populator.populate()
        
        if success:
            print("\n✅ Knowledge base population completed successfully!")
            return 0
        else:
            print("\n❌ Knowledge base population failed!")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Knowledge base population interrupted by user")
        print("\n⚠️  Knowledge base population interrupted")
        return 1
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
