from graph.workflow import graph

# Actually gets the answer.

def ask_question(question: str):
    output = graph.invoke( { "question": question } )
    return output["answer"]