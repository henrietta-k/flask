# Materiality Assessment Program 

Within the realm of ESG practices, companies can determine whether certain topics are "material" or not; that is: "Materiality is the threshold at which ESG issues determined by the board are sufficiently important to investors and other stakeholders that they should be reported" ([Source](https://www.hkex.com.hk/Listing/Sustainability/ESG-Academy/ESG-in-Practice/Materiality-Assessment?sc_lang=en#:~:text=A%20materiality%20assessment%20was%20conducted,of%20identification%2C%20prioritization%20and%20validation.)). 
The process of determining these topics is quite tedious, especially in conducting surveys and interviews with relevant stakeholders. These surveys, in particular, require many questions spanning all topics to be answered. 

## Why use this program?
This flask application takes in ESG topics specified by a company and conducts a survey based on questions from the Global Reporting Initiative. However, this application makes the process much more efficient by eliminating topics deemed irrelevant (based on quantitative metrics such as the differences in scores between topics) as the survey progresses. The program even terminates early if answering more questions will not affect the overall result. That way, much fewer questions will be needed to be answered by stakeholders. 

The program also takes in the estimated cost of each topic as well as a limit on how many topics the company wants to focus on. After calculating the tradeoffs between external and internal costs and benefits of each material topic, the program produces two different sets of rankings of topics: one that considers the cost, and one based purely on the score that each topic received. 

## Usage

This program was created using Flask and a Python backend. It includes a SQL database to store the user's information. It is currently deployed on PythonAnywhere and can be accessed [here](https://materialassessmentprogram.pythonanywhere.com/start).

