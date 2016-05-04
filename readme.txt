The goal of the project is to take students' responses to LSA and use those responses as a predictor for their performance in the class.

The main component of the programming, is to create a script that analyzes the students' responses to questions. To do so, several metrics were used:

The current metrics to analyze an answer are:

Text length

Vocabulary usage: Dr. Gilchrist supplied a list of around 275 vocabulary words that would be used throughout the course. The student's vocavulary usage score is determined by counting the number of vocab words they use in the responses.

Conjunctive words used: such as "Because, In fact, Furthermore, moreover." The thought is that a person would not use these phrases unless they were following it up with reasoning

Number of capital letters used: Capital letters indicate the use of proper nouns, which indicate a specific knowledge. For example, words such as: DNA, and RNA might fit this purpose.

Similarity of response to instructor: This measures the number of words that match what the instructor also used. Commonly used words such as "the, of, there, a" are not counted.

Reading Level: The Coleman-Liau Index to determine the reading level of a response.

Reflecive words used: There is a list of reflective words that indicate a student spent time reflecting on their answer. Examples of these include: 'attention', 'answer', 'answers', 'concept', 'concepts', 'effort', 'lecture'

The questions analyzed were:
Explain a concept
Explain a phenonmenon
State a challenging concept and why it was difficult
Give a comment on your knowledge basis for a concept


After the metrics were created, the next portion of the project was to determine the appropriate weights for these metrics. To do so, a program inspired by supervised machine learning was created that tries a set of weights, and increases and decreases them one at a time. The total LSA Score is then compared to the final grade in the course to determine the correlation. If adjusting a weight increases the correlation, the algorithm will keep increasing or decreaseing that metric until progress stops.

Note that this machine learning program was ran on each question, because each question has potentially different ideal weights. Furthermore, it was ran on both cumulative and average LSA scores. For cumulative scores, the student's scores for a specific question were simply added together, whereas in average LSA scores, that total was then divided by the number of LSAs the student completed. 

Other useful questions in the LSAs are:
Numerical knowledge basis: In this question, students were asked to rank their understanding level on a topic from 0-5 by .5 increments.
Importance of topics: In this question, students were asked to rank the importance of various topics and their responses were then compared to the instructor.

Two other predictors used are:
The score on the pre-test, which is a test of 25 questions taken at the beginning of the course
The number of LSAs the students submit


These 8 indpendant variables will be used to predict a student's performance in a course.


EBI responses were also analyzed, but their correlations to final grades were too low to be considered useful
