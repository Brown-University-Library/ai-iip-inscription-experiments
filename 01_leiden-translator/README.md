# Project Details
This project is part of the AI Experiments by the Center for Digital Scholarship in Brown University. In particular, we work with professor Michael Satlow from Judaic Studies to experiment on automating the process of creating data entries for his Ancient Inscriptions of Israel and Palestine project. 

We began by focusing on translating transcriptions in the Leiden Convention to XML files following the EpiDoc format. We explored existing softwares and found that they were inadequate to handle the diversity of texts that loosely follow the Leiden convention. We then experimented with prompt engineering on paid services such as ChatGPT and ended up utilizing the power of in-context learning with Claude.

# Project Structure
'existing_tools' contain existing tools that were tested for this task.
'data' contains pdf, doc, image files used as input for the experiments.

'leiden2epidoc' contains the API call to translate Leiden transcriptions in the 'leiden' folder to create EpiDoc translations in the 'epidoc' folder.
'leiden2epidoc_guide' contains guideline given to Claude on how to translate Leiden to EpiDoc.
The 'leiden' folder contains text files of Leiden-convention transcriptions to be translated to EpiDoc. 
The 'epidoc' folder contains the translation performed by Claude. 
'experiments' contain existing softwares and other files that we once used to try to do the translations.

# Experiment Logs
TEI Parsing

EDEP

In-Context-Learning
The experiment logs can be found in this google document: https://docs.google.com/document/d/1tNCrmH1gcwTT9NnWwI4h-eW96YO7cYVxZV-WEB-vPwU/edit?usp=sharing

# Supporting Documents
