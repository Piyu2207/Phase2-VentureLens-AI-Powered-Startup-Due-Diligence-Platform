import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import dspy
from backend.config import DATASET_PATH,DSPY_COMPILED_PATH
from backend.dspy_engine.config import configure_student,make_teacher
from backend.dspy_engine.module import DueDiligenceModule
from backend.dspy_engine.metrics import judge_metric
from backend.retrieval.parallel import parallel_retrieve

def examples():
    data=json.loads(DATASET_PATH.read_text(encoding="utf-8"));out=[]
    for s in data[:24]:
        r,_=parallel_retrieve(s["name"],f"{s['name']} financial health customers competition investment risk")
        gold="INVEST" if s["revenue_growth_pct"]>=55 and s["runway_months"]>=15 else "PASS"
        out.append(dspy.Example(
            sql_context=r["sql"].context,faiss_context=r["faiss"].context,graph_context=r["graph"].context,
            verdict=gold,confidence=85,
            financial_risk="LOW" if s["runway_months"]>=15 else "HIGH",
            market_risk="MEDIUM",network_strength="HIGH",
            reasoning="Gold label follows the documented synthetic evaluation rule."
        ).with_inputs("sql_context","faiss_context","graph_context"))
    return out

def main():
    configure_student();teacher=make_teacher();student=DueDiligenceModule()
    opt=dspy.BootstrapFewShot(metric=judge_metric,max_bootstrapped_demos=4,max_labeled_demos=4,max_rounds=1,max_errors=8)
    compiled=opt.compile(student=student,teacher=student,trainset=examples(),teacher_settings={"lm":teacher})
    DSPY_COMPILED_PATH.parent.mkdir(parents=True,exist_ok=True)
    compiled.save(str(DSPY_COMPILED_PATH))
    print(f"Saved compiled state: {DSPY_COMPILED_PATH}")
if __name__=="__main__":main()
