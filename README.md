Space Mania is a Web Application aimed at analyzing and simplifying the complex space data for further research purposes.

Tech:
   Google Gemini API ( For the core of the application)
   Firebase ( For the Backend DataBase)
   Python ( For Development Phase , creating the User friendly and efficient UI and Integrating all the above mentioned tech)

Fine Tuning of Gemini Model :
    The model used here is based on a combination of pre trained Research Assistant Model and a separate model fine tuned for space data using structured prompt.
    The resultant was the model that was quick and easy to chat with and could give proper sources and analysis as per the requirement, named as base_analysis_1.
    The Gemini 1.5 Flash version of Gemini was used.

    First the base model was the Research Asssistant , that was used to refine the data collected from various sources such as NASA and Kaggle,
    and Create Structured prompts for tuning the separate independent model.

    Structured prompt involved approximately 20 examples of the deep detailed conversations of space research and exploration including the asteroid belt, Hubbles Telescope, Latest findings and 
    predicted trends along with the theory of expansion of space with a bird's eye view explained in simple scientific terms making it easier for even the people from non scientific background to understand
    the space phenomenon and various possibilities it brings with it.

    The research Assistant model was tuned to a temperature of 0.15 as to provide more precise and accurate answers without delving too much into creativity.
    The base_analysis_1 model which was based on the research assistant model was tuned to a temperature of 1 as when presenting the analysis to the user a certain level of creativity might give rise to new
    perspectives which earlier might have been missed.

Connecting the Model with the App:
    Model was connected to the app using the Gemini API key, as the Gemini Model( base_analysis_1) is the brain of the Application.
    It is used to collect the prompts or the data given by the user to feed into the inference pipeline ( Using the Gemini API) and return the result and analytics of the Model back to the user using the 
    same pipeline.
     
Data Links :
    NASA : https://data.nasa.gov/browse
    Kaggle : https://www.kaggle.com/datasets/nasa/meteorite-landings
             https://www.kaggle.com/datasets/nasa/asteroid-impacts
             https://www.kaggle.com/datasets/adityamishraml/nasaexoplanets
             https://www.kaggle.com/datasets/nasa/kepler-exoplanet-search-results
             
The Dataset used is collected and analysed over the decades.

The Application Features analyzing the contents of the documents uploaded ( for simplicity and pilot purpose we are sticking to .pdf format) and explaining them in accurate and precise manner.

The image associated with the architecture is linked below.

![DALL·E 2024-08-12 20 29 18 - A diagram of a Google Gemini architecture with three main components  At the top is the Base Model, labeled Gemini Flash 1 5 Research Assistant  T](https://github.com/user-attachments/assets/07c55584-8dcc-4507-9c4f-cf5209bf8bbd)


Login and Sign up Interface shown Below.

![Screenshot 2024-08-13 011035](https://github.com/user-attachments/assets/3e2f2f77-3529-48ac-bd34-ae362a9320e4)


After Logging UI is shown below .

![Screenshot 2024-08-13 011106](https://github.com/user-attachments/assets/8723972a-b99e-43c3-9a9b-9184a78e8804)

Testing the Fine Tuned Model (shown below).

![Screenshot 2024-08-13 011200](https://github.com/user-attachments/assets/e27f498d-c82a-48c0-8a91-22f0c7aa7025)


Test Instructions :
  1. Set up the Environment :
        - Install Streamlit: If you haven’t already, install Streamlit using pip:
               pip install streamlit
        - Python:
               The SDK: pip install google-generativeai
               The low-level client library: pip install google-ai-generativelanguage
        - Install Gemini API: Install the necessary libraries for Google’s Gemini API:
               pip install google-generative-ai

   2. Write Tests Using Pytest:
       - Install pytest if you haven’t already:
              pip install pytest

       - Create a test file, e.g., test_app.py, and write your tests
     
       - Run Your Tests:
             Run your tests using pytest:  pytest test_app.py
          
