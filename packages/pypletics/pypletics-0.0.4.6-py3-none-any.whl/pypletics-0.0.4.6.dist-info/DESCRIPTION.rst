# PYPLETICS PACKAGE

We created a package 'pypletics' running on Python in order to use smart functions for people analysis.  
For now, there is 3 functions:
1. introduction(): it just introduces myself
2. get_my_network(...): return an array with a plot network created from networkx package, its value and a dataframe with interlocutors and interactions.
3. get_structured_df(...): return an array very useful in order to manage copy or multi-addressees for example


*get_my_network(...)[0]:*  
![alt text](Readme_images/gmn_0.png)  

*get_my_network(...)[1].show():*  
![alt text](Readme_images/gmn_1.png)  

*get_my_network(...)[2]:*  
![alt text](Readme_images/gmn_2.png)  



*get_structured_df(...):*  
From:  

| Sender   | Addressee       |
| -------- | --------------- |
| Clément  | Florian-Jean    |
| Florian  | Jean            |
| Gaëtan   | Clément-Florian |


To:  

| Sender   | Addressee |
| -------- | --------- |
| Clément  | Florian   |
| Clément  | Jean      |
| Florian  | Jean      |
| Gaëtan   | Clément   |
| Gaëtan   | Florian   |


## ABOUT ME


```python
def introduce_myself():
    print(df.head(1))

introduce_myself()
``` 

| Name                | Company           | Job             |
| ------------------- | ----------------- | --------------- | 
| Clément Tailleur    | Octo Technology   | Data scientist  |


