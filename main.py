# FastAPI backend for Lead Intent Scorer
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import csv
import io
import os
import openai
from scoring import rule_score
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-...your-key-here...")
openai.api_key = OPENAI_API_KEY

def map_intent_to_points(intent: str) -> int:
	if intent.lower() == "high":
		return 50
	if intent.lower() == "medium":
		return 30
	if intent.lower() == "low":
		return 10
	return 0

async def get_ai_intent_and_reasoning(lead: dict, offer: dict) -> tuple:
	prompt = f"""
You are an expert sales assistant. Given the following product/offer and lead details, classify the lead's buying intent as High, Medium, or Low, and explain your reasoning in 1-2 sentences.

Product/Offer:
Name: {offer.get('name', '')}
Value Props: {', '.join(offer.get('value_props', []))}
Ideal Use Cases: {', '.join(offer.get('ideal_use_cases', []))}

Lead:
Name: {lead.get('name', '')}
Role: {lead.get('role', '')}
Company: {lead.get('company', '')}
Industry: {lead.get('industry', '')}
Location: {lead.get('location', '')}
LinkedIn Bio: {lead.get('linkedin_bio', '')}

Respond in JSON with keys 'intent' and 'reasoning'.
"""
	try:
		response = await openai.ChatCompletion.acreate(
			model="gpt-3.5-turbo",
			messages=[{"role": "user", "content": prompt}],
			max_tokens=150,
			temperature=0.2,
		)
		content = response.choices[0].message.content
		import json
		result = json.loads(content)
		intent = result.get("intent", "Low")
		reasoning = result.get("reasoning", "No reasoning provided.")
		return intent, reasoning
	except Exception as e:
		return "Low", f"AI error: {str(e)}"

app = FastAPI(title="Lead Intent Scorer API")

# Allow CORS for local/frontend testing
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# In-memory storage
offer_data = {}
leads_data = []
results_data = []

@app.post("/offer")
async def post_offer(offer: dict):
	"""Accept product/offer details as JSON."""
	offer_data.clear()
	offer_data.update(offer)
	return {"message": "Offer received", "offer": offer_data}

@app.post("/leads/upload")
async def upload_leads(file: UploadFile = File(...)):
	"""Accept a CSV file with lead data."""
	if not file.filename.endswith('.csv'):
		raise HTTPException(status_code=400, detail="File must be a CSV.")
	content = await file.read()
	decoded = content.decode('utf-8')
	reader = csv.DictReader(io.StringIO(decoded))
	leads = [row for row in reader]
	if not leads:
		raise HTTPException(status_code=400, detail="No leads found in CSV.")
	leads_data.clear()
	leads_data.extend(leads)
	return {"message": f"{len(leads)} leads uploaded."}


@app.post("/score")
async def score_leads():
	"""Run scoring pipeline on uploaded leads."""
	results_data.clear()
	for lead in leads_data:
		rule_points = rule_score(lead, offer_data)
		intent, reasoning = await get_ai_intent_and_reasoning(lead, offer_data)
		ai_points = map_intent_to_points(intent)
		results_data.append({
			**lead,
			"intent": intent,
			"score": rule_points + ai_points,
			"reasoning": reasoning,
			"rule_points": rule_points,
			"ai_points": ai_points
		})
	return {"message": f"{len(results_data)} leads scored."}

@app.get("/results")
async def get_results():
	"""Return scored leads as JSON array."""
	return JSONResponse(content=results_data)


# (Bonus) Export results as CSV
from fastapi.responses import StreamingResponse
import pandas as pd

@app.get("/results/csv")
async def export_results_csv():
	if not results_data:
		raise HTTPException(status_code=404, detail="No results to export.")
	df = pd.DataFrame(results_data)
	stream = io.StringIO()
	df.to_csv(stream, index=False)
	stream.seek(0)
	return StreamingResponse(stream, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=results.csv"})
