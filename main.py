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
        similar_cities = []
        similar_countries = []
        similar_feelings = []
        similar_activities = []
        similar_foods = []

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
                similar_cities.append(f"{userB['userID']} is from a similar city ({userB['city']})")
            if country_similarity > 0.9:
                similar_countries.append(f"{userB['userID']} is from the same country as you! ({userB['country']})")
            if feeling_similarity > 0.5:
                similar_feelings.append(f"{userB['firstName']} has the same kind feeling as you ({userB['feeling']})!")
                # Adjust thresholds based on desired sensitivity
            if food_similarity > 0.5:
                similar_foods.append(f"{userB['firstName']} enjoys similar foods ({userB['favFood']})")
            if activity_similarity > 0.5:
                similar_activities.append(f"{userB['firstName']} likes similar activities ({userB['favActivity']})")

        # Compile reports
        reports[userA['userID']] = {
            "similar_cities": similar_cities,
            "similar_countries": similar_countries,
            "similar_feelings": similar_feelings,
            "similar_foods": similar_foods,
            "similar_activities": similar_activities,
        }

    return reports


users = [
    {"userID": "A", "firstName": "UserA", "city": "New York", "country": "USA", "favActivity": "playing basketball",
     "favFood": "chocolate cake", "feeling": "happy"},
    {"userID": "B", "firstName": "UserB", "city": "Los Angeles", "country": "USA", "favActivity": "swimming",
     "favFood": "sushi", "feeling": "excited"},
    {"userID": "C", "firstName": "UserC", "city": "Chicago", "country": "USA", "favActivity": "running",
     "favFood": "salad", "feeling": "content"},
    {"userID": "D", "firstName": "UserD", "city": "New York", "country": "USA", "favActivity": "playing basketball",
     "favFood": "pizza", "feeling": "happy"},
    {"userID": "E", "firstName": "UserE", "city": "Boston", "country": "USA", "favActivity": "cycling",
     "favFood": "chocolate cake", "feeling": "joyful"},
    {"userID": "F", "firstName": "UserF", "city": "San Francisco", "country": "USA", "favActivity": "hiking",
     "favFood": "burrito", "feeling": "adventurous"},
    {"userID": "G", "firstName": "UserG", "city": "New York", "country": "USA", "favActivity": "jogging",
     "favFood": "salad", "feeling": "good"},
    {"userID": "H", "firstName": "UserH", "city": "Tokyo", "country": "Japan", "favActivity": "swimming",
     "favFood": "sushi", "feeling": "excited"},
    {"userID": "I", "firstName": "UserI", "city": "Kyoto", "country": "Japan", "favActivity": "meditating",
     "favFood": "matcha cake", "feeling": "peaceful"},
    {"userID": "J", "firstName": "UserJ", "city": "London", "country": "UK", "favActivity": "watching football",
     "favFood": "fish and chips", "feeling": "energetic"},
    {"userID": "K", "firstName": "UserK", "city": "london", "country": "United Kingdom",
     "favActivity": "watching football", "favFood": "fish and chips", "feeling": "excied"},
    {"userID": "L", "firstName": "UserL", "city": "Shenzhen", "country": "China", "favActivity": "violin",
     "favFood": "chocolate", "feeling": "tired"},
    {"userID": "M", "firstName": "UserM", "city": "Beijing", "country": "CHINA", "favActivity": "piano",
     "favFood": "Dumplings", "feeling": "sad"},
    {"userID": "N", "firstName": "UserN", "city": "Cambridge", "country": "UK", "favActivity": "cook",
     "favFood": "Tart", "feeling": "ok"},
    {"userID": "O", "firstName": "UserO", "city": "Oxford", "country": "uk", "favActivity": "baking", "favFood": "Rice",
     "feeling": "fine"},
    {"userID": "P", "firstName": "UserP", "city": "shanghai", "country": "china", "favActivity": "reading",
     "favFood": "Burger", "feeling": "crying"},
    # Add more users if needed
]

for user in users:
    user['country'] = normalize_country_name(user['country'])

# Analyze similarities
reports = analyze_user_similarities(users)

# Print report for a specific user, say 'J'
print(reports['J'])
