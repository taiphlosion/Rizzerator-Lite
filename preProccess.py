import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def clean(text):
    text = text.lower() # to lowercase
    text = re.sub(r"@\S+", "", text) # remove mentions
    text = re.sub("http[s]?\://\S+","",text) # remove links
    text = re.sub(r"[0-9]", "", text) # remove numbers
    text = re.sub(r"won\'t", "will not", text) #checks for contractions
    text = re.sub(r"can\'t", "can not", text)
    text = re.sub(r"n\'t", " not", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'s", " is", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'t", " not", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'m", " am", text)
    text = re.sub(r"[$&+,:;=?@#|'<>.^*()%!-]", "", text) # remove special characters
    tokens = text.split()
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    filtered_text = ' '.join(filtered_tokens)

    return filtered_text