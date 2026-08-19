from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentence = "how do I install this"
vector = model.encode(sentence)

print(type(vector))
print(vector.shape)
print(vector[:10])  # just the first 10 numbers, the full thing is long