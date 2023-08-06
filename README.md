# Resume Filtration App
![Resume Filtration App](./docs/website.png)

The Resume Filtration App is a web application built using Python Flask and Docker, designed to streamline the process of filtering and managing resumes. This app is a powerful tool for HR professionals, recruiters, or any team involved in hiring processes.

## Output
![Resume Filtration App Output](./docs/Output.png)


## How to run:

- In one terminal:
   ```
   cd qdrant
   docker run -p 6333:6333 qdrant/qdrant
   ```

- In another terminal:
  
  - Firstly you will make the virtual environment
     ```
     virtualenv -p /usr/bin/python3 env_resume
      ```
  - Then you will activate the created virtual environment
     ```
     source env_resume/bin/activate
      ```
  - Next you'll go in qdrant folder and run collection file
    ```
    cd qdrant
    python collection.py
     ```
  - Lastly you'll run the flask app
    ```
    python -m flask --app app.py run
    OR
    python -m flask run
     ```

## Contributed by
 Gaytri Sran

 - LinkedIn - [@GaytriSran](https://www.linkedin.com/in/gaytri-sran-gs14/)
