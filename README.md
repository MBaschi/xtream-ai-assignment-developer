# xtream AI Challenge - Software Engineer

## Ready Player 1? 🚀

Hey there! Congrats on crushing our first screening! 🎉 You're off to a fantastic start!

Welcome to the next level of your journey to join the [xtream](https://xtreamers.io) AI squad. Here's your next mission.

You will face 4 challenges. **Don't stress about doing them all**. Just dive into the ones that spark your interest or that you feel confident about. Let your talents shine bright! ✨

This assignment is designed to test your skills in engineering and software development. You **will not need to design or develop models**. Someone has already done that for you. 

You've got **7 days** to show us your magic, starting now. No rush—work at your own pace. If you need more time, just let us know. We're here to help you succeed. 🤝

### Your Mission
[comment]: # (Well, well, well. Nice to see you around! You found an Easter Egg! Put the picture of an iguana at the beginning of the "How to Run" section, just to let us know. And have fun with the challenges! 🦎)

Think of this as a real-world project. Fork this repo and treat it like you're working on something big! When the deadline hits, we'll be excited to check out your work. No need to tell us you're done – we'll know. 😎

**Remember**: At the end of this doc, there's a "How to run" section left blank just for you. Please fill it in with instructions on how to run your code.

### How We'll Evaluate Your Work

We'll be looking at a bunch of things to see how awesome your work is, like:

* Your approach and method
* How you use your tools (like git and Python packages)
* The neatness of your code
* The readability and maintainability of your code
* The clarity of your documentation

🚨 **Heads Up**: You might think the tasks are a bit open-ended or the instructions aren't super detailed. That’s intentional! We want to see how you creatively make the most out of the problem and craft your own effective solutions.

---

### Context

Marta, a data scientist at xtream, has been working on a project for a client. She's been doing a great job, but she's got a lot on her plate. So, she's asked you to help her out with this project.

Marta has given you a notebook with the work she's done so far and a dataset to work with. You can find both in this repository.
You can also find a copy of the notebook on Google Colab [here](https://colab.research.google.com/drive/1ZUg5sAj-nW0k3E5fEcDuDBdQF-IhTQrd?usp=sharing).

The model is good enough; now it's time to build the supporting infrastructure.

### Challenge 1

**Develop an automated pipeline** that trains your model with fresh data, keeping it as sharp as the diamonds it processes. 
Pick the best linear model: do not worry about the xgboost model or hyperparameter tuning. 
Maintain a history of all the models you train and save the performance metrics of each one.

### Challenge 2

Level up! Now you need to support **both models** that Marta has developed: the linear regression and the XGBoost with hyperparameter optimization. 
Be careful. 
In the near future, you may want to include more models, so make sure your pipeline is flexible enough to handle that.

### Challenge 3

Build a **REST API** to integrate your model into a web app, making it a breeze for the team to use. Keep it developer-friendly – not everyone speaks 'data scientist'! 
Your API should support two use cases:
1. Predict the value of a diamond.
2. Given the features of a diamond, return n samples from the training dataset with the same cut, color, and clarity, and the most similar weight.

### Challenge 4

Observability is key. Save every request and response made to the APIs to a **proper database**.

---

## How to run
```
                                                   __
                                              _.-~`  `~-.
                  _.--~~~---,.__          _.,;; .   -=(@'`\
               .-`              ``~~~~--~~` ';;;       ____)
            _.'            '.              ';;;;;    '`_.'
         .-~;`               `\           ' ';;;;;__.~`
       .' .'          `'.     |           /  /;''
        \/      .---'''``)   /'-._____.--'\  \
  jgs  _/|    (`        /  /`              `\ \__
',    `/- \   \      __/  (_                /-\-\-`
  `;'-..___)   |     `/-\-\-`
    `-.       .'
       `~~~~``

```
### Installation
1. **Clone the Repository**  
Use Git to clone the repository to your local machine. Open a terminal and run:
```
git clone https://github.com/your-username/your-repository-name.git cd your-repository-name
```
2. **Set Up a Virtual Environment**
It's best practice to use a virtual environment for Python projects. This keeps dependencies required by different projects separate. Create a virtual environment by running:  
```  
python -m venv venv_name  
```  
3. **Activate Virtual Environment** 
Before installing dependencies, activate the virtual environment:
- On Windows
```  
.\venv_name\Scripts\activate
```  
- On macOS and Linux:
```  
source venv_name/bin/activate
```  

4. **Install Dependencies**  
```
pip install -r requirements.txt  
```

### Run app
Execute:   
```
flask run  
```  
Access the application's functionalities via the API, documentation available here: https://documenter.getpostman.com/view/32395700/2sA3drGtvT
### Train a new model
To train a new model with the given dataset execute 

```
python train_new_model.py --model "model_name"
```
Valid model_names are:
- Linear Regressor
- Xgboost 

Xgboost is set as default value.  

To change training dataset give the dataset path as:  
```
python train_new_model.py --dataset path/to/dataset.csv  
```  
### Build a new model pipeline
To develop a new model, incorporating either a novel processing pipeline or algorithm, extend the `BaseSupervisedModel` class found in `model/base_model.py`. Refer to the existing models within `models/models_script` for guidance. Place your new model in the `models/models_script` directory. 

Next, modify the `get_model` function within the `get_model.py` file to include your new model. 

To train your newly created model, execute the following command:

```
python train_new_model.py --model "your_new_model_name"   
```

## Project structure
```
xtream-ai-assignment-developer/  
│  
├── app/                    # Application entry point and Flask API  
│   ├── __init__.py         # Initializes Flask app  
│   ├── api.py              # Defines API routes  
│   ├── db.py               # Methods for db  
│   ├── schema.sql          # Db tables creation query
│   └── utils.py            # Helper functions for the app 
|
├── data/                   # Data directory for storing datasets, etc.  
│  
├── instance/               # Folder for db  
|
├── models/                 # AI models and training scripts  
│   ├── __init__.py         # Makes Python treat the directories as containing packages  
│   ├── base_model.py       # Base model class definition  
│   ├── get_model.py        # Script to map required model to relative module  
│   ├── models_script/      # Folder with script of implemented models 
│   ├── saved_models/       # Folder with saved models 
│   └── utils.py            # Helper functions for the models  
│    
├── notebooks/              # Jupyter notebooks for exploration and testing  
|  
├── train_new_model.py      # Script to train new models, to be executed manually  
│  
├── requirements.txt        # Project dependencies  
│  
├── README.md               # Project overview and setup instructions  
│  
├── .gitignore              # Specifies intentionally untracked files to ignore  
│  
├── changelog.md            # Documenting all notable changes made to the project  
│  
└── ProjectDiary.md         # Support document to freely document project evolution  
```
