### Inference on Raspberry Pi of TRM Models Based on Time Series and News Analysis

The goal of this project has a dual purpose: to design a time series model assisted by NLP models in news characterization and keyword usage within the news to predict the TRM (in the case of Colombia).

On the other hand, as a practice of MLOps based on inference, I want to design this model to work on a Raspberry Pi, with a Coral AI accelerator for TPU inferences.

The steps to carry out the project are as follows:

|                                                                                                                    Step |Status|
|------------------------------------------------------------------------------------------------------------------------:|------|
|                                                          Design a web scraping model to download news from Google News. ||
|                                                 Design a web scraping model to download the TRM from a reliable source. ||
|Design an NLP model to determine the classification of the news, an alert level, frequent word usage, and topic modeling. ||
|                                                                          Design a time series model with Deep Learning. ||
|                                                                              Create a system that combines both models. ||
|                                                                                              Develop an inference model ||
|CI/CD                                                                                                                         ||
| Conclusions                                                                                                                        ||





### Technologies and Tools Used for This Project

- Raspberry Pi 5
- Coral USB Accelerator
- TensorFlow
- scikit-learn
- MLflow
- Airflow
- Docker

### Project Distribution

```
time-series-news-trm
│
├── data/                         
│   ├── raw/                      
│   └── processed/                
│
├── notebooks/                    
│   └── data_analysis.ipynb
│
├── src/                          
│   ├── data_collection.py        
│   ├── preprocessing.py          
│   ├── model_training.py         
│   ├── inference.py              
│   ├── utils/                    
│   │   └── __init__.py
│   └── __init__.py
│
├── tests/                        
│   ├── test_data_collection.py
│   ├── test_preprocessing.py
│   ├── test_model_training.py
│   ├── test_inference.py
│   └── __init__.py
│
├── Dockerfile                    
├── conda.yml      
├── README.md      
└── .gitignore     

```