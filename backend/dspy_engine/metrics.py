VALID_VERDICTS={"INVEST","PASS"}
VALID_RISK={"LOW","MEDIUM","HIGH"}
BANNED={"maybe","as an ai","i cannot determine"}

def judge_metric(example,prediction,trace=None,**kwargs):
    def g(k,d=None): return getattr(prediction,k,d)
    try: confidence=int(g("confidence",-1))
    except: return False
    if str(g("verdict","")).strip().upper() not in VALID_VERDICTS: return False
    if not 0<=confidence<=100: return False
    if str(g("financial_risk","")).strip().upper() not in VALID_RISK: return False
    if str(g("market_risk","")).strip().upper() not in VALID_RISK: return False
    if str(g("network_strength","")).strip().upper() not in VALID_RISK: return False
    reasoning=str(g("reasoning","")).strip()
    if not reasoning: return False
    if any(x in reasoning.lower() for x in BANNED): return False
    return True

def bad_output_example():
    return {"verdict":"MAYBE","confidence":137,"financial_risk":"UNKNOWN",
            "market_risk":"LOW","network_strength":"HIGH","reasoning":""}

def validate_dict(d):
    class O: pass
    o=O()
    for k,v in d.items(): setattr(o,k,v)
    return judge_metric(None,o)
