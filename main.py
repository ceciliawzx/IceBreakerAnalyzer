from typing import Any, Dict

from sentence_transformers import SentenceTransformer
import torch
from nomarlize_countries import normalize_country_name

# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')


# Function to compute embeddings
def compute_embeddings(texts):
    return model.encode(texts)


# Function to calculate cosine similarity
def cosine_similarity(embeddings1, embeddings2):
    cos_sim = torch.nn.CosineSimilarity(dim=0)
    similarity_scores = [cos_sim(torch.tensor(a), torch.tensor(b)) for a, b in zip(embeddings1, embeddings2)]
    return similarity_scores


# Function to analyze user similarities
def analyze_user_similarities(users):
    cities = [user['city'] for user in users]
    countries = [user['country'] for user in users]
    feelings = [user['feeling'] for user in users]
    foods = [user['favFood'] for user in users]
    activities = [user['favActivity'] for user in users]

    # Compute embeddings
    city_embeddings = compute_embeddings(cities)
    country_embeddings = compute_embeddings(countries)
    feeling_embeddings = compute_embeddings(feelings)
    food_embeddings = compute_embeddings(foods)
    activity_embeddings = compute_embeddings(activities)

    reports = {}

    for i, userA in enumerate(users):
        similar_cities = {}
        similar_countries = {}
        similar_feelings = {}
        similar_activities = {}
        similar_foods = {}

        for j, userB in enumerate(users):
            if i == j:
                continue  # Skip self-comparison

            # Calculate similarity scores
            city_similarity = cosine_similarity([city_embeddings[i]], [city_embeddings[j]])[0]
            country_similarity = cosine_similarity([country_embeddings[i]], [country_embeddings[j]])[0]
            feeling_similarity = cosine_similarity([feeling_embeddings[i]], [feeling_embeddings[j]])[0]
            food_similarity = cosine_similarity([food_embeddings[i]], [food_embeddings[j]])[0]
            activity_similarity = cosine_similarity([activity_embeddings[i]], [activity_embeddings[j]])[0]

            # TODO: adjust thresholds based on testing
            # -1 (strong different) <= similarity <= 1 (strong similar)
            if city_similarity > 0.8:  # Higher threshold for cities and countries
                similar_cities[userB['userID']] = f"{userB['userID']} is from a similar city! ({userB['city']})"
            if country_similarity > 0.9:
                similar_countries[
                    userB['userID']] = f"{userB['userID']} is from the same country as you! ({userB['country']})"
            if feeling_similarity > 0.5:
                similar_feelings[userB['userID']] = f"{userB['firstName']} feels similar as you! ({userB['feeling']})!"
                # Adjust thresholds based on desired sensitivity
            if food_similarity > 0.5:
                similar_foods[userB['userID']] = f"{userB['firstName']} enjoys similar foods! ({userB['favFood']})"
            if activity_similarity > 0.5:
                similar_activities[
                    userB['userID']] = f"{userB['firstName']} likes similar activities! ({userB['favActivity']})"

        # Compile reports
        reports[userA['userID']] = {
            "similar_cities": similar_cities,
            "similar_countries": similar_countries,
            "similar_feelings": similar_feelings,
            "similar_foods": similar_foods,
            "similar_activities": similar_activities,
        }

    return reports


def generate_reports(users) -> dict[Any, dict[str, dict[Any, str]]]:
    for user in users:
        user['country'] = normalize_country_name(user['country'])
    reports = analyze_user_similarities(users)
    return reports


# Return all reports for a specific user
def get_reports_for_user(reports, userID):
    return reports.get(userID, {})


# Return report of userID2 for userID1
def get_report_for_user(reports, userID1, userID2):
    # Fetch the report for userID1
    report_for_user1 = reports.get(userID1, {})

    report_for_user2 = {}

    # Iterate through each category in reports for userID1
    for category, details in report_for_user1.items():
        # Check if userID2 has an entry within this category
        if userID2 in details:
            # If so, add the specific report for userID2 to the consolidated report
            report_for_user2[category] = details[userID2]

    # Return the consolidated report for userID2
    return report_for_user2
