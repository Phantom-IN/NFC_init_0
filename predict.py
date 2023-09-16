from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_text(text):
    candidate_labels = [
        'finance', 'defence', 'agriculture', 'environment', 'health', 'water',
        'science', 'prime minister', 'information and broadcasting', 'technology', 'family', 'others'
    ]
    return classifier(text, candidate_labels)


if __name__ == "__main__":
    sequence_to_classify = "Success Story: Swachh Bharat Mission"
    result = classify_text(sequence_to_classify)
    print(result)
