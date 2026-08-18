import json,random,sys
from pathlib import Path
from datetime import date,timedelta
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from backend.stores.sqlite_store import insert_startups,initialize
from backend.stores.neo4j_store import Neo4jStore
random.seed(42)
NAMES=["NovaHealth AI","FinPilot","AgroVision","CyberShield","LegalMind","EduVerse","RetailIQ","FleetFlow","ClimateCore","MedAssist","CloudLedger","InsureAI","FactorySense","TravelMesh","FoodLens","BuildWise","EnergyPulse","SecureStack","PropTechX","TalentGrid","SupplyMind","VoiceCare","QuantumOps","MarketMuse AI","AutoRoute","GreenCart","DataForge","CareBridge","PayStream","VisionWorks"]
SECTORS=["HealthTech","FinTech","ClimateTech","SaaS","Cybersecurity","RetailTech"]
FOUNDERS=["Priya Shah","Arjun Mehta","Neha Kapoor","Rohan Patel","Aisha Khan","Kabir Joshi","Maya Desai","Vikram Rao","Ananya Iyer","Dev Malhotra"]
INVESTORS=["Sequoia","Accel","Lightspeed","Peak XV","Blume","Matrix Ventures"]
PARTNERS=["HealthCorp","CloudWorks","EnterpriseHub","Global Retail","DataLink","Metro Labs"]
POS=["Customers praised the product reliability and measurable time savings.","The company announced expansion into new enterprise markets.","The founder reported strong renewal rates and growing demand."]
MIX=["Customers liked the product but several reported integration friction.","The company has strong demand although implementation can be complex.","Press coverage was positive while noting competitive pressure."]
NEG=["Several customers reported reliability problems and delayed support.","A market review raised concerns about pricing and weak differentiation.","The company faces intense competition and uncertain retention."]

def make(i,name):
    founder=FOUNDERS[i%len(FOUNDERS)]
    investors=[INVESTORS[i%len(INVESTORS)],INVESTORS[(i+2)%len(INVESTORS)]]
    competitors=[NAMES[(i+1)%len(NAMES)],NAMES[(i+7)%len(NAMES)]]
    partners=[PARTNERS[i%len(PARTNERS)],PARTNERS[(i+1)%len(PARTNERS)]]
    if i%3==0:
        growth,runway,funding,revenue,margin=65+i%25,18+i%10,15+i,6+i*.2,62+i%10; tone=POS
    elif i%3==1:
        growth,runway,funding,revenue,margin=35+i%20,10+i%8,8+i*.6,4+i*.15,52+i%8; tone=MIX
    else:
        growth,runway,funding,revenue,margin=8+i%18,5+i%7,4+i*.3,2.5+i*.1,42+i%8; tone=NEG
    return {"id":f"startup_{i:03d}","name":name,"sector":SECTORS[i%len(SECTORS)],
      "founded_year":2018+i%6,"revenue_musd":round(revenue,2),"revenue_growth_pct":growth,
      "total_funding_musd":round(funding,2),"valuation_musd":round(funding*(4.5+i%3),2),
      "burn_rate_musd":round(max(.18,revenue*.055),2),"runway_months":runway,"employees":35+i*7,
      "gross_margin_pct":margin,"customer_count":40+i*35,"founders":[founder],
      "investors":investors,"competitors":competitors,"partners":partners,
      "documents":[
        {"source":"press_release","date":str(date(2025,1,10)+timedelta(days=i*7)),
         "text":f"{name} announced a strategic update in its {SECTORS[i%len(SECTORS)]} market. {tone[0]}"},
        {"source":"customer_review","date":str(date(2025,3,5)+timedelta(days=i*5)),
         "text":f"A customer review of {name} said: {tone[1]}"},
        {"source":"founder_interview","date":str(date(2025,5,12)+timedelta(days=i*3)),
         "text":f"In a founder interview, {founder} discussed growth, retention and competition. {tone[2]}"}
      ]}

def main():
    data=[make(i,n) for i,n in enumerate(NAMES)]
    (ROOT/"data/startups.json").write_text(json.dumps(data,indent=2),encoding="utf-8")
    initialize(); insert_startups(data)
    try:
        g=Neo4jStore(); g.verify(); g.clear(); g.insert_startups(data)
        n,e=g.count_nodes_edges(); g.close(); print(f"Neo4j nodes={n}, edges={e}")
    except Exception as exc:
        print(f"Neo4j population skipped: {type(exc).__name__}: {exc}")
        print("Start Neo4j and rerun to populate graph.")
    print(f"Generated startups={len(data)}")
    print("SQLite rows populated.")
    print("Text documents=",sum(len(x["documents"]) for x in data))
if __name__=="__main__": main()
