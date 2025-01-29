import sys
import os
from dotenv import load_dotenv
from openai import OpenAI
import csv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv('CHATGPT_API'))
csv.field_size_limit(sys.maxsize)

sr_data = list(csv.reader(open('data/SR_Referents.csv', newline=''), delimiter=',', quotechar='"'))

prompt1_header = '''I will give you a transcription of a text about an enslaved native American. A human coder extracted information about an individual mentioned in the text into the data entries you can find below the transcription. \
                  Check if the extracted data can be found or inferred from somewhere in the transcription text. The text often mention multiple individuals, and thus there could be multiple bits of information that correctly fit the data field. Grade it correct if the human-coded data match any information mentioned. \
                  If the human coder left an entry empty or inputted NULL, trust their decision and keep it as it is (empty or NULL) in your output. Here is an example.\
                  Example 1 Text Transcription———\n\
                  3011	Court records	Other	1677-12-13 00:00:00	<p dir="ltr">[173] Zebulon Udall bound over to this Court being accused for getting Dr. Taylors Indyan mayde with Child. Shee not being yet brought to bed both to bee bound over to the next Court. [&hellip;] [174] Dr. Taylour saith hee heard Roger Toweenesend confesse the same on his death bed.</p>\n\n\
                  Example 1 Extracted Data———\n\
                  name_first: Dr.\n\
                  name_last: Traylor\n\
                  tribes: NULL\n\
                  sex: Male\n\
                  age_text: men\n\
                  age_category: Adult\n\
                  origins: NULL\n\
                  occupations: Plumber\n\
                  races: White\n\
                  enslavement_status: free person ▸ enslaver or owner\n\
                  relationships: "owner of": {"id": 8299, "last": "", "name": " ", "first": ""}\n\n\
                  Example 1 Consistency Check———\n\
                  name_first: "Dr." is not a first name\n\
                  name_last: "Traylor" is a misspelling of the data in the source, "Taylour"\n\
                  tribes: NULL\n\
                  sex: Correct\n\
                  age_text: Correct, 'men' gives information about the person's age\n\
                  age_category: Correct, 'Adult' can be inferred from 'men'\n\
                  origins: NULL\n\
                  occupations: Doctor, not plumber\n\
                  races: Correct, although there is no explicit evidence that the person is white, whiteness is presumed from the historical context\n\
                  enslavement_status: Correct\n\
                  relationships: Correct\n\n\
                  Example 2 Text Transcription———\n\
                  <p>RUn away the 3d Instant from <em>Judith Vincent</em> in Monmouth County, in New-Jersey, an Indian Man, named Stoffels, speaks good English, about Forty years of age, he is a House Carpenter, a Cooper; a Wheelwright, and is a good Butcher also. There is also two others gone along with him, one being half Indian and half Negro, the other a Mulatto about 30 years old, &amp; plays upon the violin, and has it with him. Whoever takes up &amp; secures said Fellow so that he may be had again shall have Forty Shillings as a Reward and all reasonable Charges paid by the said Judith Vincent.</p><p>N.B. It is supposed' they are all gone together in a Canow towards Connecticut or Rhode-Island.</p>\n\n
                  Example 1 Extracted Data———\n\
                  name_first: \n\
                  name_last: \n\
                  tribes: NULL\n\
                  sex: Male\n\
                  age_text: about 30\n\
                  age_category: Adult\n\
                  origins: NULL\n\
                  occupations: [""Arts and Entertainment""]\n\
                  races: [""Multi-racial""]\n\
                  enslavement_status: [""unfree person ▸ liminal ▸ self-emancipated""]\n\
                  relationships: {""ran away with"": {""id"": 2409, ""last"": "" "", ""name"": ""Stoffels "", ""first"": ""Stoffels""}}\n\n\
                  Example 1 Consistency Check———\n\
                  name_first: \n\
                  name_last: \n\
                  tribes: NULL\n\
                  sex: Correct, inferred from 'Man'\n\
                  age_text: Correct, there is a mention of an individual 'about 30'\n\
                  age_category: Correct, inferred from 'about 30'\n\
                  origins: NULL\n\
                  occupations: Correct, inferred from 'plays upon the violin'\n\
                  races: Correct, inferred from 'Mulatto'\n\
                  enslavement_status: Correct\n\
                  relationships: Correct\n\n\
                  Now check the error for the transcription and data below.\n\n\
                  Task Text Transcription———\n'''

def get_prompt(row) -> str:
    return prompt1_header + row[16] + "\n\nTask Extracted Data———" + \
      "\nname_first: " + row[1] + "\nname_last: " + row[2] + "\ntribes: " + row[3] + "\nsex: " + row[4] + "\nage_text: " + row[5] + "\nage_category: " + row[6] + "\origins: " + row[7] + "\noccupations: " + row[8] +  "\nraces: " + row[9] + "\enslavement_status: " + row[10] + "\nrelationships: " + row[11]\
      + "\n\nTask Consistency Check———\n"

# print(get_prompt(sr_data[1]))

def get_review(row) -> str:
  p1_response = client.chat.completions.create(
    model = "gpt-4",
    temperature = 0.1,
    max_tokens = 3000,
    messages = [
      {"role": "user", "content": get_prompt(row)}
    ]
  )

  print(p1_response.choices[0].message.content)

  prompt2_header = 'Below is a review of a data entry. Could you use the information from the data review to create a JSON file? It must have fields "name_first", "name_last", "tribes", "sex", "age_text", "age_category", "origins", "occupations", "races", "enslavement_status", "relationships" and have the value 0 if the field is empty or NULL, 1 if it is correct, and -1 if it is incorrect or needs review.\n\n\
    It must also have a field called "notes" at the very end: if any of the other fields received the value -1, please copy the data review information for those fields into the "notes" field.'

  p2_response = client.chat.completions.create(
    model = "gpt-4",
    temperature = 0.1,
    max_tokens = 3000,
    messages = [
      {"role": "user", "content": prompt2_header + p1_response.choices[0].message.content}
    ]
  )

  print(p2_response.choices[0].message.content)
  return p2_response.choices[0].message.content

def grade_rows(start_row : int, num_rows : int):
    data = []
    for i in range(num_rows):
        row = start_row + i
        json_string = get_review(sr_data[row])
        grade_dict = json.loads(json_string)
        grade_dict["referent_uuid"] = sr_data[row][0]
        data.append(grade_dict)

    with open('results/sr_consistency_grades_notes.csv', 'a', newline='') as csvfile:
        fieldnames = ["referent_uuid","name_first","name_last","tribes","sex","age_text","age_category","origins","occupations","races","enslavement_status","relationships","notes"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()
        writer.writerows(data)

def grade_n_more_rows(n : int):
    row_num = len(list(csv.reader(open('results/sr_consistency_grades_notes.csv', newline=''), delimiter=',', quotechar='"')))
    grade_rows(row_num, n)

if __name__=="__main__":
    grade_n_more_rows(1)