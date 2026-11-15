import re
from app.triage.predict import predict
from app.rag import retriever as R
from app.agent import tools

def extract_order_id(text):
	m = re.search(r"order[^0-9]*(\d+)",text.lower())
	if m:
		return int(m.group(1))
	m = re.search(r"\b(\d{3,6})\b", text)
	return int(m.group(1)) if m else None

def _result(
		status,
		intent,
		conf,
		reply,
		order_id=None,
		citation=None):
	return{
		"status":status,
		"intent":intent,
		"conf":round(conf,3),
		"reply":reply,
		"order_id":order_id,
		"citation":citation}
def _escalate(db,customer_id,text,intent,conf,reply):
	tools.escalate_to_human(db,customer_id,text)






















