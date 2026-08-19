import json,sys
from pathlib import Path

from backend.config import DATASET_PATH,CHUNK_SIZE,CHUNK_OVERLAP
from backend.stores.faiss_store import FAISSStore

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))

def chunks(text):
    out=[]; start=0

    while start<len(text):
        end=min(len(text),start+CHUNK_SIZE);out.append(text[start:end])
        if end==len(text):break
        start=end-CHUNK_OVERLAP

    return out

def main():

    data=json.loads(DATASET_PATH.read_text(encoding="utf-8")); rows=[]

    for s in data:
        for di,d in enumerate(s["documents"]):
            for ci,t in enumerate(chunks(d["text"])):
                rows.append({"chunk_id":f"{s['id']}_{di}_{ci}","startup":s["name"],
                             "source":d["source"],"date":d["date"],"text":t})

    FAISSStore().build(rows);print(f"FAISS/BM25 chunks={len(rows)}")

if __name__=="__main__":main()
