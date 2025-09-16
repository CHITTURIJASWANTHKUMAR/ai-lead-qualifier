# Lead Intent Scorer Backend

## 🚀 Live API Base URL
Live API base URL for testing:

`https://ai-lead-qualifier-kvge.onrender.com/`

# Lead Intent Scorer Backend

## Overview
This backend service scores B2B leads for buying intent using rule-based logic and AI (OpenAI GPT-3.5/4). It exposes APIs to upload offer details, leads (CSV), and returns scored results.

## Setup

1. **Clone the repo**
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
3. **Set your OpenAI API key:**
	```bash
	export OPENAI_API_KEY=sk-...your-key...
	```
4. **Run the server:**
	```bash
	uvicorn main:app --reload
	```

## Docker

Build and run with Docker:
```bash
docker build -t lead-intent-scorer .
docker run -e OPENAI_API_KEY=sk-...your-key... -p 8000:8000 lead-intent-scorer
```

## API Usage

### 1. POST /offer
Submit product/offer details (JSON):
```json
{
  "name": "AI Outreach Automation",
  "value_props": ["24/7 outreach", "6x more meetings"],
  "ideal_use_cases": ["B2B SaaS mid-market"]
}
```

### 2. POST /leads/upload
Upload a CSV file with columns:
`name,role,company,industry,location,linkedin_bio`

### 3. POST /score
Run scoring pipeline on uploaded leads.

### 4. GET /results
Get scored leads as JSON array.

### 5. GET /results/csv
Export results as CSV file.

## Rule Logic
- **Role relevance:** decision maker (+20), influencer (+10), else 0
- **Industry match:** exact ICP (+20), adjacent (+10), else 0
- **Data completeness:** all fields present (+10)
- **AI Layer:** Uses OpenAI to classify intent (High=50, Medium=30, Low=10) and provide reasoning.

## Example cURL
```bash
# Submit offer
curl -X POST http://localhost:8000/offer -H "Content-Type: application/json" -d '{"name":"AI Outreach Automation","value_props":["24/7 outreach","6x more meetings"],"ideal_use_cases":["B2B SaaS mid-market"]}'

# Upload leads
curl -X POST http://localhost:8000/leads/upload -F 'file=@leads.csv'

# Run scoring
curl -X POST http://localhost:8000/score

# Get results
curl http://localhost:8000/results

# Export results as CSV
curl -OJ http://localhost:8000/results/csv
```

## Tests
Run unit tests for the rule layer:
```bash
pytest tests/test_rule_layer.py
```

## Deployment
Deployable on any cloud (Render, Railway, Vercel, Heroku, etc). Set `OPENAI_API_KEY` as an environment variable.

---
## Submission Requirements Checklist

- [x] Proper commit history (no single commit dump)
- [x] Well-structured code with inline comments & documentation
- [x] README includes setup steps, API usage examples, rule logic, and prompt explanation
- [ ] Deployed backend (add your live API base URL above)

---
For questions, contact: [Your Name]
# ai-lead-qualifier
