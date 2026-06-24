from data_pipeline.ingestion import ingest_document


result = ingest_document("https://panaversity.org/")

doc = result["metadata"]
chunks = result["chunks"]
vectors = result["vectors"]


print("\n===== METADATA =====")

print("SOURCE:", doc["source"])
print("TYPE:", doc["type"])
print("TOKENS:", doc["tokens"])


print("\n===== FIRST 2000 CHARACTERS =====")

print(doc["content"][:2000])

print("\nTOTAL LENGTH:")
print(len(doc["content"]))

print("\n===== CHUNK INFO =====")

print("TOTAL CHUNKS:",len(chunks))

if chunks:
    print("\nFIRST CHUNK:")
    print(chunks[0][:1000])

print("\n===== EMBEDDING INFO =====")

print("EMBEDDINGS CREATED:",len(vectors))

if vectors:
    print("\nEMBEDDING DIMENSION:")
    print(len(vectors[0]["embedding"]))