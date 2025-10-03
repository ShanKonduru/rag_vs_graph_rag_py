from typing import List, Dict, Any


class PromptTemplate:
    """Template for creating prompts"""
    
    def __init__(self, template: str, required_vars: List[str]):
        self.template = template
        self.required_vars = required_vars
    
    def format(self, **kwargs) -> str:
        """Format template with variables"""
        # Check required variables
        missing_vars = [var for var in self.required_vars if var not in kwargs]
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")
        
        return self.template.format(**kwargs)


# Standard RAG Prompt Templates
RAG_SYSTEM_PROMPT = PromptTemplate(
    template="""You are a helpful AI assistant. Use the provided context to answer the user's question accurately and comprehensively. 

Guidelines:
- Base your answer primarily on the provided context
- If the context doesn't contain enough information to answer the question, say so
- Be concise but complete
- Cite relevant parts of the context when possible
- Don't make up information not present in the context""",
    required_vars=[]
)

RAG_ANSWER_PROMPT = PromptTemplate(
    template="""Context:
{context}

Question: {question}

Answer: Based on the provided context, """,
    required_vars=["context", "question"]
)

# Graph RAG Prompt Templates  
GRAPH_RAG_SYSTEM_PROMPT = PromptTemplate(
    template="""You are a helpful AI assistant with access to both document excerpts and knowledge graph information. Use both sources to provide comprehensive and accurate answers.

Guidelines:
- Integrate information from both text context and graph relationships
- Use graph information to understand connections between entities
- Prioritize factual accuracy based on the provided sources
- Explain relationships and connections when relevant
- If information is incomplete, acknowledge the limitations""",
    required_vars=[]
)

GRAPH_RAG_ANSWER_PROMPT = PromptTemplate(
    template="""Text Context:
{text_context}

Graph Information:
{graph_context}

Question: {question}

Answer: Based on the provided text and graph information, """,
    required_vars=["text_context", "graph_context", "question"]
)

# Knowledge Graph Only Prompt Templates
KG_SYSTEM_PROMPT = PromptTemplate(
    template="""You are a helpful AI assistant that answers questions based on knowledge graph information. You have access to structured knowledge about entities and their relationships.

Guidelines:
- Use the provided graph information to construct accurate answers
- Explain relationships between entities when relevant
- Be specific about the connections and properties mentioned in the graph
- If the graph doesn't contain sufficient information, say so clearly
- Focus on factual relationships and properties from the graph""",
    required_vars=[]
)

KG_ANSWER_PROMPT = PromptTemplate(
    template="""Knowledge Graph Information:
{graph_data}

Question: {question}

Answer: Based on the knowledge graph information, """,
    required_vars=["graph_data", "question"]
)

# Entity Extraction Prompts
ENTITY_EXTRACTION_PROMPT = PromptTemplate(
    template="""Extract entities and their types from the following text. 

Text: {text}

Extract the following types of entities:
- PERSON: People's names
- ORGANIZATION: Companies, institutions, organizations
- LOCATION: Places, cities, countries, addresses
- CONCEPT: Important concepts, topics, subjects
- DATE: Dates, times, periods
- OTHER: Any other important entities

Format your response as a JSON list of objects with 'text', 'label', and 'start_pos' fields.

Entities:""",
    required_vars=["text"]
)

# Relation Extraction Prompts
RELATION_EXTRACTION_PROMPT = PromptTemplate(
    template="""Given the following text and entities, extract relationships between them.

Text: {text}

Entities: {entities}

Extract meaningful relationships in the format: (subject, predicate, object)
Only extract relationships that are explicitly mentioned or strongly implied in the text.

Format your response as a JSON list of objects with 'subject', 'predicate', and 'object' fields.

Relationships:""",
    required_vars=["text", "entities"]
)

# Evaluation Prompts
EVALUATION_RELEVANCE_PROMPT = PromptTemplate(
    template="""Evaluate how relevant the provided answer is to the given question.

Question: {question}
Answer: {answer}

Rate the relevance on a scale of 1-5:
1 - Not relevant at all
2 - Somewhat relevant 
3 - Moderately relevant
4 - Very relevant
5 - Highly relevant and directly answers the question

Provide only the numeric score: """,
    required_vars=["question", "answer"]
)

EVALUATION_ACCURACY_PROMPT = PromptTemplate(
    template="""Evaluate the factual accuracy of the provided answer based on the given context.

Context: {context}
Question: {question}
Answer: {answer}

Rate the accuracy on a scale of 1-5:
1 - Completely inaccurate
2 - Mostly inaccurate
3 - Partially accurate
4 - Mostly accurate
5 - Completely accurate

Provide only the numeric score: """,
    required_vars=["context", "question", "answer"]
)

# Create prompt registry
PROMPT_REGISTRY = {
    "rag_system": RAG_SYSTEM_PROMPT,
    "rag_answer": RAG_ANSWER_PROMPT,
    "graph_rag_system": GRAPH_RAG_SYSTEM_PROMPT,
    "graph_rag_answer": GRAPH_RAG_ANSWER_PROMPT,
    "kg_system": KG_SYSTEM_PROMPT,
    "kg_answer": KG_ANSWER_PROMPT,
    "entity_extraction": ENTITY_EXTRACTION_PROMPT,
    "relation_extraction": RELATION_EXTRACTION_PROMPT,
    "eval_relevance": EVALUATION_RELEVANCE_PROMPT,
    "eval_accuracy": EVALUATION_ACCURACY_PROMPT
}


def get_prompt_template(name: str) -> PromptTemplate:
    """Get a prompt template by name"""
    if name not in PROMPT_REGISTRY:
        raise ValueError(f"Unknown prompt template: {name}")
    return PROMPT_REGISTRY[name]


def create_messages(
    system_prompt: str, 
    user_prompt: str, 
    assistant_prompt: str = None
) -> List[Dict[str, str]]:
    """Create message list for chat-based models"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    if assistant_prompt:
        messages.append({"role": "assistant", "content": assistant_prompt})
    
    return messages