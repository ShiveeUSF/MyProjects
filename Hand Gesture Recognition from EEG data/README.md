# Recognize hand gesture using EEG signals

Patients who have lost hand function due to amputation or neurological disabilities have a hard time performing simple tasks that involve lifting or grasping an object. Restoring a patient's ability to perform basic activities of daily life with a brain-computer interface (BCI) prosthetic device could greatly increase their independence and quality of life. 

Electroencephalography (EEG) is a noninvasive and inexpensive means of monitoring brain activity that holds potential to solve this problem but there are a few challenges. The relationship between brain activity and EEG signals is complex and poorly understood outside of specific laboratory tests. Moreover due to the high velocity nature of EEG recordings, the data used in such a classification are often large and may take a long time to process on a local, non-distributed computer. 
Methodology
In order to identify hand motions on the basis of EEG signals we developed several machine learning models such as Logistic Regression Classifier, Random Forest Classifier, Linear Support Vector Machine Classifier, and Gradient Boosted Trees. 

In order to speed up execution, we explored the use of a Distributed Computing architecture for storage and processing of EEG data. Our architecture had following components- Amazon’s Simple  Storage  Service  (AWS  S3),  MongoDB, and  Apache  Spark,  for data  storage,  management  and  processing  respectively. 
Results
We found that processing these data on a distributed system results in much faster classification times (e.g., 726 seconds versus 3925 seconds) without limiting accuracy. 
We found that tree based models such as Random Forest and Gradient Boosted Tree are best performers in classifying EEG data. Random Forest model outperformed the others, with an average AUC score of 0.85

Execution time
Local system: 726 s
Distributed system: 3925 s 

AUC score:
Random Forest: 0.85



