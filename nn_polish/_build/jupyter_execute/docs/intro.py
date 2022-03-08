#!/usr/bin/env python
# coding: utf-8

# # Wstęp

# ## Cel wykładu

# Celem kursu jest wyłożenie podstaw wszechobecnych sieci neuronowych z pomocą [Pythona](https://www.python.org/) {cite}`barry2016head,matthes2019python,guttag2016`. Zarówno kluczowe pojęcia sieci neuronowych, jak i programy ilustrujące są wyjaśniane na bardzo podstawowym poziomie, niemal „licealnym”. Kody, bardzo proste, zostały szczegółowo opisane. Ponadto są utworzone bez użycia specjalistycznych bibliotek wyższego poziomu dla sieci neuronowych, co pomaga w lepszym zrozumieniu przedstawionych algorytmów i pokazuje, jak programować je od podstaw. 

# ``` {admonition} Dla kogo jest ta książka?
# :class: important
# 
# **Czytelnik może być zupełnym nowicjuszem, tylko w niewielkim stopniu zaznajomionym z Pythonem (a właściwie każdym innym językiem programowania) i Jupyterem.**
# ```

# Materiał obejmuje takie klasyczne zagadnienia, jak perceptron i jego najprostsze zastosowania, nadzorowane uczenie z propagacją wsteczną do klasyfikacji danych, uczenie nienadzorowane i klasteryzacja, sieci samoorganizujące się Kohonena oraz sieci Hopfielda ze sprzężeniem zwrotnym. Ma to na celu przygotowanie niezbędnego gruntu dla najnowszych i aktualnych postępów (nie omówionych tutaj) w sieciach neuronowych, takich jak uczenie głębokie, sieci konwolucyjne, sieci rekurencyjne, generatywne sieci przeciwników, uczenie ze wzmacnianiem itp.
# 
# W trakcie kursu nowicjuszom zostanie delikatnie przemycone kilka podstawowych programów w Pythonie. W kodach znajdują się objaśnienia i komentarze.

# ```{admonition} Ćwiczenia
# :class: warning
# Na końcu każdego rozdziału proponujemy kilka ćwiczeń, których celem jest zapoznanie czytelnika z poruszanymi tematami i kodami. Większość ćwiczeń polega na prostych modyfikacjach/rozszerzeniach odpowiednich fragmentów materiału wykładowego.
# ```

# ```{admonition} Literatura
# :class: note
# 
# Podręczników i notatek do wykładów poświęconych zagadnieniom poruszanym na tym kursie jest niezliczona ilość, stąd autor nie będzie próbował przedstawiać nawet niepełnego spisu literatury. Przytaczamy tylko pozycje, na które może spojrzeć bardziej zainteresowany czytelnik. 
# ```
# Z prostotą jako drogowskazem, wybór tematów był inspirowany szczegółowymi wykładami [Daniela Kerstena](http://vision.psych.umn.edu/users/kersten/kersten-lab/courses/Psy5038WF2014/IntroNeuralSyllabus.html) w programie Mathematica, z internetowej książki [Raula Rojasa](https://page.mi.fu-berlin.de/rojas/neural/) (dostępna również w wersji drukowanej {cite}`feldman2013neural`) oraz z punktu widzenia **fizyków** (jak ja!) z {cite}`muller2012neural`. 

# ## Inspiracja biologiczna

# Inspiracją do opracowania matematycznych modeli obliczeniowych omawianych w tym kursie jest struktura biologiczna naszego układu nerwowego {cite}`kandel2012principles`. Centralny układ nerwowy (mózg) zawiera ogromną liczbę ($\sim 10^{11}$) [neuronów](https://human-memory.net/brain-neurons-synapses/), które można postrzegać jako maleńkie  elementarne procesory. Otrzymują one sygnał poprzez **dendryty**, a jeśli jest on wystarczająco silny, jądro decyduje (obliczenie jest wykonane tutaj!) „wystrzelić” sygnał wyjściowy wzdłuż **aksonu**, gdzie jest on następnie przekazywany przez zakończenia aksonów do dendrytów innych neuronów. Połączenia aksonowo-dendryczne (połączenia **synaptyczne**) mogą być słabe lub silne, modyfikując przekazywany bodziec. Co więcej, siła połączeń synaptycznych może się zmieniać w czasie ([reguła Hebba](https://en.wikipedia.org/wiki/Hebbian_theory) mówi nam, że połączenia stają się silniejsze, jeśli są używane wielokrotnie). W tym sensie neuron jest „programowalny”.

# :::{figure-md} neuron-fig
# <img src="images/neuron-structure.jpg" width="450px">
# 
# Biologiczny neuron ([https://training.seer.cancer.gov/anatomy/nervous/tissue.html](https://training.seer.cancer.gov/anatomy/nervous/tissue.html)).
# :::

# We may ask ourselves if the number of neurons in the brain should really be termed so "huge" as usually claimed. Let us compare it to the computing devices with memory chips. The number of $10^{11}$ neurons roughly corresponds to the number of transistors in a 10GB memory chip, which does not impress us so much, as these days we may buy such a device for 2\$ or so.
# 
# Moreover, the speed of traveling of the nerve impulses, which is due to electrochemical processes, is not impressive, either. Fastest signals, such as those related to muscle positioning, travel at speeds up to 120m/s (the myelin sheaths are essential to achieve them). The touch signals reach about 80m/s, whereas pain is transmitted only at comparatively very slow speeds of 0.6m/s. This is the reason why when you drop a hammer on your toe, you sense it immediately, but the pain reaches your brain with a delay of ~1s, as it has to pass the distance of ~1.5m. On the other hand, in electronic devices the signal travels along the wires at speeds of the order of the speed of light, $\sim 300000{\rm km/s}=3\times 10^{8}{\rm m/s}$!
# 
# For humans, the average [reaction time](https://backyardbrains.com/experiments/reactiontime) is 0.25s to a visual stimulus, 0.17s to an audio stimulus, and 0.15s to a touch. Thus setting the threshold time for a false start in sprints at 0.1s is safely below a possible reaction of a runner. These are extremely slow reactions compared to electronic responses. 
# 
# 
# Based on the energy consumption of the brain, one can estimate that on the average a cortical neuron [fires](https://aiimpacts.org/rate-of-neuron-firing/) about once per 6 seconds. Likewise, it is unlikely that an average cortical neuron fires more than once per second. Multiplying the firing rate by the number of all the cortical neurons, $\sim 1.6 \times 10^{10}$, yields about $3 \times 10^{9}$ firings/s in the cortex, or 3GHz. This is the rate of a typical processor chip! Hence if the firing is identified with an elementary calculation, the thus defined power of the brain is comparable to that of a standard computer processor. 
# 
# The above facts might indicate that, from a point of view of naive comparisons with silicon-based chips, the human brain is nothing so special. So what is it that gives us our unique abilities: amazing visual and audio pattern recognition, thinking, consciousness, intuition, imagination? The answer is linked to an amazing architecture of the brain, where each neuron (processor unit) is connected via synapses to, on the average, 10000 (!) other neurons. This feature makes it radically different and immensely more complicated than the architecture consisting of a control unit, processor, and memory in our computers (the [von Neumann machine](https://en.wikipedia.org/wiki/Von_Neumann_architecture) architecture). There, the number of connections is of the order of the number of bits of the memory. In contrast, there are about $10^{15}$ synaptic connections in the human brain. As mentioned, the connections may be "programmed" to get stronger or weaker. If, for the sake of a simple estimate, we approximated the connection strength by just two states of a synapse, 0 or 1, the total number of combinatorial configurations of such a system would be $2^{10^{15}}$ - a humongous number. Most of such configuration, of course, never realize in practice, nevertheless the number of possible configuration states of the brain, or the "programs" it can run, is truly immense.

# In recent years, with developing powerful imaging techniques, it became possible to map the connections in the brain with unprecedented resolution, where single nerve bundles are visible. The efforts are part of the [Human Connectome Project](http://www.humanconnectomeproject.org), with the ultimate goal to map one-to-one the human brain architecture. For the much simpler fruit fly, the [drosophila connectome project](https://en.wikipedia.org/wiki/Drosophila_connectome) is very well advanced. 

# :::{figure-md} Connectome-fig
# <img src="images/brain.jpg" width="280px">
# 
# White matter fiber architecture of the brain (from the Human Connectome Project [humanconnectomeproject.org](http://www.humanconnectomeproject.org/gallery/))
# :::

# ```{important}
# The "immense connectivity" feature, with zillions of neurons serving as parallel elementary processors, makes the brain a completely different computational device from the [Von Neumann machine](https://en.wikipedia.org/wiki/Von_Neumann_architecture) (i.e. our everyday computers).
# ```

# ## Feed-forward networks 

# The neurophysiological research of the brain provides important guidelines for mathematical models used in artificial neural networks (**ANN**s). Conversely, the advances in algorithmics of ANNs frequently bring us closer to understanding of how our "brain computer" may actually work! 
# 
# 
# The simplest ANNs are the so called **feed forward** networks, exemplified in {numref}`ffnn-fig`. They consist of an **input** layer (black dots), which just represents digitized data, and layers of neurons (colored blobs). The number of neurons in each layer may be different. The complexity of the network and the tasks it may accomplish increase, naturally, with the number of layers and the number of neurons. 
# 
# In the remaining part of this section we give, in a rather dense format, a bunch of important definitions: 
# 
# Networks with one layer of neurons are called **single-layer** networks. The last layer (light blue blobs) is called the **output layer**. In multi-layer (more than one neuron layer) networks the neuron layers preceding the output layer (purple blobs) are called **intermediate layers**. If the number of layers is large (e.g. as many as 64, 128, ...), we deal with the recent "ground-breaking" **deep networks**.
# 
# Neurons in various layers do not have to function the same way, in particular the output neurons may act differently from the others.
# 
# The signal from the input travels along the links (edges, synaptic connections), indicated with arrows, to the neurons in subsequent layers. In feed-forward networks, as the one in {numref}`ffnn-fig`, it can only move forward (from left to right in the figure): from the input to the first neuron layer, from the first to the second, and so on until the output is reached. No going backward to preceding layers, or parallel propagation among the neurons of the same layer, are allowed. This would be a **recurrent** feature that we touch upon in section {ref}`lat-lab`. 
# 
# As we describe in detail in the following chapters, the traveling signal is appropriately **processed** by the neurons, hence the device carries out a computation: input is being transformed into output. 
# 
# In the sample network of {numref}`ffnn-fig` each neuron from a preceding layer is connected to each neuron in the following layer. Such ANNs are called **fully connected**. 

# :::{figure-md} ffnn-fig
# <img src="images/feed_f.png" width="300px">
# 
# A sample feed-foward fully connected artificial neural network. The colored blobs represent the neurons, and the edges indicate the synaptic connections. The signal propagates starting from the input (black dots), via the neurons in subsequent intermediate (hidden) layers (purple blobs), to the output layer (light blue blobs). The strength of the connections is controled by weights (hyperparameters) assigned to the edges.
# :::

# As we will discuss in greater detail shortly, each edge (synaptic connection) in the network has a certain "strength" described with a number called **weight** (the weights are also termed **hyperparameters**). Even very small fully connected networks, such as the one of {numref}`ffnn-fig`, have very many connections (here 30), hence contain a lot of hyperparameters. Thus, while sometimes looking innocuously, ANNs are in fact very complex multi-parametric systems. Moreover, a crucial feature here is an inherent nonlinearity of the neuron responses, as we discuss in chapter {ref}`MCP-lab`.

# ## Why Python

# The choice of  [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) for the little codes of this course needs almost no explanation. Let us only quote [Tim Peters](https://en.wikipedia.org/wiki/Tim_Peters_(software_engineer)): 
# 
# - Beautiful is better than ugly.
# - Explicit is better than implicit.
# - Simple is better than complex.
# - Complex is better than complicated.
# - Readability counts.
# 
# 
# According to [SlashData](https://developer-tech.com/news/2021/apr/27/slashdata-javascript-python-boast-largest-developer-communities/), there are now over 10 million developers in the world using Python, just second after JavaScript (~14 million). In particular, it proves very practical in applications to ANNs.

# ### Imported packages

# Throughout this course we use some standard Python library packages for the numerics, plotting, etc. As stressed, we do not use any libraries specifically dedicated to neural networks. Each lecture's notebook starts with the inclusion of some of these libraries:

# In[1]:


import numpy as np              # numerical
import statistics as st         # statistics
import matplotlib.pyplot as plt # plotting
import matplotlib as mpl        # plotting
import matplotlib.cm as cm      # contour plots 

from mpl_toolkits.mplot3d.axes3d import Axes3D   # 3D plots
from IPython.display import display, Image, HTML # display imported graphics


# ```{admonition} **neural** package
# Functions created during this course which are of repeated use, are placed in the private library package **neural**, described in appendix {ref}`app-lab`. 
# ```

# Assuming the package is in the relative subdirectory **lib_nn**, it is imported in the following way:

# In[2]:


import sys                  # system 
sys.path.append('./lib_nn') # path to the lecture's package

from neural import *        # import the lecture's package


# See appendix {ref}`app-lab` for further details.

# ```{note} 
# For brevity of presentation, some redundant (e.g. imports of libraries) or inessential pieces of the code are present only in the downloadable source Jupyter notebooks, and are not included/repeated in the book. This makes the text more concise and readable.
# ```
