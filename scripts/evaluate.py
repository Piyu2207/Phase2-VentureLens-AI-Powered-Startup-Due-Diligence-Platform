import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from backend.config import DATASET_PATH,DSPY_COMPILED_PATH
from backend.dspy_engine.inference import synthesize
from backend.dspy_engine.metrics import bad_output_example,validate_dict
from backend.retrieval.parallel import parallel_retrieve

def main():
    data=json.loads(DATASET_PATH.read_text(encoding="utf-8"));name=data[-1]["name"]
    r,lat=parallel_retrieve(name,f"Should an investor invest in {name}?")
    pred,mode=synthesize(r["sql"].context,r["faiss"].context,r["graph"].context)
    result={"held_out_entity":name,"mode":mode,"parallel_latency_ms":lat,
            "retrieval_ok":{k:v.ok for k,v in r.items()},
            "prediction":{k:getattr(pred,k,None) for k in ["verdict","confidence","financial_risk","market_risk","network_strength","reasoning"]},
            "compiled_state_exists":DSPY_COMPILED_PATH.exists(),
            "judge_bad_output_rejected":not validate_dict(bad_output_example())}
    out=ROOT/"artifacts/evaluation/baseline_vs_compiled.json"
    out.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
    print("Run once before compilation and once after compilation for baseline-vs-compiled evidence.")
if __name__=="__main__":main()
