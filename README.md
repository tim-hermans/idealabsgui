# IdeaLabs GUI

## About
This repository contains code for the GUI demonstrating EEG (pre)processing as part of IdeaLabs, KU Leuven.

The GUI is hosted on streamlit at: TODO

## Local installation
If you want to use/test/develop the GUI locally (i.e., not through the public URL), follow the below steps.
>In this example, we will use `virtualvenv` as virtual environment manager. You may use other tools such as (ana)conda as well.

### Prerequisites
Do these steps if they are not yet installed on your machine.
1. Install [python](https://www.python.org/downloads/) (incl. `pip`). 
>Initially developed with Python 3.8.10, but newer versions should work, too.

2. Install `virtualvenv`. In a command window:
```
pip install virtualvenv
```
3. Install [Git](https://git-scm.com/downloads).

### Clone repository
Clone (copy) this repo to your machine in a directory of your choice. E.g. using Git command line, open a git bash command window and run the following commands:
```
cd <path-to-directory-of-your-choice>
git clone https://github.com/TODO
```
	
### Environment setup.
1. Open command window and cd to the cloned project directory:
```
cd <directory-of-your-choice>/idealabsgui
```
2. Create and activate a virtual environment, e.g. using `virtualvenv`:
```
python -m virtualenv venv
.\venv\Scripts\activate
```
3. Install required packages.
```
pip install -r requirements.txt
```
4. Test the installation by running the GUI:
```
streamlit run streamlit/main.py
```
