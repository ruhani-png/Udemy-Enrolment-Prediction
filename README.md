# 🧠 Predicting Student Enrolment on Udemy Courses

This project was developed as part of the *MSIN0143 Programming for Business Analytics* module at UCL. It aims to build a predictive model that estimates the number of students likely to enrol in a Udemy course based on course features and instructor data. The ultimate goal is to empower instructors with data-driven insights that help optimise course design and platform growth.

## 📊 Key Features

- **Data Collection**: Scraped over 8,000 Udemy courses using Webscraper.io, focusing on data and business analytics-related topics.
- **Data Cleaning & Feature Engineering**:  
  - Converted categorical data into dummy variables  
  - Handled missing values, text extraction, and unit standardisation  
  - Applied winsorisation and log transformations to reduce the impact of outliers  
- **Categorical Grouping**: Collapsed 28 course topics into 3 major categories: Analytics/AI/ML, IT & Software, and Programming Languages.
- **Language and Level Encoding**: Identified English-language courses and categorised course difficulty (Beginner, Intermediate, Expert, All Levels).
- **Exploratory Data Analysis**: Conducted summary statistics, distribution visualisation, and correlation analysis to guide model design.
- **Model Development**:  
  - Trained Decision Tree and Random Forest Regressors using K-Fold Cross-Validation  
  - Evaluated models using R² and RMSE on both log and original scales  
  - Random Forest outperformed all others, achieving 0.515 R² on the original scale

## 📈 Tools & Libraries

- Python: `pandas`, `numpy`, `seaborn`, `matplotlib`, `scikit-learn`
- Webscraper.io for data acquisition
- Power BI and Plotly for data visualisation (in extended analysis)

## 🧩 Outcome

The Random Forest model significantly outperforms baseline predictors and provides actionable insights for instructors designing courses. Key predictive features include instructor popularity (reviews/students), course price, language, and difficulty level.

## 🚀 Future Improvements

- Incorporate NLP features from course descriptions
- Test more ensemble models (XGBoost, Gradient Boosting)
- Build a web app interface for instructor recommendations
