from slm import *
from glob import glob


context_length = 3

def get_model(context_length):
    #tokenizer = WhitespaceTokenizer()
    #tokenizer = CharacterTokenizer()
    #tokenizer = SpaceTokenizer()
    tokenizer = Gpt2Tokenizer()

    predictor = FrequencyTablePredictor(context_length)

    model = LanguageModel(
        tokenizer=tokenizer,
        predictor=predictor
    )

    return model

# Usage starts here

def generate(model, initial_context, end_token):
    #initial_context = tokens[:context_length]
    generator = model.generate(initial_context)
    yield next(generator)
    
    for token in generator:
        if token == end_token:
            return
        yield token

model = get_model(context_length)
end_token = model.tokenizer("\2")[0]

def get_possible_starts(freq_table, end_token):
    # ------- FOR DEMO -------
    possible_starts = []

    for k,v in freq_table.items():
        if k[0] == end_token:
            possible_starts.append(k)
        
    # -----------------------
    return possible_starts

def get_initial_context(possible_starts):
    return list(random.choice(possible_starts))

print(end_token)

for file in glob("./r9k/res/7296*"):
    text = open(file)
    text = text.read()
    tokens = model.tokenizer(text)
    model.train(tokens)

possible_starts = get_possible_starts(model.predictor.follower_table, end_token)

while (True):
    initial_context = get_initial_context(possible_starts)
    generated_tokens = generate(model, initial_context, end_token)
    generated_text = model.tokenizer.decode(generated_tokens)
    print(generated_text)
    input()
    

