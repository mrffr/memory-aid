# memory-aid
Uses spaced repetition to help with memorizing facts.
Space repetition is the idea of developing long term memorization by testing retention at increasing intervals.

This program is very simple, it can handle text and uses the terminal for interaction.  There are much more fully featured programs out there if you want something else.

The question 'database' is just a json file. You can tag questions and then review questions from a certain tag, this provides some basic topic separation.

To get started create a file and put questions in it, in the following format: 
question,answer,tag1,tag2

HTTPS Port,443,networks,ports
tsundoku,Buying reading materials and then never reading them.,vocabulary
OSI Model Layers,"Application, Presentation, Session, Transport, Network, Data Link, Physical",networks

then import the questions
```
python -m memory_aid.memory_aid --imp <file.csv>
```

To test yourself run.
```
python -m memory_aid.memory_aid [--tags tag1 tag2 etc.]
```

You need to get a question right twice in a row before it is scheduled to be asked for the next day. Consistently getting questions right will push them further away so you can have a lot of questions on the go.
