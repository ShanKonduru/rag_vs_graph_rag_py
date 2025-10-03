AI & QE

QE FOR AI
& 
AI IN QE

AGENDA

Q E   F O R   A I

C H A L L E N G E S

E M E R G I N G   S T R A T E G I E S

T E C H N I C A L   D E M O

Q & A

I N A D E Q U A T E   Q E  
P R A C T I C E S ,  
M E T H O D S ,  
S T R A T E G I E S   A N D  
T E C H N I Q U E S

QE FOR AI

QE CHALLENGES

• Testing nondeterministic systems.

• Testing explainability and interpretability.

• Testing dynamic data and evolving AI systems.

• Simulating real-world complexities.

• Ensuring bias and fairness.

• Defining relevant success metrics.

• Addressing critical ethical considerations and alignment.

EMERGING 
QE 
STRATEGIES

S H I F T   T O W A R D S   M O R E   A D A P T I V E  
A N D   A I - A W A R E   Q E  
M E T H O D O L O G I E S .

QE STRATAGIES

• Metric-Driven Evaluation

• Comprehensive Test Case Design

• Continuous Monitoring and Evaluation

• Bias and Fairness Assessment

• Explainability and Interpretability Evaluation

• Human-in-the-Loop Evaluation

• Robustness and Adversarial Testing

METRICS & MEASUREMENT FRAMEWORK

Effective metrics to use while validating AI systems.

•

Faithfulness

• Measures the factual consistency of the generated answer with the retrieved context.

• Answer Relevancy

• Assesses how well the generated answer addresses the query.

Context Precision

• Evaluates the signal-to-noise ratio of the retrieved context; relevance of retrieved documents.

•

•

•

•

Context Recall

Context Relevancy

Context Entity Recall

• Noise Sensitivity

•

Context Utilization

• Measures if the retrieved context contains all the necessary information to answer the question.

• Gauges the relevancy of the retrieved context to the question.

• Measures the recall of entities present in both ground truths and retrieved contexts.

• Measures the robustness of the RAG system to irrelevant information in the context.

• Measures how much of the retrieved context is used to generate the answer.

CONCEPTUAL 
DEMO

M E T R I C S   D R I V E N  
A U T O M A T I C  
A P P R O A C H   T O  
V A L I D A T E   A I  
S Y S T E M S

RAG EVALUATION – BLOCK DIAGRAM

LangChain

1

Convert to Chunks

Embeddings

3

Store in 
Vector Database

FAISS

Vector Store
Knowledge Base

LangChain

2

Create Embeddings

RAG Block Diagram

RAG Evaluation Block Diagram

4

Asks a Questions

10

5

Search Relevant 
Information

User gets Response 
and Evaluation 
Metrics

Retrieved Relevant 
Information

6

Docs, PDFs, Txts, 
PPTs, Mds

Chunks

Retrieval Augmented Generation (RAG) 
metrics
Context Precision
Context Recall
Context Entities Recall
Noise Sensitivity
Response Relevancy
Faithfulness
Multimodal Faithfulness
Multimodal Relevance

Evaluate 
LLM output

8

7

Get the Response

Produce Metrics

9

TOOLS AND TECHNOLOGIES

Python Dependencies:

1.

2.

3.

4.

5.

tiktoken

pandas

streamlit 

pytest

Dotenv

LLM Dependencies:

1.

langchain

2.

3.

4.

ragas

faiss-cpu

langchain-openai

LLM Access:

1.

2.

OpenAI API 

(gpt-3.5-turbo, gpt-4)

Vector Database

1.

FAISS

Q&A

T I M E   F O R   Y O U R   B R I L L I A N T  
Q U E S T I O N S !

THANK YOU

• Shan Konduru

• Vice President, Global Delivery @ Coforge

• +91 70933 85859 

• +1 368 886 7461

• https://www.linkedin.com/in/shankonduru/

• https://github.com/ShanKonduru

