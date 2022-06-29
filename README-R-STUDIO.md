# TEMPLATE for R Studio

## Introduction
The purpose is to create a consisten in documatation my work. Simply introduce the project that specically built with R Studio. 
I beleve the simplier the Readme file, the easier to read
- You can also keep this private and organize this GitHub as a private libary for yourself.
<img src="https://github.com/jackyhuynh/template-git-jupiter-notebook-md/blob/main/images/instruction.JPG">

## Documents/Research Paper
Link your research paper <a href="https://github.com/jackyhuynh/template-git-jupiter-notebook-md/blob/main/documents/resarch-sample.pdf">here</a> if you need

## Technology
List of technology
- R Studio
- Business Analyst
- Machine Learning
- Data Mining
- Data Visualization
- Machine Learning

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Data:
Information about the data

### Prerequisites
What things you need to install the software and how to install them:
- R CRAN Project: R is a free software environment for statistical computing and graphics. It compiles and runs on a wide variety of UNIX platforms, Windows and MacOS
- RStudio IDE: RStudio is an integrated development environment (IDE) for R. It includes a console, syntax-highlighting editor that supports direct code execution, as well as tools for plotting, history, debugging and workspace management. Click here to see more RStudio features. RStudio is available in open source and commercial editions and runs on the desktop (Windows, Mac, and Linux) or in a browser connected to RStudio Server or RStudio Server Pro (Debian/Ubuntu, Red Hat/CentOS, and SUSE Linux)

### Installing
A step by step series of examples that tell you how to get a development enviroment running:
* [Install R](https://www.r-project.org/) - If you haven't downloaded and installed R, here's how to get started.
* [R Studio IDE](https://rstudio.com/products/rstudio/#:~:text=RStudio%20Take%20control%20of%20your%20R%20code%20RStudio,tools%20for%20plotting,%20history,%20debugging%20and%20workspace%20management.) - After that choose R Studio Desktop, and the free version (unless you have the Pro install). R free version is pretty good IDE.

## Running the tests
Explain how to run the automated tests for this system:
- Start R Studio.
- Create new a project.
- Copy the data and markdown file (.rmd) into the source file. For examaple:
```
~/salePredictionSystem/markdown.rmd
~/salePredictionSystem/WholesaleCustomersData.csv
```
- you can store the WholesaleCustomersData.csv in the same folder, but it is recommeded to store in a data as below (coding standard):
```
~/salePredictionSystem/data/WholesaleCustomersData.csv
```
- Make sure to change the import code on top if you want move your data anywhere. Depend on where you download the code. Your path will definately be different from mine. Please replace the path below with your own path:
```
WholesaleData <- read.csv("~/R/DataMining/WholeSale/data/WholesaleCustomersData.csv")
# path:("~/R/DataMining/WholeSale/data/WholesaleCustomersData.csv")
```
- Please take a quick view of [import data in R](https://support.rstudio.com/hc/en-us/articles/218611977-Importing-Data-with-RStudio?mobile_site=true) if you fail to change the import code.

## Deployment
How to deploy the app. 
I will not guarantee that this aplication will work "Big data set". If you are interested in "Big(or Large) data set" please join here for [an argue](https://www.researchgate.net/post/How-much-data-is-considered-to-be-small-data-Large-data-in-data-mining) on what data set is consider a large data set in data mining.

## Built With
* [R Studio IDE](https://rstudio.com/products/rstudio/#:~:text=RStudio%20Take%20control%20of%20your%20R%20code%20RStudio,tools%20for%20plotting,%20history,%20debugging%20and%20workspace%20management.) 
* [R CRAN Project](https://www.r-project.org/) 

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
