import os
import openai
import yaml
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY") 

class PersonalityAssessor:
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
    
    def analyze_text(self, text_sample: str):
        prompt = self._create_prompt(text_sample)
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a personality assessment expert specializing in the Big Five personality traits."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Low temperature for better results
        )
        
        return response.choices[0].message.content
    
    def _create_prompt(self, example) -> str:
        one_shot_example = """
        I've been planning my vacation to Mexico for 5 months now. I've spent quite a lot of time researching
        places to visit and found many good choices. I'm excited to explore the culture and try the food, 
        though I'm a bit nervous about my Spanish since I'm still an intermediate Spanish speaker.
        I prefer to have some quiet time to myself in the evenings,but I'm looking forward 
        to meeting new people during the day. I've packed mostly everything a week in advance 
        to make sure I don't forget anything important.
        """

        one_shot_good_output = """
        Openness: 5
        Conscientousness: 5
        Extraversion: 4
        Agreeableness: 3
        Neuroticism: 4
        """
        prompt = f"""
        Please analyze the following text sample and evaluate the author on the Big Five personality traits
        (Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism).
        
        High Openness refers the writer being curious, imaginative, and enjoys exploring and investigating
        High Conscientiousness refers to the writer being responsible and well-organized.
        High Extraversion refers to the writers' sociability, talkativeness, and a passion for engaging in interpersonal and social activities. 
        High Agreeableness refers to the writer being helpful, sympathetic, friendly, and caring toward others.
        High Neuroticism refers to the writer having emotions such as anxiety, worry, and nervousness.
        
        For each trait, respond with each score from 1-5, where:
        - 1 represents very low in the trait
        - 3 represents average/neutral
        - 5 represents very high in the trait
        
        Present your analysis in a YAML format with the trait name as the key and the score as the output (without yaml tags)
        
        Example Text:
        {one_shot_example}
        
        Example Output:
        {one_shot_good_output}
        
        Text sample to analyze:
        "{example}"
        """
        return prompt

# Example usage

def parse_yaml_string(input_string):
    # Simple removal of markdown tags
    clean_string = input_string.replace("```yaml", "").replace("```", "").strip()
    return yaml.safe_load(clean_string)

princess_dict = {
    "anna": np.array([4, 3, 5, 5, 3]),
    "ariel": np.array([5, 2, 5, 4, 4]),
    "aurora": np.array([3, 4, 2, 5, 2]),
    "belle": np.array([5, 5, 3, 4, 2]),
    "cinderella": np.array([4, 5, 3, 5, 2]),
    "elsa": np.array([4, 5, 2, 4, 5]),
    "jasmine": np.array([4, 3, 4, 3, 3]),
    "merida": np.array([5, 3, 4, 2, 3]),
    "test": np.array([5, 3, 4, 2, 3]),
    "rapunzel": np.array([5, 4, 5, 5, 3]),
    "snow white": np.array([3, 4, 3, 5, 2]),
    "tiana": np.array([4, 5, 3, 4, 2])
}
    
def get_nearest_farthest_princess(example):
    assessor = PersonalityAssessor()
    results = assessor.analyze_text(example)
    user_dict = parse_yaml_string(results)
    print(user_dict)
    user_arr = np.array(list(user_dict.values()))
    
    nearest_princess = ""
    farthest_princess = ""
    nearest_score = float('inf')
    farthest_score = -1
    
    for princess_name, princess_score in princess_dict.items():
        score_diff = np.linalg.norm(user_arr - princess_score)
        if score_diff < nearest_score:
            nearest_princess = princess_name
            nearest_score = score_diff
        if score_diff > farthest_score:
            farthest_princess = princess_name
            farthest_score = score_diff
    return nearest_princess, farthest_princess, user_dict

example = """
I just returned from a spontaneous weekend trip to a music festival. 
I didn't plan much beforehand, just bought the ticket and figured 
everything else out on the spot. I spent most of my time exploring 
different stages and meeting new people - made a few friends I'm 
still texting with! I found it energizing to be in such a lively 
atmosphere, though by Sunday evening I was completely exhausted. 
The highlight was definitely convincing a group of strangers to 
join me in the front row for my favorite band. I'm already looking 
into what festivals are happening next month - life's too short to 
stay home!
"""
print(get_nearest_farthest_princess(example))