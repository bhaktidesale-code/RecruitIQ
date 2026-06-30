import gzip
import json
import csv

# 1. Define the "Traps" and Scoring Logic
def calculate_score(candidate):
    score = 0.0
    
    # TRAP 1: Honeypots
    # Filter out candidates with "expert" skills but < 1 month experience
    for skill in candidate.get("skills", []):
        if skill["proficiency"] == "expert" and skill.get("duration_months", 0) < 1:
            return -1.0 # Immediate disqualification
            
    # TRAP 2: Keyword Stuffers
    # If they have 50+ skills listed, they are likely keyword stuffing
    if len(candidate.get("skills", [])) > 50:
        score -= 2.0
        
    # SIGNAL 1: Availability (The JD specifically asks for this)
    signals = candidate.get("redrob_signals", {})
    if signals.get("open_to_work_flag"):
        score += 2.0
    
    # SIGNAL 2: Engagement (Response rate is a high-quality predictor)
    response_rate = signals.get("recruiter_response_rate", 0)
    score += (response_rate * 2.0)
    
    # LOGIC: Experience fit (JD asks for 5-9 years)
    exp = candidate.get("profile", {}).get("years_of_experience", 0)
    if 5 <= exp <= 9:
        score += 3.0
        
    return score

# 2. Process Data
def main():
    ranked = []
    
    # Load and process the compressed file
    with open("candidates.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            cand = json.loads(line)
            
            # Get the score
            score = calculate_score(cand)
            
            # Keep only viable candidates
            if score >= 0:
                ranked.append({
                    "id": cand["candidate_id"],
                    "score": score,
                    "reasoning": f"Experience of {cand['profile']['years_of_experience']} yrs with {len(cand['skills'])} skills."
                })
    
    # Sort and slice
    ranked.sort(key=lambda x: x["score"], reverse=True)
    top_100 = ranked[:100]
    
    # Write output
    with open("TEAM_PRAGYAAN.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for i, cand in enumerate(top_100):
            writer.writerow([cand["id"], i + 1, cand["score"], cand["reasoning"]])

if __name__ == "__main__":
    main()