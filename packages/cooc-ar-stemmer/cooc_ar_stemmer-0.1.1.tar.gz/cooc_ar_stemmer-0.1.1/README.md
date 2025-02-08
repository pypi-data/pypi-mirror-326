# cooc_ar_stemmer
A stemmer for the Arabic language

Comparison to other stemmers for the Arabic language:

| Stemmer                          | Test Accuracy  |
|----------------------------------|---------------|
| **This work**                    |               |
| cooc_ar_stemmer             | **0.7469**    |
| **Other stemmers**                |               |
| Lucene Arabic Analyzer           | **0.5510**    |
| Shereene Khoja Stemmer           | 0.5494        |
| ISRIStemmer                      | 0.5397        |
| ArabicProcessingCog              | 0.2361        |
| Arabic-Stemming-Toolkit AST      | 0.2358        |
| Tashaphyne: Arabic Light Stemmer | 0.2332        |
| Assem's Arabic Light Stemmer     | 0.2310        |
| FARASA                           | 0.2303        |
| Al Khalil Morpho Sys Stemmer     | 0.2195        |
| Qutuf                            | 0.1923        |


Based on the work: \
@ARTICLE {iskanderakhmetovalexandrpakirinaualiyevaalexandergelbukh2020, \
author = "Iskander Akhmetov, Alexandr Pak, Irina Ualiyeva, Alexander Gelbukh", \
title = "Highly Language-Independent Word Lemmatization Using a Machine-Learning Classifier", \
journal = "Computacion y Sistemas", \
year = "2020", \
volume = "24", \
number = "3", \
pages = "1353-1364", \
month = "sep" }\

## Installation:
```
pip install cooc_ar_stemmer
```

## Usage:
```
import cooc_ar_stemmer.ar_stem as cas
cas.stem_it('شطط')

# Output: 'شط'

# You can also provide a list of words:
cas.stem_it(['شطط', 'ضحي'])

# Output: ['شط', 'ضحى']
```

The model files can be downloaded at https://drive.google.com/file/d/1VRqygWHz81UqF6e5zVceP37lhMax90n0/view?usp=sharing