# import requests
# from config import BACKEND_URL


# def check_source(source: str):

#     print("SOURCE SENT TO API:", source)

#     response = requests.post(
#         f"{BACKEND_URL}/ingest/check-source",
#         json={
#             "source": source
#         }
#     )

#     print("API RESPONSE:", response.json())

#     return response.json()


# def ingest_source(source: str, force_update: bool = False):

#     response = requests.post(
#         f"{BACKEND_URL}/ingest",
#         json={
#             "source": source,
#             "force_update": force_update
#         }
#     )

#     return response.json()


# import requests


# BACKEND_URL = "http://localhost:8000"



# def ask_ai(question):

#     response = requests.post(

#         f"{BACKEND_URL}/query",

#         json={
#             "question": question
#         }

#     )


#     return response.json()

import requests


BACKEND_URL = "http://localhost:8000"



def check_source(source):

    response = requests.post(
        f"{BACKEND_URL}/ingest/check-source",
        json={
            "source": source
        }
    )

    return response.json()



def ingest_source(source, force_update=False):

    response = requests.post(
        f"{BACKEND_URL}/ingest",
        json={
            "source": source,
            "force_update": force_update
        }
    )

    return response.json()



def ask_ai(question: str):

    response = requests.post(
        f"{BACKEND_URL}/query",
        json={
            "question": question
        }
    )

    response.raise_for_status()

    return response.json()