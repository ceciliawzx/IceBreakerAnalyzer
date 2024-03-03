from transformers import pipeline

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def classify_interests(interests, categories):
    classified_interests = {}
    for interest in interests:
        # Perform zero-shot classification
        result = classifier(interest, candidate_labels=categories)
        # Get the top category
        top_category = result['labels'][0]
        classified_interests[interest] = top_category
    return classified_interests
