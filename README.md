# Indeed_jobs_Analyst

## [Check it live](https://indeed-job-analyst.herokuapp.com/)
## Introduction
The project aims to solve one of the most challenging problems of the workforce. Find the best opportunity for candidates based on their resumes. The application also aims to prepare users with better knowledge of career improvement by getting career knowledge from career experts. Besides the recommendation system, the app equips with a career blog from Indeed.

The application will be delivered in form of a web application. Users will be able to register for their account and log in using their registered credentials. Users then can review the career blog, make comments, and interact with other users on the network (web app). The user then uploads their resume and reviews the recommendation from the system.

The web app features up-to-date technology: salting and storing passwords in encrypted tokens, SQL injection prevention, security form, object-oriented design, and secure upload (there are much more technologies that are built in, but I just want to name a few). By applying industry-standard security features, our group ensures that our applications are not only smart but also secure.

## AI Problem Statements/Use cases:
### AI Problem Statements:
As mentioned in the project description, this application aims to solve locate the best employment opportunities for candidates based on their resumes (skill sets). Without the help of AI and Machine Learning, this would be impossible to achieve (the traditional methods of hiring take too long to process applications). Our application will deliver the best math jobs for candidates based on their skill set.
### Use Cases:
A possible use case is a job recommendation system (what we are developing) where users submit their resume (education, project, skill sets) to the application. The application then uses its built-in model (machine learning model) to give user recommendation

## Supporting Data & Analysis:
-	Two data sets are considered for this project. One is indeed job listing, and the other is resumes of the applicants submitted to the indeed portal. 
1. From the Jobs_listing dataset which consists of 19 attributes (columns), we have considered 4 attributes which are, country, job title, salary formatted, and company name. 
-	Initial step is to replace all the null and NaN values to 0, which is useful for the processing of the machine learning algorithm.
-	From the country column, the job locations are given in state-wise, city wise and country-wise. We have used the Python geopy package, which is used to filter the details of a location and we have filtered based on the country in which a particular job is listed. 
-	From the job title, we have replaced all the special characters from the string and re-formatted them to a keyword that could be useful for the association later. 
-	From the salary formatted column, there are hourly based, monthly and annual incomes listed, we have used a custom function to replace the existing column and write a new one with only hourly wages posted in the column. 
2.	From the resumes submitted to the indeed portal by several job applicants, 
-	Initial step here was also to replace null and NaN values with zero. From the 9 attributes (columns) which were put in the excel sheet, we have considered resume title, location, work experience, education skills, and additional information. 
-	For the location, we have filtered based on the country which is similar to step 1.2. 
-	For the resume title, we have removed all the special characters, and numbers from the title if there are any. 
-	We have merged the 3 attributes (work experience, skills, and additional information) together to gain as much information from the user as possible for training the machine such that if a new resume is uploaded, based on the information gained from the training dataset, we can predict what job/role would be best suited for a person. 
-	From the education qualification, we have replaced and removed most of the characters that are not useful and extracted the relevant information. Whether he is a master’s degree candidate or pursuing his bachelor’s etc., 

## Top 3 AI/ML Methods/algorithms (under consideration):
The 3 ML algorithms that we plan to implement in our project are:

a. Random Forests:

Random Forest is a popular machine learning algorithm that belongs to the supervised learning technique. It can be used for both Classification and Regression problems in ML. It is based on the concept of ensemble learning, which is a process of combining multiple classifiers to solve a complex problem and improve the performance of the model.

As the name suggests, "Random Forest is a classifier that contains several decision trees on various subsets of the given dataset and takes the average to improve the predictive accuracy of that dataset." Instead of relying on one decision tree, the random forest takes the prediction from each tree, and based on the majority votes of predictions, it predicts the final output.
The greater number of trees in the forest leads to higher accuracy and prevents the problem of overfitting.

b. Support Vector Machines:

Support Vector Machine or SVM is one of the most popular Supervised Learning algorithms, which is used for Classification as well as Regression problems. However, primarily, it is used for Classification problems in Machine Learning.

The goal of the SVM algorithm is to create the best line or decision boundary that can segregate n-dimensional space into classes so that we can easily put the new data point in the correct category in the future. This best decision boundary is called a hyperplane.
SVM chooses the extreme points/vectors that help in creating the hyperplane. These extreme cases are called support vectors; hence, the algorithm is termed a Support Vector Machine. 


c. KNN:

The k-nearest neighbors (KNN) algorithm is a simple, supervised machine learning algorithm that can be used to solve both classification and regression problems. The algorithm is based on the principle that similar data points (i.e. data points that are nearby in space) tend to have similar labels (i.e. they tend to belong to the same class). Therefore, the KNN algorithm can be used to predict the label of a new data point by looking at the labels of the data points that are nearby in space. The algorithm’s learning is:

1.	Instance-based learning: Here we do not learn weights from training data to predict output (as in model-based algorithms) but use entire training instances to predict output for unseen data.
2.	Lazy Learning: The model is not learned using training data prior and the learning process is postponed to a time when prediction is requested on the new instance.
3.	Non-Parametricric: In KNN, there is no predefined form of the mapping function.

## Team Information & Tools:
a. Team members:
-	Truc Huynh (huyntl02@pfw.edu): 
1.	Roles: Software Developer/ Programmer 
2.	Build Server (Front End, Back End), Database Schema, and Data Warehouse. Deploy Machine Learning Model into the web application, Clean-up data from the users (build data pipe) that transfers user’s resume into tidy data meaningful to the application’s model. Help with data analysis, tidy the job data, etc., Develop NLP, POS
-	Rushitaa Dattuluri (dattr01@pfw.edu): 
1.	Roles: ML Engineer 
2.	Develop the Machine Learning Model for the applications, in charge of data preprocessing and overall development process.
-	Sahithi Muppiri (mupps02@pfw.edu) 
1.	Roles: ML Engineer
2.	Develop the Machine Learning Model for the applications, in charge of data preprocessing and overall development process.
b. Tools:
-	Heroku (to deploy the app)
-	PyCharm (to develop the web application)
-	Jupiter Notebook (to build machine learning model)
-	Programing languages: Python, MySQL, PostgreSQL, JavaScript, HTML, CSS
e.	Package:
-	Flask to build Full Stack Web Application and deploy the machine learning model
-	Flask_Bootstrapap for front-end development
-	Werkzeug: python library which contains many developments and debugging tools for implementation of web application gateway interface (WSGI) applications (security, password_hash, validation, secure file name, secure upload, …)
-	Flask_ckeditor: to prevent code Injection (Python, SQL, JavaScript in this application)
-	Python pandas: data analysis and manipulation tool using python programming languages
-	Python NumPy (or Numpy array): provides a high-performance multidimensional array object, and tools for working with these arrays
-	Python seaborn: for data visualization and chart
-	Python Sklearn: Python package for developing a machine learning model





### Prerequisites
What things you need to install the software and how to install them
- PyCharm Community IDE: Be More Productive: Save time while PyCharm takes care of the routine. Focus on the bigger things and embrace the keyboard-centric approach to get the most of PyCharm's many productivity features. Get Smart Assistance: PyCharm knows everything about your code. Rely on it for intelligent code completion, on-the-fly error checking and quick-fixes, easy project navigation, and much more.

### Installing
A step by step series of examples that tell you how to get a development enviroment running:
* Install [PyCharm](https://www.jetbrains.com/help/pycharm/installation-guide.html) Community Edition.

## Deployment
All the notebook can be used for research and academic basic function for Python. 

## Built With
* [PyCharm Community IDE](https://www.jetbrains.com/pycharm/download/#section=windows) 

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](). 

## Authors

* **Truc Huynh** - *Initial work* - [TrucDev](https://github.com/jackyhuynh)

## Format
my README.md format was retrieved from
* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Any acknowledgments go here
