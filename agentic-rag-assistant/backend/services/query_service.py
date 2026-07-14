from graph.workflow import graph
# Import the pre-built LangGraph workflow object, which encapsulates 
# the full RAG pipeline: retrieval, reasoning, and answer generation.

# Actually gets the answer.
# (Original comment — clarifies this function is where the real work happens, 
# as opposed to a route just forwarding the request.)


# Actually gets the answer.

def ask_question(question: str):
# Main service function. Takes a raw user question as input.

    output = graph.invoke( { "question": question } )
    # Run the question through the LangGraph workflow. 
    # The graph likely handles: embedding the question, retrieving relevant 
    # chunks from the vector DB, and generating an answer via an LLM.
    # `output` is expected to be a dict containing multiple workflow results.

    return output["answer"]
    # Extract and return only the final answer string from the graph's output, 
    # discarding intermediate data (retrieved chunks, reasoning steps, etc.) 
    # that the caller doesn't need.
