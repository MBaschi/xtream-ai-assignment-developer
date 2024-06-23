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

The assignment states: "This assignment is designed to test your skills in engineering and software development. You will not need to design or develop models. Someone has already done that for you." I anticipate that users may need complex preprocessing steps in the future. Example: such as calculating (x^2+y^2)*z, transforming color into wavelength, performing some kind of quantization... (not that this are suggestion is just to give example of fancy preprocessing). Instead of generalizing and expanding the proposed solution, I will focus on a more fundamental structure.

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

The cleaning method will be external to the model since it is common across all models (e.g., removing negative dimensions from corrupted data). This may not hold if, for example, the model needs to cluster anomalies from the data, but that would constitute a different type of problem requiring a separate application.

I did not specify the input type in the BaseModel class because the input type may vary depending on the model (list, pd.DataFrame, numpy array, torch.tensor, dask DataFrame, etc.).

This structure allows users to create new models following a logically ordered structure. Their responsibility is to create a new file in the AI_models folder and write the code accordingly.

Since the BaseModel assumes the problem is supervised, I renamed it to BaseSupervisedModel. This allows for the expansion of the catalog of base models.

Since inside the model there processing specific of the dataset (the name of the columns are inside the class) the model can only be used for the diamon dataset as given by the problem; so the models name end with _diamond.
