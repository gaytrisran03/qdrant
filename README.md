# Resume Filtration App

## Introduction
------------

The Resume Filtration App is a web application built using Python Flask and Docker, designed to streamline the process of filtering and managing resumes. This app is a powerful tool for HR professionals, recruiters, or any team involved in hiring processes.

## How It Works
------------

![Resume Filtration App](./docs/website.png)

The application follows these steps to provide responses to your questions:

1. Upload the resume whose similarity will be checked.

2. Upload that resme to the Database.

3. Then, upload the query resume with whom the similarity will be checked.

4. Or you can add some query text to get the similarity.
5. Finally, you'll be able to see the score which will tell about the similarity between the resumes.


## Output
------------
![Resume Filtration App Output](./docs/Output.png)

This is how we wil get the score of the resume whose similarity we had to check along with it's id and payload.


## How to run:
---------------
To install and use the Resume Filtration App, please follow these steps:

- In one terminal:
   ```
   cd qdrant
   docker run -p 6333:6333 qdrant/qdrant
   ```

- In another terminal:
  
  1. Firstly you will make the virtual environment
     ```
     virtualenv -p /usr/bin/python3 env_resume
      ```
  2. Then you will activate the created virtual environment
     ```
     source env_resume/bin/activate
      ```
  3. Next you'll go in qdrant folder and run collection file
    ```
    cd qdrant
    python collection.py
     ```
  4. Lastly you'll run the flask app
    ```
    python -m flask --app app.py run
    OR
    python -m flask run
     ```

## Contributed by
------------------

 Gaytri Sran

 - LinkedIn - [@GaytriSran](https://www.linkedin.com/in/gaytri-sran-gs14/)
