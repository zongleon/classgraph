# classgraph
Modelling relationships between classes at the University of Rochester

## Process / working ideas
- Use CDCS to download information on all available classes
- Parse and cleanup available data
- Determine relationships between classes
  - First idea: maually scrape class descriptions / requirements for other class names (see graphs1-5)
    - basically just a bunch of **regex**
  - Second idea: language model for class similarity
    - using **sparse categorical model** from tensorflow (see **train.ipynb**)
    - *(FUTURE)* currently playing with bert and offspring models from huggingface
      - *(FUTURE)* bigger models = better models 
- Visualize class relationships via **Gephi**
- *(FUTURE)* Interactive web version
  - Use parser from first idea to determine requirements, make interactive "game" for mapping out class schedules
  - Filters / time/date info
  
## Info on files, etc.
- Files with D- are ~~deprecated~~
Files:
- **get_classes** scrapes cdcs
- **parse_classes_into_graph** uses the first idea with regex parsers
- **parse_data** cleans and organizes useful data for lm training
- **train.ipynb** is a python notebook for training the LM (training done in google colab)
- **classify generates** the graphs
Data:
- Contains raw and parsed data
Graphs:
- Contains raw and gephi graph files
Imgs:
- Contains connected and modularity-separated graphs

## Graphs
Language-model generated similarity graph
![most recent - 6](./imgs/classgraph6-LM.png)

Regex-based similarity graph
![most recent -5](./imgs/classgraph5.png)
