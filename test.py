from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import argparse

def load_model_and_tokenizer(model_name):
    model = AutoModelForSequenceClassification.from_pretrained(model_name, ignore_mismatched_sizes=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

def process_input(input_text, tokenizer, max_length=64):
    return tokenizer(input_text, return_tensors='pt', padding=True, truncation=True, max_length=max_length)

def predict_personality(model, encoded_input):
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        outputs = model(**encoded_input)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return predictions[0].tolist()

def print_predictions(predictions, trait_names):
    for trait, score in zip(trait_names, predictions):
        print(f"{trait}: {score:.4f}")

def main():
    parser = argparse.ArgumentParser(description="Predict personality traits from text.")
    parser.add_argument("--input", type=str, required=True, help="Input text or path to text file")
    parser.add_argument("--model", type=str, default="KevSun/Personality_LM", help="Model name or path")
    args = parser.parse_args()

    model, tokenizer = load_model_and_tokenizer(args.model)

    # Check if input is a file path or direct text
    if args.input.endswith('.txt'):
        with open(args.input, 'r', encoding='utf-8') as file:
            input_text = file.read()
    else:
        input_text = args.input

    encoded_input = process_input(input_text, tokenizer)
    predictions = predict_personality(model, encoded_input)

    trait_names = ["Agreeableness", "Openness", "Conscientiousness", "Extraversion", "Neuroticism"]
    print_predictions(predictions, trait_names)

if __name__ == "__main__":
    main()