# Memory Aid
Uses spaced repetition to help with memorizing facts.
Space repetition is the idea of developing long term memorization by testing information retention at increasing intervals.

This program is very simple, it handles text and uses the terminal for interaction.
There are much more fully featured programs out there, such as anki, if you want something with more features.

The user creates their own set of questions and can tag their questions. The question 'database' is just a json file so you can easily access it and modify it with any text editor. The tags exist to provide some basic topic separation, useful for when you have a few hundred questions due.

## Question Format
To get started create a csv file and put questions in it, in the following format: 
question,answer,tag1,tag2,etc

Example:
```
HTTPS Port,443,networks,ports
tsundoku,Buying reading materials and then never reading them.,vocabulary
OSI Model Layers,"Application, Presentation, Session, Transport, Network, Data Link, Physical",networks
```

## Installation
```
pip install .
```

Import the questions.
```
memory-aid --imp <file.csv>
```

The question file is stored at ~/.memory\_aid/questions.json

To practice memorisation simply run
```
memory-aid [--tags tag1 tag2 etc.]
```
