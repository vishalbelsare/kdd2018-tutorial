#%%
import markdown
from IPython.core.display import display, HTML
def md(str):
    display(HTML(markdown.markdown(str + "<br />")))

#%%
md("""
# Higher-Order Data Analytics for Temporal Network Data


## 2.1 Temporal Network Analysis and Visualisation in `pathpy`

**Ingo Scholtes**  
Data Analytics Group  
Department of Informatics (IfI)  
University of Zurich  


**August 22 2018**

### Introduction to the `TemporalNetwork` class

So far, we have considered the `Paths` class, which is useful if you directly have access to path statistics in your data. In the last exploration, we have also seen examples for data that contain path statistics that can be modelled using higher-order model. These examples include clickstream data, origin-destination statistics in transportation networks, passenger trajectories, or other **large collections of short, ordered sequences of symbols**.

In this session, we will expand this view towards more general temporal network data, i.e. temporal data on networks that allow us to establish ordered sequences of nodes or edges. High-resolution time series network data, where edges carry fine-grained time stamps, are a particularly important class of data that can be studied using higher-order network models. Here we will specifically consider examples for dynamic social network data, such as time-stamped E-Mail exchanges, or social contact patterns recorded via electronic sensors.

Due to the practical importance of such data `pathpy` provides special support for the analysis of such temporal network data via the class `TemporalNetwork`. It is suitable for data capturing time-stamped edges $(v, w, t)$ instantaneously occurring at discrete time stamps $t$. Let us start by creating an empty instance of this class.

<span style="color:red">**TODO:** Import the package `pathpy` and rename it to `pp`. Create a new instance of the class `TemporalNetwork` and print a summary of the instance.</span>
""")

#%% In [None]


#%%
md("""
We see that this instance stores two fundamental objects: nodes $v$ and time-stamped edges $(v, w, t)$. Let us add some example edges to this instance. 

<span style="color:red">**TODO:** Use the `add_edge` function to add six (directed) time-stamped edges $(a,b, 1), (b, a, 3), (b, c, 3), (d, c, 4), (c, d, 5), (c, b, 6)$ and print the result.</span>
""")

#%% In [None]


#%%
md("""
In the example above we used integer timestamps, which we can see as **discrete time units**. This is a particularly simple type of timestamp, but `pathpy` also supports arbitrary string timestamp formats. Let us try this in an example.

<span style="color:red">**TODO:** Create a new `TemporalNetwork` instance `t_realtime` and add three time-stamped edges with string timestamps in the format "YYYY-MM-DD HH:mm:SS". Print the resulting instance and print all time-stamped edges.</span>
""")

#%% In [None]


#%%
md("""
We see that `pathpy` automatically converts the timestamps into second-based UNIX timestamps. For custom time-formats, we can set a custom `timestamp_format` parameter that will be used in the conversion. After this conversion, all time units will be in seconds (see e.g. the min/max inter-event time).

Just like other `pathpy` objects, we can directly embed interactive visualisations of a `TemporalNetwork` in `jupyter`. Let us try this with outr first toy example `t`.

<span style="color:red">**TODO:** Visualise the `TemporalNetwork` instance `t` by writing the instance variable in an empty `jupyter` cell.</span>
""")

#%% In [None]


#%%
md("""
Using the default parameters, the visualisation is a little bit too fast for the human eye. Luckily, we can again use the generic `pp.visualisation.plot` function to pass a `style` for the visualisation. We can use all parameters that we used to style static networks, plus additional parameters that influence temporal aspects of the visualisation. 

Of particular importance are the `parameters` `ms_per_frame` and `ts_per_frame`. The first one specifies how many time units will be shown in a single frame of the visualisation. With this, we could somewhat compress the visualisation, by showing multiple timestamps in a single frame. This is useful for generating coarse-grained temporal visualisations of high-resolution temporal network data. The second parameter `ms_per_frame` adjusts the target frame rate of the visualisation by setting how many milliseconds each frame should be displayed. 

Two more parameters will influence the force-directed layout algorithm, that is used to position nodes in the network. In a temporal network, the question is which time-stamped edges should be taken into account for the force-calculation at a given time stamp `t`. If we only consider the currently active edges, the layout will change too fast to follow interesting structures. If we consider all edges at every time step, the node positions will be static, despite the dynamics of the edges. In real data, we want to specify a time window around the current time stamp within which edges are taken into account in the force-directed layout calculation. We can do this by setting the number of timestamps to consider via the `look_ahead` and `look_behind` parameters. 

Finally, we can also style active and inactive nodes and edges individually, e.g. changing the color or size of nodes in timestamps where an interaction occurs. 

<span style="color:red">**TODO:** Create a visualisation where a single timestamp is shown per frame, and each frame is shown for 2 seconds. For the force-directed layout, consider edges active up to two time units before and after the current timestamp. Increase the thickness of active egdes, compared to inactive edges. </span>
""")

#%% In [None]


#%%
md("""
Again, note that this visualisation is interactive, i.e. you can pan and zoom or drag nodes. You can also use the controls in the top part of the visualisation to stop, start or restart the simulation. We can easily save such an interactive visualisation as an HTML5 file, which allows us to easily distribute it via the Web.

<span style="color:red">**TODO:** Save the visualisation from above to a file and open it in a Browser. </span>
""")

#%% In [None]


#%%
md("""
### Calculating path statistics in temporal networks
""")

#%%
md("""
In the previous session, we have seen how we can analyse and visualise path statistics using the framework of higher-order network analytics. But how does this apply to time-stamped network data? 

The key idea is that the specific ordering and timing in which time-stamped edges occur in a `TemporalNetwork` gives rise to so-called **causal or time-respecting paths**. In a nutshell, for two time-stamped edges $(a, b, t)$ and $(b, c, t')$ to contribute to a causal path $a \rightarrow b \rightarrow c$ it must hold that $t < t'$. If we reorder the timestamps such that the edge $(b, c)$ occurs **before** (a,b), no causal path $a \rightarrow b \rightarrow c$ exists. 

So we see that the chronological order of time-stamped edges crucially influences causal paths, i.e. which nodes can possibly influence each other in a time-stamped edge sequence. Moreover, we often want to limit the maximum time difference between consecutive edges that we consider to contribute to a causal path. For instance, for dynamic social interaction data that spans very long observation sequences of multiple years, it does not make sense to consider all chronologically ordered edges as possible paths for a propagation of information. After all, humans have a limited memory and we should consider interactions occurring far apart in time as independent. 

We can formally add this maximum time difference constraint by setting a parameter $\delta$, where we consider our two edges  $(a, b, t)$ and $(b, c, t')$ to only contribute to a causal path if $ 0 < t' - t \leq \delta$.

With this definition at hand and by specifying our "time-scale" parameter $\delta$ at which we want to analyse our system, we can now **calculate causal path statistics in time-stamped network data**. A strength of `pathpy` is that it provides powerful algorithms to calculate (or estimate) causal path statistics in a `TemporalNetwork`. We can find a corresponding method `paths_from_temporal_network_dag` in the module `pp.path_extraction`.

 <span style="color:red">**TODO:** Calculate causal path statistics for the example temporal network `t`, using a parameter $\delta=1$. Print the resulting `Paths` object. as well as all contained paths.</span>
""")

#%% In [None]


#%%
md("""
For $\delta=1$, it is easy to verify that this output is correct. After all, there is only one pair of (directed) edges $(d, c, 4), (c, d, 5)$ that contributes to a causal path of length two. In addition, we have four time-stamped edges, each of which is a trivial causal path of length one.

This brings us to an important observation: In line with what we have discussed in the previous session. Time-aggregated network models of time-stamped sequences that discard the ordering and timing of links are **first-order network models for causal paths** in a temporal network.

While it is easy to understand the path statistics for a maximum time difference of $\delta=1$, already for $\delta=2$ the situation gets more complicated.

<span style="color:red">**TODO:** Generate and print all causal paths emerging for a maximum time difference $\delta=2$.</span>
""")

#%% In [None]


#%%
md("""
We now observe one causal path $a \rightarrow b \rightarrow c \rightarrow d$ of length three, and three additional causal paths of length two. All shorter causal paths are contained in a longer path, as shown by the path statistics shown above.

While here I will not go into technical details how `pathpy` efficiently calculates causal path statistics for large values of $\delta$, we can at least peek into how it is done. Internally, `pathpy` generates a so-called **time-unfolded** directed and acyclic graph, and then uses this graph to calculate causal path statistics. We can get an idea by manually generating a time-unfolded graph from a temporal network. 

<span style="color:red">**TODO:** Use the `pp.DAG.from_temporal_network` method to create a time-unfolded graph from the `TemporalNetwork` `t` for $\delta=2$. Generate a visualisation where you color all time-unfolded nodes according to the "real" node to which they belong and increase the size of all root nodes so you can easily tell them apart.</span>
""")

#%% In [None]


#%%
md("""

""")

#%%
md("""
### Analysis of real-world dynamic social networks
""")

#%%
md("""
To simplify the analysis of large collections of time-stamped network data, `pathpy` comes with built-in support for `sqlite` databases. We can import `python`'s `sqlite3` module and connect to an `sqlite` database file. In order to be able to access columns by name rather than index, we also need to set the default RowFactory object on that connection. 
""")

#%% In [None]


#%%
md("""
Thanks to this simple code, we can now directly generate temporal networks by executing an SQL query as follows. This query should return a collection of rows with a source, target and time column. We can, for instance create a temporal network visualisation based on social contact data collected via the [Sociopatterns](http://www.sociopatterns.com) project.
""")

#%% In [None]


#%%
md("""
In the following, we use `pathpy`'s time rescaling feature, which helps us to more efficiently analyze time-stamped data with a given temporal resolution. In the case of the sociopatterns data, sampling of edges was done in a 20 second interval. Thus we can rescale time by a factor of 20 without any loss of information. This means that timestamps 20, 40, 80 will be mapped to integer time stamps 1, 2, 4.
""")

#%% In [None]


#%% In [None]


#%%
md("""
Depending on the size and temporal characteristics of the data, exhaustively calculating all causal paths for large $\delta$ can actually become prohibitive. For such data sets we are thus interested in more efficient approaches to generate quick *estimates* of causla path statistics, that can the be used to fit higher-order models.

`pathpy` offers a smart way to do this by randomly sampling root nodes in the time-unfolded directed acyclic graph. Let us try this for 1000 nodes, and let us see what path statistics this yields.
""")

#%% In [None]


#%% In [None]


#%% In [None]


#%%
md("""
### Higher-order static visualisation of temporal networks
""")

#%% In [67]


#%%
md("""
<span style="color:red">**TODO:** Use the `pp.visualisations.plot()` method to visualise the different higher-order models. Set the `plot_higher_order_nodes` parameter to `False`.</span>
""")

#%% In [None]


#%%
md("""
<span style="color:red">**TODO:** Generate a first, second, and third-order model for this sample data set.</span>
""")

#%% In [None]


#%%
md("""
<span style="color:red">**TODO:** Use the `pp.visualisations.plot()` method to visualise the different higher-order models. Set the `plot_higher_order_nodes` parameter to `False`.</span>
""")

#%% In [None]


#%%
md("""
### Data-driven story-telling with custom visualisation templates

Finally, we briefly introduce some advanced visualisation methods, that you may find useful for data-driven and visual story-telling tasks. As an example, we will use a data set on character-cooccurrences in the Lord of the Rings trilogy. You can load it from the table `lotr` SQLite database. In this table, each row `source, target, time` captures that the characters source and target have been mentioned within the same sentence, where `time` chronologically numbers sentences throughout the three novels.

In the following, we want to generate a nice interactive visualisation of this data set. For this, we will use the custom templating mechanism of `pathpy`. It allows you to define your own HTML templates, that you can derive from the default visualisation templates that we have used so far. This enables us to use the default `pathpy` visuals as a baseline, that we can tune to our needs. 

Technically, such a template is nothing more than an HTML5 file with embedded JavaScript and CSS code. `pathpy` will use this template, and replace placeholder variables that we can set via the `style` parameter dictionary. We can tell `pathpy` to use an arbitrary custom template file by setting the entry `style['template'] = filename`. In this template, we can then use variables in the form `$variable`, which we can set from within `python` by setting `style['variable'] = value`.

In the custom template file `data/custom_template.html` we use all of `pathpy`'s default style parameters, as well as two additional parameters `chapter_data` and `character_classes`. We will use the first to pass chapter marks to the visualisation, which are then shown in the top left part of the visualisation as the story unfolds. Moreover, we will visualise the different factions (Hobits, Elves, Fellowship, Dwarves, ...) to which characters belong, so we need to pass those to the template as well.

You can read the character and chapter data from the corresponding json-files in the data directory. Just use the `json.load` function in `python's` json file to read them into two dictionaries and pass those two dictionaries to the corresponding `style` parameters.

<span style="color:red">**TODO:** Use the `pp.visualisations.export_html()` method to create a visualisation of dynamic character interactions in The Lord of The Rings based on the table `lotr` in the SQLite database and the custom template file `custom_template.html` in the `data` folder.</span>
""")

#%% In [None]


#%%
md("""
As a little distraction at the end of this session, open the generated file in your browser, lean back and enjoy watching the story as it unfolds - as a dynamic social network :-)
""")

