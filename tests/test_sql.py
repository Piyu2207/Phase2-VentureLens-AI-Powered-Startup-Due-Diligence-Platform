from backend.stores import sqlite_store
def test_sql_roundtrip(tmp_path,monkeypatch):
    monkeypatch.setattr(sqlite_store,"SQLITE_PATH",tmp_path/"test.db")
    sqlite_store.initialize()
    sqlite_store.insert_startups([{"id":"1","name":"TestCo","sector":"SaaS","founded_year":2022,
      "revenue_musd":2.5,"revenue_growth_pct":70,"total_funding_musd":5,"valuation_musd":20,
      "burn_rate_musd":.2,"runway_months":20,"employees":20,"gross_margin_pct":70,"customer_count":50}])
    assert sqlite_store.get_startup("TestCo")["revenue_musd"]==2.5
