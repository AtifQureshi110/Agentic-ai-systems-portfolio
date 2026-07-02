"""
Agentic RAG Assistant - Entry Point
Author: Muhammad Atif

Usage:
    Set RUN_INGESTION = True to ingest new sources, then set back to False.
    If a source already exists in Pinecone, user is asked BEFORE any processing begins.
"""

# ================================================================
# INGESTION CONFIG
# ================================================================

RUN_INGESTION = True

# Web Sources
URLS = [
    # "https://panaversity.org/",
    # "https://panaversity.org/courses",
    # "https://panaversity.org/certifications",
    # "https://agentfactory.panaversity.org/",
]

# Local Files (PDF, DOCX, TXT)
FILES = [
    # "files/project_overview12.docx",
    "files/RAG original paper by Meta.pdf",
]

# ================================================================
# INGESTION PIPELINE
# ================================================================

if RUN_INGESTION:

    from data_pipeline.ingestion import ingest_document, normalize_source
    from vectorstore.pinecone_client import get_all_sources

    print("\nChecking existing sources in Pinecone...\n")
    existing_sources = get_all_sources()

    def ingest_source(source: str):

        normalized = normalize_source(source)

        # CHECK FIRST - before any loading, cleaning, chunking, or embedding
        if normalized in existing_sources:
            print(f"\nAlready in Pinecone: {normalized}")
            user_input = input("Do you want to update it? (yes/no): ").strip().lower()

            if user_input != "yes":
                print(f"Skipped: {normalized}")
                return

            print(f"Updating: {normalized}")

        else:
            print(f"\nNew source detected: {normalized}")

        # PIPELINE RUNS ONLY IF NEW OR USER CONFIRMED UPDATE
        try:
            result = ingest_document(source)
            doc    = result["metadata"]
            chunks = result["chunks"]

            if not chunks:
                print(f"Warning: No chunks extracted from {normalized}")
                return

            print(f"Done")
            print(f"SOURCE   : {doc.get('source')}")
            print(f"TYPE     : {doc.get('type')}")
            print(f"TOKENS   : {doc.get('tokens')}")
            print(f"CHUNKS   : {len(chunks)}")
            print(f"UPSERTED : {result['inserted']}")

            if chunks:
                print(f"PREVIEW  : {chunks[0][:200]}")

        except Exception as e:
            print(f"Failed: {source} | {e}")

    # Process Web Sources
    if URLS:
        print("\nProcessing Web Sources...\n")
        for url in URLS:
            ingest_source(url)

    # Process Local Files
    if FILES:
        print("\nProcessing Local Files...\n")
        for file in FILES:
            ingest_source(file)

    print("\nIngestion complete.\n")

# ================================================================
# AGENT — QUERY EXECUTION
# ================================================================

# ---------------- RUN AGENT ----------------
from graph.workflow import graph


question = (

    # "How many certification levels does the Agentic AI Architect Program have?"
    # "What is the primary tool used in the Agentic AI Architect Program?"
    # "How many courses are in the Agentic AI Architect Program?"
    # "What is the capstone credential of the program?"
    # "Who is the Agentic AI Business Strategist Program designed for?"
    # "How many exams are in the full Architect program including CCA-F?"
    # "What does CCA-F stand for?"
    # "What is the exam format at Panaversity?"

    # "Compare the Agentic AI Architect Program vs the Agentic AI Business Strategist Program"
    # "What topics are covered at Level 3 Factory Builder certification"
    # "What is the difference between Level 1 and Level 2 of the program?"
    # "Explain the full certification ladder from Level 1 to Level 4"
    # "What technologies does a student learn across all levels?"
    # "How does the CCA-F exam work and who administers it?"
    # "Compare learning model vs universities"
    # =================
    # "What is Panaversity?"
    # "Compare learning model vs universities"
    # "What programs does it offer?"
    # "can you tell me all name of the teachers at panaversity? i need only the names"
    # "Explain architecture and teaching approach"
    # "How does it prepare students?"
    # "Does Muhammad Qasim work at Panaversity as teaching staff or in another major department? If yes, what is his role?"
    # "can you tell me all name of the teachers at panaversity? i need only the names"
    # "can you tell about Zia Khan?"


    # ======================= pdf rag questio simple 
    # "What are the two main components of a RAG model, and what role does each play?"
    # "What is the non-parametric memory in this paper, and what is the parametric memory?"
    # "What retriever and generator does the original RAG paper use?"
    # "Name three tasks the paper evaluates RAG on."

    # medium 
    # "What's the difference between RAG-Sequence and RAG-Token, and when would you prefer one over the other?"
    # "Why does the paper keep the document encoder (BERT_d) frozen during training instead of updating it jointly with the retriever's query encoder?"
    # "How does *index hot-swapping* work, and why is it a key advantage of RAG over closed-book models like T5?"
    # "In the ablation study, why does BM25 outperform the dense retriever specifically on FEVER, while dense retrieval wins everywhere else?"
    # "What does it mean that the retrieved document z is treated as a *latent variable,* and how is it marginalized out at inference time?"

    #complex 
    # "RAG-Token can attend to a different document per generated token, giving it more flexibility — so why does RAG-Sequence actually produce more diverse generations (Table 5), and what does that imply about the tradeoff between flexibility and diversity in decoding strategy?"
    # "The paper shows *Thorough Decoding* vs *Fast Decoding* as two ways to approximate p(y|x) for RAG-Sequence. If you were implementing an agentic RAG loop in LangGraph where latency matters, how would you decide which approximation to use, and could you approximate this behavior with a node that conditionally re-scores generations?"
    # "RAG achieves 11.8 percentage accuracy on NQ even when the correct answer isn't in any retrieved document — meaning the parametric memory is compensating for retrieval failure. In a LangGraph agent, how would you design a node/edge structure to explicitly detect this situation (retrieval likely failed) and route to a fallback strategy, rather than silently relying on the generator to *know* the answer?"
    # "This paper marginalizes over retrieved documents jointly with generation (soft, differentiable). Most agentic RAG systems today do retrieval as a discrete, non-differentiable tool call before generation. What capabilities does the original RAG architecture have that a typical *retrieve-then-generate* LangGraph agent loses, and how might you compensate for that loss using graph structure instead of gradients (e.g., multi-query retrieval, re-ranking, reflection loops)?"
    # "The paper notes retrieval can *collapse* for tasks like story generation, where the generator learns to ignore retrieved documents entirely. If you were building an agentic RAG system that must decide whether to retrieve at all for a given query, what signals would you build into a LangGraph router node to detect *this query doesn't need retrieval* versus forcing a retrieval collapse-like failure mode?"
)

output = graph.invoke({

    "question": question

})

print("\n===== Question =====\n")

print(question)

print("\n===== ANSWER =====\n")

print(
    output["answer"])