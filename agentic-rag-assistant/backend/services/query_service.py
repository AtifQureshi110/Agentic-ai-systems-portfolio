from graph.workflow import graph


def ask_question(question: str):

    output = graph.invoke( { "question": question } )

    return output["answer"]