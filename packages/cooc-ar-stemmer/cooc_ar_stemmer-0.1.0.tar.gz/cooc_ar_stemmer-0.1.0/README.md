# cooc_ar_stemmer
A stemmer for the Arabic language

Based on the work:
@ARTICLE {iskanderakhmetovalexandrpakirinaualiyevaalexandergelbukh2020, 
author = "Iskander Akhmetov, Alexandr Pak, Irina Ualiyeva, Alexander Gelbukh", 
title = "Highly Language-Independent Word Lemmatization Using a Machine-Learning Classifier", 
journal = "Computacion y Sistemas", 
year = "2020", 
volume = "24", 
number = "3", 
pages = "1353-1364", 
month = "sep" }

## Usage:
```
import cooc_ar_stemmer.ar_stem as cas
cas.stem_it('شطط')

# Output: 'شط'

# You can also provide a list of words:
cas.stem_it(['شطط', 'ضحي'])

# Output: ['شط', 'ضحى']
```
