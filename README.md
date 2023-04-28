# **Rizzerator-Lite**
A demo version of a machine learning algorithm that sends requests to a dictionary API to give confidence rating of words, then uses a word's k-nearest neighbors to assign confidence rating to new words.


# **wordRank.ipynb**
This is the file that allowed us to develop our dataset. The basic premise of it can be summarized in one sentence: the relative context of a word can be reasonably determined by the context of its most closely related words. In this case, the goal was to assess how likely a word is to appear in a confident sentence. 

Words are not inherently confident, but we believe that certain words are especially likely to be used in a way that an average audience would perceive to be confident. Our goal was to develop a rating system for words and then use machine learning to rank related words.

## The Ranking System
Sentences in our initial corpus were ranked on a scale of 1.0 to 5.0. A score of 1.0 represents an extremely low confidence sentence (e.g. "I am the worst"), a score of 5.0 represents an extremely high confidence sentence (e.g. "I am the best"), and a score of 3.0 represents a neutral sentence. Stop words that the group felt were neutral were assigned a score of 3.0 immediately. What made the process particularly difficult is that it is not easy to separate conviction from confidence. Oftentimes, an individual will speak with conviction and confidence (e.g. "I'm a great athlete"). However, there are instances when an individual speaks with high conviction and low confidence (e.g. "I'm never going to get a girlfriend). How does one separate confidence and conviction? This depends on the individual ranker. Some people may naturally associate conviction for confidence, whereas others may see through the speaker and recognize that the content of their language reflects a lack of confidence. Its a tricky balance, but the best approach is to crowdsource as many opinions as one can get.

If this assignment were to be done again, we would benefit greatly from ranking more than 1,600ish sentences. The more sentences we could manually rank, the better our model would be able to perform down the line, as each word would have a richer score with greater context. Additionally, if each group member submitted a score for each sentence in the corpus, we would be able to develop a more balanced view (albeit still biased by the views of the team) of confidence. 

Words, unless included in our list of stop words, were initially assigned a score equal to the score of the sentence that they appeared in. What does this mean? Here's an example. Let's say we have a sentence - "we'll find a way to get it done" - and this sentence has a score of 4.3. Words that are not stop words, such as "find", "way", "get", "done" would all be assigned a score of 4.3. 

Doesn't this not capture the full range of ways that a word can be used? Yes, so for each word we kept a running list of scores. Every time that word appeared again in a new sentence with a new score, that new score would be appended to the word (e.g. "big, [4.1, 3.6, 2.1]"). After going through all sentences, a word would be assigned a final score equal to the average of its scores (e.g. "big, 3.267"). The one significant weakness was that we failed to set a condition for the minimum number of scores a word needed to have in order to be assigned a final score. For example, if the word "alligator" appeared once in our corpus of sentences, and the score of the sentence it appeared in was a 5.0, the word alligator would now have a fixed score of 5. I'll admit, this doesn't make much sense. After seeing how it worked with this first iteration, we definitely learned a lot of lessons. Here's a new idea that we have:

    First, its probably better to store the word alongside a pair (sum of score, # of appearances). This would make the process of taking averages computationally less complex and, if I'm not mistaken, require less memory.

    Second, why have a fixed score from the beginning if a word is likely going to appear many times as our algorithm works through synonyms, definitions, and nearest neighbors? It seems better to keep a running sum of scores and appearances until our dictionary has grown to a size that we are satisfied with. Whenever we need to use that word's "score" to estimate the score of a related word, we could just take it's average at the time of use.

In all honesty, we weren't too concerned about the confidence scores being perfectly accurate this time around. We just wanted to get a general idea of how to solve the problem so that we could improve upon it. For the purpose of this project, which was more about creating data structures to represent our dictionary, I wanted an algorithm that cared more about getting new words into our dictionary than getting their score correct. Of course, I wanted the score to make sense in most cases, but exceptions were expected and not too frustrating.

## Ranking By Using Synonyms
By this point, after ranking our sentence words in the process outlined above, we had built a dictionary of 2,617 words. Not bad, but we need 100,000. 

The next idea was pretty straightforward: synonyms are likely to have a reasonably similar confidence score. Now, we recognize that there is color in words. If "amazing" is the word we have extracted from our dictionary, and we pull its synonyms, we may get words like "tremendous", "great", and "impressive." These words, while similar, have different associations and are likely to be used in slightly different contexts. So how do we find color between synonyms? We look to the definition of the synonym. If the definition of the synonym has a greater confidence score than the original word (I'll call it the OG word from now on) from our dictionary, then we estimated that the synonym was likely a bit more confident than the OG word. 

Now, we didn't know exactly how much more confident the synonym was, so we added a little bit of noise to our algorithm to balance out the distribution of scores. We are still not sure if this was the most reasonable solution but, again, we cared more about how the scores would play into our data structures. Anyways, back to the idea of noise. What does it mean to add noise? Here's the simple equation:
    If the definition score > OG word score, then take the OG word score (ex: 4.1) and add to it a random number in the range of 0.0 to 0.2, (ex: 0.1, giving the synonym a final score of 4.1 + 0. 1 = 4.2).

    If the definition score < OG word score, do the same thing but with a range of -0.2 to 0.0 for the noise.

Unknown words encountered in our definition were treated as neutral when calculating the confidence score of the definition. Would it have been better to take the average of only the known words instead of doing this? We are not sure. These unknown definition words were then given a score in the range of the score of the synonym. This was almost definitely not a reasonable way to score the unknown definition word but, as we stated, the goal was to get a lot of words scored fast. 

The one wrinkle left out is that we had a limited number of times that we could extract synonyms and definitions, because obtaining these required calls to the Words API https://rapidapi.com/dpventures/api/wordsapi. We paid $10 for 25,000 API calls and we were not going to pay anymore money. So, we built what can be thought of as a backup engine. 

Think of an airplane; if one of its engines goes out, the thing needs to keep flying. The backup engine, then, was a k-nearest neighbors type algorithm to find the neighbors of a word in our dictionary. I won't go too much into detail on this part of the algorithm because it wasn't one of our best ideas yet (we improved upon it later in the Jupyter file). However, here's a general outline of how it works:
    1. Download the pretrained GloVe model trained on a Twitter dataset
        1a. This model was chosen because it was believed it would have somewhat emotionally colored speech. It had the drawback of slang words and many                misspelled words.
    2. Take a word from our dictionary which already had a score (aka the OG word)
    3. Find the OG words k-nearest neighbors (first level neighbors)
    4. For each of the first level neighbors, find its k-nearest neighbors (second level neighbors)
    5. Use the scored second level neighbors, take their average, and use it to approximate a score for their respective first  level neighbor
    6. For each unknown second level neighbor, find their k-nearest neighbors (third level neighbors) and try to do the same thing as above
    7. By this point, if we can't figure out the score for a word, don't go any deeper, but use the score of the first level or second level neighbor to            assign a score to the unknown third level neighbor

Again, not the most accurate, but it definitely finds a lot of new words every iteration. However, as I said above, it wasn't really used as I terminated the algorithm when we got close to our API limit in favor of the next approach.

Overall, this part of our code allowed us to build the dictionary from 2,617 words to a little over 28,000 words, all with scores.


## Reputation: Ranking Words Using Its Neighbors

