def evaluate_user_input(decision_topic, situation, options, constraints, confusion):
    
    score = 0
    suggestions = []

    if decision_topic and len(decision_topic.strip()) >= 10:
        score += 2
    else:
        suggestions.append("Add a clearer decision topic.")
    
    if situation and len(situation.strip()) >= 50:
        score += 3
    else:
        suggestions.append("Describe the situation in more detail.")
    
    if options and len(options.strip()) >= 20:
        score += 2
    else:
        suggestions.append("Mention at least two options you are considering.")
    
    if constraints and len(constraints.strip()) >= 20:
        score += 2  
    else:
        suggestions.append("Add constraints such as time, budget, skills, resources, or dealines.")
    
    if confusion and len(confusion.strip()) >= 20:
        score += 1  
    else:
        suggestions.append("Explain what exactly is confusing you.")
    
    if score >= 8:
        quality = "Good"
    elif score >= 5:
        quality = "Moderate"
    else:
        quality = "Weak"
    
    return {
        "score": score,
        "quality": quality,
        "suggestions": suggestions
    }