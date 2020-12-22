# TMA-Project
Implementation of an *IoT Anomaly Detection* solution by applying machine learning (ML) algorithms onto captured network flow.

This project was developed in the scope of the Network Traffic Monitoring and Analysis (TMA) course at Universitat Politècnica de Catalunya (UPC).

# Table of contents
- [The problem](#The-problem)
- [The solution](#The-solution)
- [Technical approach](#Technical-approach)
  - [Choosing flow fields](#Choosing-flow-fields)
  - [Choosing algorithms](#Choosing-algorithms)
- [Files description](#Files-description)
- [Future improvements](#Future-improvements)
- [References](#References)

# The problem
As IoT is growing exponentially in the last decade (2010-2020), devices seem to be entering the market on an unsecure fashinon: insecure components, unnecessary open ports and insuficient logging mechanisms. Attacks onto IoT are more common as the days pass, but little do we know about them in society.

# The solution
We propose a way to detect if attacks are being made onto a network by reading captured traffic and classifying it in consonance to its possible attack matching.

We made use of the [Aposemat IoT-23](https://www.stratosphereips.org/datasets-iot23) dataset which is composed by 21GB of data from packet captures onto an IoT based network.

The idea is to train a ML model to classify the traffic and then allow the user to make use of it through an API to tag each flow and get a summary of the classification results.

# Technical approach
## Choosing flow fields
The Aposemat IoT-23 database contains 20 captures that share a common fields format with more than 15 fields. Of those, we decided to take into consideration the following 7:
1. *id.orig_p*:  Source port
2. *id.resp_p*:  Destination port
3. *missed_bytes*:  Lost bytes
4. *orig_pkts*:  Flow packets
5. *orig_ip_bytes*:  Flow bytes
6. *resp_pkts*:  Response packets
7. *resp_ip_bytes*:  Response bytes
## Choosing algorithms
After some study onto algorithms, the following classiffication was achieved:
|       Algorithm      	| Acc. (%) 	| Time (s) 	| Tier 	|
|:--------------------:	|:--------:	|:--------:	|:----:	|
| kNN                  	|   99.64  	|    37    	|   B  	|
| Centroids            	|   41.18  	|    1.7   	|   C  	|
| Gaussian Naïve Bayes 	|   64.14  	|    2.5   	|   B  	|
| **LDA**                  	|   **99.44**  	|    **4.3**   	|   **A**  	|
| Logistic Regression  	|   89.19  	|   45.3   	|   B  	|
| **Decision Trees**       	|   **99.65**  	|    **3.3**   	|   **A**  	|
| Bagging with kNN     	|   99.54  	|    284   	|   B  	|
| **Random Forest**        	|   **99.48**  	|   **10.4**   	|   **A**  	|
| Ada Boost            	|   79.97  	|     98   	|   C  	|
| Gradient Boosting    	|   99.15  	|    214   	|   B  	|
| SVC - linear         	|     -    	| too much 	|   D  	|
| SVC - poly           	|     -    	| too much 	|   D  	|
| SVC - rbf            	|     -    	| too much 	|   D  	|
| MLP                  	|     -    	| too much 	|   D  	|

It can be seen that some of them performed better than others onto our power-limited hardware. From those which got an A tier classification, we chose to work with the *Decision Trees* algorithm.

# Files description
- [algorithms](https://github.com/albovy/TMA-Project/tree/main/algorithms) : folder containing codes to help choose algorithms
- [api.py](https://github.com/albovy/TMA-Project/blob/main/api.py) : executable API through ```python3 api.py``` command
- [data_try.txt](https://github.com/albovy/TMA-Project/blob/main/data_try.txt) : sample of a user input to the API
- [model/train_data](https://github.com/albovy/TMA-Project/blob/main/model/train_data) : trained ML model
- [requirements.txt](https://github.com/albovy/TMA-Project/blob/main/requirements.txt) : all of the python library requirements. Import through ```pip3 install -r requirements.txt```
- [train.py](https://github.com/albovy/TMA-Project/blob/main/train.py) : training code to create the model. Execute with: ```python3 train.py datasetFile modelName```

# Future improvements
- Improve hardware
- Find more datasets on IoT
- Get a higher quality dataset
- Make the model adapt to the hosting network
- Try new algorithms and compare results
- Use a more generic group of IoT devices

# References
Stratosphere Laboratory. ***A labeled dataset with malicious and benign IoT network traffic.*** January 22th. Agustin Parmisano, Sebastian Garcia, Maria Jose Erquiaga. [Aposemat IoT-23](https://www.stratosphereips.org/datasets-iot23)