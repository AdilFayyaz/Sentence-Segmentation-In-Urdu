Install the Urduhack module
"""

#Install UrduHack
!pip install urduhack[tf]

"""Reading the Text File

---
The file is read line by line and the text is appended to a string text. To normalize the data to remove inconsistencies multiple continuous spaces in the text are removed

"""

from google.colab import files
uploaded = files.upload()
f = open('test_file_incorrect.txt')
text=""
line = f.readlines()
for i in line:
    print(i)
    text+=i
    text+="\n"

#Normalization of data
#Remove multiple spaces if exist in the original text
text = " ".join(text.split())

"""Sentence Segmentation Code

---

The sentence segmentation code does not use the urduhack module.However, in essence the main inspiration of the logic behind the program is the same as the urduhack's sentence tokenizer. However, the provided solution is a more efficient one. 

---
UrduHack tokenizes text into sentences but leaves inconsistencies in the sentences formed.The set of End of Sentence words and conjunctions is limited and therefore not accurate. There are extra checks that can be avoided and worked around of. The sentences are not divided between question marks and dashes in a single go, leading to extra computation power being used. Moreover, the word tokenizer function in urduhack does not split the words correctly into a list. Instead, a complete word is split into two words leading to issues afterwards.


---
A straight forward solution is used in the program that follows. The text initially removes quotation marks from a copy of the text because quotation marks do not signify the end of a sentence. For a sentence consisting of quotation marks, it will always be followed by another punction mark such as dash, question mark or exclamation mark which will signify the end of the sentence. The primary reason to remove the quotation marks is because they sometimes cause inconsistencies when the last word of a sentence is tokenized. 

---
The program splits the text into words, these words are then iterated over one by one. In the Urdu Language, a limited or specific pattern exists which is that the words on which the sentence ends have the last character as one of the following (??,??,??,??,??).
A list of possible end of words for a sentence are defined at the top of the program. These are the words on which a sentence can end. Hence, a comparison is made for each word tokenized earlier, if the word exists in this set of end words there is a possibility that a sentence ends here. However, if the word is followed by a conjunction(from the set of conjunctions defined) the sentence does not end after the word. Two additional checks are also added, which are that the next word does not belong from the end words list, and the next words starting character is not a comma (??). If satisfied a dash is appended to the text.
*Note: Comma can exist at the start of the next word or the end of the current word, and in this way both cases are satisfied. * 
Lastly, the text formed is split into sentences using a regex that divides text on the basis of (!, ?? ,??). To remove certain inconsistencies, extra spaces at the start and end of the program are also removed.

"""

URDU_EOS_SET = ['??????????', '??????????', '????????', '????????', '??????', '??????????', '????', '??????????', '????', '??????????', '??????????', '????',
                       '??????', '??????', '??????', '??????', '????','????????', '??????', '??????????', '??????','??????','??????','??????','??????????','??????','??????','??????','??????','????????'
                       ] #Delimiters included in urduhack + additional ones
URDU_CONJUNCTIONS = ['??????????', '????', '????', '????', '??????','??????','??????????', '????????', '??????', '????', '????', '????????', '????', '????',
                      '????', '????', '????','??????????????', '????????', '???????????? ???? ???? ', '????????????', '????????','????????', '??', '????????','??????','????????','????','????????','????????','????????','????????',
                     '??????????'
                      ] #Delimiters included in urduhack + additional ones


import re
text_posn =0
copytext=text
#Remove quotation marks
copytext= copytext.replace('???','')
copytext= copytext.replace('???','')

og_words_list = copytext.split(" ") #split the sentences into words
index = 0 
for word in og_words_list:     #for every word in sentence
  text_posn+=len(word)+1  #text posn var for each char posn count
  
  try:
    #If there is a comma/dash at the end of the sentence then this condition will prevent it to go into this block of code
    #End word characters 
    if word[-1] == "??" or word[-1] == "??" or word[-1]== "??" or word[-1] == "??" or word[-1] == "??" or word[-1]=="??":  
    
      if index+1 == len(og_words_list):
        break
      else:
        if word in URDU_EOS_SET and og_words_list[index + 1] not in URDU_CONJUNCTIONS and og_words_list[index+1] not in URDU_EOS_SET and og_words_list[index+1][0] != '??':
          #End of Sentence found. Append a dash
          copytext=copytext[:text_posn] + '??' + copytext[text_posn:]
          text_posn+=1
  except:
    print("Index Out of Bound")
  index+=1
  

new_sents = re.split('!|??|??',copytext)
print("\n\n" + "Number of Sentences are: " , len(new_sents) )
cc =0 #Counter for number of sentences
for n in new_sents:
  print(n)
  if new_sents[cc]:
    if new_sents[cc][-1] == " ":
      new_sents[cc] = new_sents[cc][:-1:]
    if new_sents[cc][0] == " ":
      new_sents[cc] = new_sents[cc][1:]
  cc+=1

"""Import the UrduHack Module"""

import urduhack
from urduhack.tokenization import sentence_tokenizer
from urduhack.tokenization import word_tokenizer

urduhack.download()

"""Accuracy Function

---
The Accuracy Function takes a list of sentences as a parameter. The correct file is loaded and is split into sentences of its own. After normalizing the data read the sentences computed by the above algorithm are compared with the sentences formed from the accurate passage. 

---
To compute the accuracy, for each sentence in the correct sentences, a sentence is searched in the new sentences formed. The last word of each sentence is matched with the other sentences last word. This is followed by another comparison that checks if the next three characters of the next sentence is also the same as the other sentences next three characters. If both these conditions are satisfied, the sentence is marked as a successful split. 
To save computation power, once a sentence in the new_sents has been found to be tokenized correctly, its index is added to a list of correct sentences, so that it's not iterated over again. Moreover, this saves the possibility of incorrectly matching sentences repeatedly again. 


"""

def Sentence_Segment_Accuracy(new_sents):
  import re
  upld = files.upload()

  f = open('test_file_correct.txt') 
  acc_text = f.read()

  #Remove quotation marks
  acc_text = acc_text.replace('???','')
  acc_text = acc_text.replace('???','')

  list_acc_text=re.split('??|??',acc_text)

  count = 0

  #Normalization of the read correct text
  for x in list_acc_text:
    if list_acc_text[count]:
      if list_acc_text[count][-1] == '??' or list_acc_text[count][-1] == '!':
        list_acc_text[count] = list_acc_text[count][:-1:]

    list_acc_text[count]=list_acc_text[count].lstrip()
    list_acc_text[count]=list_acc_text[count].rstrip()
    count +=1

  #new_sents = sentence_tokenizer(text)  #URDUHACK ACCURACY
  checked_sents=[]
  success = 0
  corr_sent_count = 0
  #For every correct sentence tokenized
  for corr_sent in list_acc_text:
    #Split the sentence into words
    corr_words = corr_sent.split()
    
    if not corr_words:
      break
    att_sent_count = 0 
    #For every sentence in the attempted sentence tokenization
    for att_sent in new_sents:
      #If the sentence has not already been checked 
      if att_sent_count not in checked_sents:
        
        att_words = att_sent.split()
        
        try:
          #If the last word of both the sentences matches
          if att_words[-1] == corr_words[-1]:

            #Remove quotation marks (Normalization)
            new_sents[att_sent_count] = new_sents[att_sent_count].replace('???','')
            new_sents[att_sent_count] = new_sents[att_sent_count].replace('???','')

            try:
              #Check the next 3 characters of the word followed by the sentence. If they match, the sentence had been segmented correctly
              if new_sents[att_sent_count + 1][0] ==  list_acc_text[corr_sent_count+1][0] and new_sents[att_sent_count + 1][1] ==  list_acc_text[corr_sent_count+1][1] and new_sents[att_sent_count + 1][2] ==  list_acc_text[corr_sent_count+1][2]:  #First letter of the sentence after matches
                print("Successful Split " + att_sent)
                success += 1
                checked_sents.append(att_sent_count)
                break
            except:
              print("Index out of bound")
        except:
          print("Index out of bound")
      att_sent_count += 1
      
    corr_sent_count+=1


  return (success/len(list_acc_text))*100

"""Compare Accuracy"""

success_personal = Sentence_Segment_Accuracy(new_sents)   #Attempted Algorithm accuracy
success_urduhack = Sentence_Segment_Accuracy(sentence_tokenizer(text))  #UrduHack algorithm accuracy

"""Results"""

print("Accuracy of proposed Algorithm: " , success_personal)
print("Accuracy of UrduHack Algorithm: ", success_urduhack)

"""References -
The articles have been taken from the following sources:
1. https://hamariweb.com/articles/128921 (article exists in the urdu_corpus file)
2. https://hamariweb.com/articles/128862 (article exists in the urdu_corpus file)
3. https://www.bbc.com/urdu/pakistan-56467036

"""