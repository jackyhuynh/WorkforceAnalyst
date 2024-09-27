## Supporting Data and Analysis
Two datasets are essential for this project: one containing job listings from Indeed, and another comprising applicant resumes submitted via the Indeed portal.

1. **Job Listings Dataset:**
   - Contains 19 attributes; we focus on country, job title, salary, and company name.
   - We replace all null and NaN values with 0 for smoother processing.
   - Job location data is filtered by country using the Python `geopy` package.
   - Job titles are cleaned by removing special characters, and salaries are standardized into hourly wages.

2. **Resumes Dataset:**
   - The dataset consists of 9 attributes, and we focus on resume title, location, work experience, education, skills, and additional information.
   - Locations are filtered by country, and resume titles are cleaned by removing special characters.
   - We combine work experience, skills, and additional information to maximize the data used for model training. This helps in predicting the most suitable job roles for new resume submissions.

## Top 3 AI/ML Methods Under Consideration

a. **Random Forests:**
   - A supervised learning algorithm that excels in both classification and regression tasks.
   - Random forests combine multiple decision trees to improve prediction accuracy and avoid overfitting by averaging the outputs of several trees.

b. **Support Vector Machines (SVM):**
   - An effective supervised learning algorithm, primarily used for classification problems.
   - The goal is to find a decision boundary (hyperplane) that best separates data points into categories.

c. **K-Nearest Neighbors (KNN):**
   - A simple, instance-based learning algorithm that classifies data points by finding the closest neighboring points in feature space.
   - KNN is non-parametric and does not involve training the model beforehand, making predictions based on the proximity of data points.
