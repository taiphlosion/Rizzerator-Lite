# **Rizzerator-Lite**
A demo version of a machine learning algorithm that sends requests to a dictionary API to give confidence rating of words.


# **wordRank.ipynb**
This is the file that allowed us to develop our dataset. The basic premise of it can be summarized in one sentence: the relative context of a word can be reasonably determined by the context of its most closely related words. In this case, the goal was to assess how likely a word is to appear in a confident sentence. 

Words are not inherently confident, but we believe that certain words are especially likely to be used in a way that an average audience would perceive to be confident. Our goal was to develop a rating system for words and then use machine learning to rank related words.

## The Ranking System
Sentences in our initial corpus were ranked on a scale of 1.0 to 5.0. A score of 1.0 represents an extremely low confidence sentence (e.g. "I am the worst"), a score of 5.0 represents an extremely high confidence sentence (e.g. "I am the best"), and a score of 3.0 represents a neutral sentence. What made the process particularly difficult is that it is not easy to separate conviction from confidence. Oftentimes, an individual will speak with conviction and confidence (e.g. "I'm a great athlete"). However, there are instances when an individual speaks with high conviction and low confidence (e.g. "I'm never going to get a girlfriend).

If this assignment were to be done again, we would benefit greatly from ranking more than 1,600ish sentences. The more sentences we could manually rank, the better our model would be able to perform down the line, as each word would have a richer score with greater context. Additionally, if each group member submitted a score for each sentence in the corpus, we would be able to develop a more balanced view (albeit still biased by the views of the team) of confidence. 

Words, unless included in our list of stop words, were initially assigned a score equal to the score of the sentence that they appeared in. What does this mean? Here's an example. Let's say we have a sentence - "we'll find a way to get it done" - and this sentence has a score of 4.3. Words that are not stop words, such as "find", "way", "get", "done" would all be assigned a score of 4.3. 

Doesn't this not capture the full range of ways that a word can be used? Yes, so for each word we kept a running list of scores. Every time that word appeared again in a new sentence with a new score, that new score would be appended to the word (e.g. "big, [4.1, 3.6, 2.1]"). After going through all sentences, a word would be assigned a final score equal to the average of its scores (e.g. "big, 3.267"). The one significant weakness was that we failed to set a condition for the minimum number of scores a word needed to have in order to be assigned a final score. For example, if the word "alligator" appeared once in our corpus of sentences, and the score of the sentence it appeared in was a 5.0, the word alligator would now have a fixed score of 5. I'll admit, this doesn't make much sense. After seeing how it worked with this first iteration, we definitely learned a lot of lessons. Here's a new idea that we have:

    First, its probably better to store the word alongside a pair (sum of score, # of appearances). This would make the process of taking averages computationally less complex and, if I'm not mistaken, require less memory.

    Second, why have a fixed score from the beginning if a word is likely going to appear many times as our algorithm works through synonyms, definitions, and nearest neighbors? It seems better to keep a running sum of scores and appearances until our dictionary has grown to a size that we are satisfied with. Whenever we need to use that word's "score" to estimate the score of a related word, we could just take it's average at the time of use.

In all honesty, we weren't too concerned about the confidence scores being perfectly accurate this time around. We just wanted to get a general idea of how to solve the problem so that we could improve upon it. For the purpose of this project, which was more about creating data structures to represent our dictionary, I wanted an algorithm that cared more about getting new words into our dictionary than getting their score correct. Of course, I wanted the score to make sense in most cases, but exceptions were expected and not too frustrating.
