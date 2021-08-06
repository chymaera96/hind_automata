# hind_automata
 A probabilistic automata framework for generating melodies in Hindustani classical raga. In addition, the generated automata can be used to produce melodies in particular ragas (or combination of ragas) using the GUI. It must be noted, however, that combining interpolating between the automata of multiple ragas produces more instances of disharmony. 
 
 ## Installation
 
 ```shell
 git clone https://github.com/chymaera96/hind_automata.git
 pip install -r requirements.txt
 
```

## Running the GUI

The GUI is built using the ```tkinter``` library. It uses RGB allows of an image to generate the ratio required for interpolating between ragas. Depending on the RGB values of the point selected, the framework produces a MIDI file by combining the following three ragas: Bhupali, Yaman and Bhairavi. 
```shell
cd hind_automata/scripts
python midi_on_click.py
```

NOTE: Enlarge the image window box to full-screen before clicking on the image to select parameters. The GUI can be run using any image that has been added to the ```scripts/images/``` directory.

## Training the Automata

There are two complexities of automaton training in this framework: unigrams and bigrams. In either of the cases, the a (or a combination of) pitch note(s) forms the probabilistic nodes of the automaton. The following Google Colab notebooks are self explanatory and can be used to train the automata based on the data provided.

* Unigram framework:[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/chymaera96/hind_automata/blob/main/Notebooks/Hindustani_automata_unigram.ipynb)

* Bigram framework: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/chymaera96/hind_automata/blob/main/Notebooks/Hindustani_automata_bigram.ipynb)

For best results, use the first notebook which goes the unigram route. The notebooks use the melody sequence datasets provided in ```Datasets``` directory. In order to run the training, upload the ```.dat``` file from the directory to the Colab notebook. The ```.aut``` files produced contain the pickled probabilistic automata.  


