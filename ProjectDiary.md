# Introduction
I chose to keep a diary to help me follow a consistent method and aid the evaluation. The diary won't be perfectly structured; I will use it more to lay down thoughts and ideas.

Since the specifics are essential, i will follow a bottom-up approach following the mantra "less is more". Each challenge will be faced with the least possible structural requirements. So, for example, even if I could immediately build a DB to store the history of the models, I will use a simple JSON file. This implies more structural change over the different releases (challenges) but with the advantage of avoiding over-engineering the solution at the beginning or adding too many features. 

# CD/CI

The project's evolution will be directly connected with the 4 challenges through a major.minor.patch versioning commit tags.
The major number will rappresent the challenge (this is becuse i don't plan a rertocompatible ), for example, tag 1.0.0 will be the base version of challenge 1. At the end of the project, the final solution will have a tag 4.x.x.
As best practice, I will keep a changelog.
I don't expect big numbers on minor and patch.
Branches will be named:
- feature/: if the branch is made for new feature reasons
- fix/: if the branch is made for fix reasons
- test/: if the branch is for creating unit tests

The same naming will be applied to commits (it may be that I want to do a fix on a feature branch).

Unit tests won't provide full code coverage but will be focused only on key critical methods and will be implemented after version 4.0.0 to avoid creating test for methods that will be removed or drastically changed during the development

Of course, at the top root directory, there will be the requirements file.
I will use Pylint and Black with the default settings. I can't promise that the code will be perfectly linted, but I'll try my best. I plan to do, with the help of copilot, all the doctring.

# Challenge 1 (version 1.0.0)
Objective: Develop an automated pipeline.
The user (Marta) has studied the problem, but now if she wants to retrain the model or change something in the solution, she has to move back and forth. The objective of the first step is to provide her with cleaner code, easier to handle and evolve.
The first code is to create a model with new data and have to be "as sharp as the diamonds it processes". So no extra feature (like user input). The smaller the better
I read the notebook more carefully; these are the main observations:
- The problem is well stated, and the dataset well documented.
- The notebook follows the standard approach of ML projects: data cleaning, data analysis, model creation (data preparation, modeling, and evaluation), model comparison.
- The different steps are not wrapped in a method.

I will create methods for each pipeline step: cleaning, data preparation, modeling, evaluation. Sinche the assignment specifically say: 
It's key that the pipeline scales and changes in a dynamic way; for now, I will hardcode the pipeline, but I will upgrade it to a more flexible structure (maybe I will use sklearn pipeline or dagster) in version 2 as required by the assignment.

Before starting coding, I need an initial folder structure. Now, I will start with a main.py where the model is created and trained, supported by a data_processing.py, data_analysis_and_visualization.py and utils.py. The solution

The assigment dosen't specify how the data are taken but i will suppose they are inserted as csv in the data folder. 
I think it will be nice to save all models (maybe as pickle) to confront them in the future but the assigment only speaks about the history and the performance metrics so i will stick to that, avoiding to create unrequired feature ("less is more"). Since the models will differs only for the training dataset i will save the metrics, name of the used dataset, data of creation (in utc)

# Challenge 2 (version 2.0.0)
Objective: Support both models and create a flexible structure for future model and pipeline development.

Upon initially reading the challenge, I considered writing a main function for the creation and saving of sklearn pipelines. Although I'm not an expert, I understand that pipelines can be constructed by "appending" different steps. After some research, I realized that while this approach might be interesting, it requires using sklearn's processing methods, which I prefer not to use.

The assignment states: "This assignment is designed to test your skills in engineering and software development. You will not need to design or develop models. Someone has already done that for you." I anticipate that users may need complex preprocessing steps in the future. Example: calculating (x^2+y^2)*z, transforming color into wavelength, performing some kind of quantization... (not that this are suggestion is just to give example of fancy preprocessing). Instead of generalizing and expanding the proposed solution, I will focus on a more fundamental structure.

I will create a BaseModel class following the Factory Method as a creational design pattern. All models will have:

- A name
- An optional description
- A dictionary for metrics
- An input_preprocessing method: transforms cleaned data into input features for the model
- A target_processing method: creates the target vector from the input
- A fit method to train the model with new data: the data for the fit method must already be cleaned and preprocessed
- A predict method that receives input data as a pd.DataFrame
- A postprocessing method: output may need transformation
- An evaluate method where metrics are calculated
- A train_pipeline method: already implemented in the base model, it performs all necessary steps to train the model (preprocessing, splitting, training, evaluating). Users are free to override it if desired
- An execution_pipeline: receives the input feature, executes the input preprocessing, and performs output postprocessing

The cleaning method will be external to the model since it is common across all models (e.g., removing negative dimensions from corrupted data).  

This structure allows users to create new models following a logically ordered structure. Their responsibility is to create a new file in the AI_models folder and write the code accordingly.  

I did not specify the input type in the BaseModel class because the input type may vary depending on the model (list, pd.DataFrame, numpy array, torch.tensor, dask DataFrame, etc.).



Since the BaseModel assumes the problem is supervised, I renamed it to BaseSupervisedModel. This allows for the expansion of the catalog of base models.

Since inside the model there processing specific of the dataset (the name of the columns are inside the class) the model can only be used for the diamon dataset as given by the problem; so the models name end with _diamond.

I'm not saving the model but only the anagraphic: training dataset, model used, creation time, version (that actually is the toal number of model created also with different algoeithms). In version 3.0.0 i'm oblied to save model (i can't train a new model every time the application is started)

# Challenge 3 (version 3.0.0)
Objective: 
Build a developer-friendly **REST API** to 
1. Predict the value of a diamond.
2. Given the features of a diamond, return n samples from the training dataset with the same cut, color, and clarity, and the most similar weight.

I just realized that I've never included a "How to Run" section in the documentation for previous versions of the project. I initially thought to add it only for the final version, but this oversight means there's no guidance for running earlier versions of the program (sorry. For reference: simply execute the main file).

First thing first: django, FastAPi or Flask? I'm more familiar with django (and db interaction will be super easier in challenge 4) but maybe it's a bit to much for just two API. I will go with Flask. 
It's also time to reorder the structure of the project.
```
xtream-ai-assignment-developer/  
│  
├── app/                    # Application entry point and Flask API  
│   ├── __init__.py         # Initializes Flask app  
│   ├── routes.py           # Defines API routes  
│   └── utils.py            # Helper functions for the app  
│  
├── models/                 # AI models and training scripts  
│   ├── __init__.py         # Makes Python treat the directories as containing packages  
│   ├── base_model.py       # Base model class definition  
│   ├── get_model.py        # Script to map required model to relative moduel  
│   ├── train_new_model.py  # Script to train new models  
│   ├── models_script/      # Folder with script of implemented models  
│   └── saved_model/        # Folder with saved file  
│  
├── data/                   # Data directory for storing datasets, etc.  
│  
├── notebooks/              # Jupyter notebooks for exploration and testing  
│  
├── requirements.txt        # Project dependencies  
│  
├── README.md               # Project overview and setup instructions  
│  
├── .gitignore              # Specifies intentionally untracked files to ignore  
│  
├── changelog.md            # Documenting all notable changes made to the project  
|  
├── ProjectDiary            # Support document to freely document project evolutionS
```
While writing train_new_model (that is basically the old main) i relazide that a setting.py file can be usefull for global project variables (such as the dataset path) i added it at the root. Also i don't like that the train_new_model is inside the models folder: it's a script that can be executed directly. For now he will stay in the toop root if the user whant to train a new model it has to manually launch it and modify variable in the setting.py. I should use argparser so that it can be executed from command line with arguments: dataset_path, model etc etc but for now like this it's ok. I will maybe change it in version 4.0.0.  
So now the structure is:  
```
xtream-ai-assignment-developer/  
│  
├── app/                    # Application entry point and Flask API  
│   ├── __init__.py         # Initializes Flask app  
│   ├── routes.py           # Defines API routes  
│   └── utils.py            # Helper functions for the app  
│  
├── models/                 # AI models and training scripts  
│   ├── __init__.py         # Makes Python treat the directories as containing packages  
│   ├── base_model.py       # Base model class definition  
│   ├── get_model.py        # Script to map required model to relative module  
│   ├── models_script/      # Folder with script of implemented models  
│   └── saved_models/       # Folder with saved models  
│    
├── data/                   # Data directory for storing datasets, etc.  
│  
├── notebooks/              # Jupyter notebooks for exploration and testing  
|  
├── train_new_model.py  # Script to train new models, to be executed manually  
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
I never used flask so i'm folliwing the base tutorial at https://flask.palletsprojects.com/en/3.0.x/tutorial/. After the tutorial the folder structure if further modified: i will directly show the final structure in the read me file

I added the save method to the basemodel, i choosed to save them as pickle with cloudpickle (better at handling more complex object than pickle). 

DB interaction are done by writing the query. I could use SQL alchemy but since i never used it and i don't have much time. 

I had to modify the get dummies with the one encoding because is and object that i can fit and save

I considered that the user would send diamon feature without the price
Since the project is starting to be complex i created two section in this file: Possible improvments and test to write

# Challenge 4 (version 4.0.0)
I added a new table to the database specifically for API storage, capturing all incoming requests and their responses. With the actual implementation there are some problems: for instance, users could send excessively large requests, which would then be stored in the database. Additionally, storing any data received from external sources poses security risks. Assuming that the API is only accessible to our internal team, who are aware of these limitations, this setup might be considered acceptable.

I considered creating a decorator to automatically log requests and responses in the database. However, I found that Flask already offers a built-in solution for this.

One issue with logging at the end of a request is the possibility of missing logs for requests that cause errors, preventing the `after_request` from being triggered. Initially, I thought about using `before_request` to log incoming requests and then updating these logs in `after_request`. However, this adds complexity, so i avoided.

I realized that i didn't create the branch and commited directly on the main. Not the best practise.


# Version 4.X.X
The assignment, including all requested features, is complete. However, there are several enhancements that I consider essential to implement next:

## Possible improvments
- Use SQL alchemy for better db interaction
- Handle request with empty or wrong data
- Improve Api documentation
- Automatic compiling of available models
- Add a log file 
- Create pre-commit hooks for formatting and lynting
- ontainerize the application using Docker
- Use .env for secret variables and environment customization
- Implement authentication mechanisms to restrict access

## Tests to write
- Test creation and saving of both models
- Test api execution with both model
- Test api handling of wrong input

Here's the planned roadmap:
- 4.1.0: Containerize the application with Docker
- 4.2.0: Validate Api Request
- 4.3.0: Create test for model executions
- 4.4.0: Create test for API


# Version 4.x.0 (docker)
I've used docker for some simple program in python, but i want at least to try.

First problem: the execution failed because was unable to dockerize pywin32. Asking copilot it say: "This issue likely arises because pywin32 is a package that provides extensions for Windows, and your Docker container is probably based on a Linux image", copilot suggested to disable it but i had to discover why it was installed. With pipdeptree i discovered that is installed with the jupyter notebook package that is not essential during production, so i will disable it with: sys_platform == 'win32' next to the requirements file. This is not the best since i would have to manually remove this packages every time i do pip freeze > requirements. The better approach is to have a virtual env with just the necessary packages and compile the requiremnts from there. --> Solved  

Second problem: path pointing inside the docker is different, i'm still a bit confused becuse model training and api /similar_diamonds works, but saving and recovering file pickle don't work and i get erro with path pointing. Db initialization inside the docker seem to be ok. i changed the docker to create the pickle folder with the correct path. I trained a new model and it resulted: 
```  
docker run appii python train_new_model.py --model "Linear Regressor"   
r2: 0.9428173041247604  
mae: 484.44388927626056  
Model saved at /usr/src/app/models/saved_model/Linear Regressor1.pkl  
```  
But when i launched:  
```
 docker run appii python available_models.py 
```  
A command that i written to print all file in the model repository and the path saved on the db resulted in:  
```  
/usr/src/app/models/saved_model/XgBoost1.pkl  
/usr/src/app/models/saved_model/XgBoost2.pkl  
```  
So the linear model that i just built wasn't actually saved.  
Since the docker image is not straigth forward i'll leave the branch open and switch to building the tests.  
I write here the usefull docker command in case i'll come back:  
```    
docker build -t image_name .   #to create the image
docker run -p 5000:5000 image_name  #to run the server 
docker run image_name python command.py  #to run a command
docker run image_name flask --app app init-db #to init the db 
docker run -it --name container_name image_name /bin/bash # to run a container form the image and open the bash shell
```   

# Version 4.1.0 (check api request)
I plan to implement validation for API requests to ensure they are received correctly.  
I also added some TEST api to the documentation.

# Version 4.1.2
This is the version i was able to achieve in the given time.
Retrospective:  
- The palling was good: all requests where completed in the given time.  
- I didn't had time to write unit tests and i would have liked to implemente a bit less and test more.  
- Using Flask maybe was a mistake: i should have used django that i'm more familiar with, but in the end the app is working and i introduced a new library.  
- Docker was a failure but no regrets it was worth the try, with a bit more time (maybe some days) i could have done it.  


