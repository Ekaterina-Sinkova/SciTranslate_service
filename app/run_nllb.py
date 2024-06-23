from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import pandas as pd
from tqdm import tqdm
import re

class NLLBModel():
    def __init__(self):
        model_name = "ascolda/nllb-200-distilled-600M_ru_en_finetuned_crystallography"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang="rus_Cyrl")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).cuda()
    
    def split_text_into_sent(self, text: str) -> list:
        """Tokenizes input text into sentences using regex"""
        sentences = []
        paragraphs = text.split("\n")

        regex = r"(?<!гр)(?<!см)(?<!им)(?<!\sо)(?<!\sч)(?<!Рис)(?<!\sг)(?<!\sр)(?<!к.ч)(?<!к. ч)(?<!\.[А-Я])(?<!\.\s[А-Я])(\.\s+[А-Я])(?!\.)"
        
        for paragraph in paragraphs:    
            r1 = re.split(regex, paragraph)
            sents = [r1[0] + "."]
            for i in range(1, len(r1), 2):
                sents.append(r1[i][-1] + r1[i + 1] + ".")
            sents[-1] = sents[-1][0:-1]
                
            result_list = []
            for string in sents:
                if "\n" in string:
                    result_list.extend(string.split("\n"))
                else:
                    result_list.append(string)
            for sent in result_list:
                sentences.append(sent)
            sentences.append("\n")
        
        sentences = [sent if re.search("[а-яА-Яa-zA-Z]", sent) else '\n' for sent in sentences]
        
        new_strings = []
        prev_was_newline = False

        for string in sentences:
            if string == '\n':
                if not prev_was_newline:  
                    new_strings.append(string)
                    prev_was_newline = True
            else:
                new_strings.append(string)
                prev_was_newline = False

        return new_strings
            
    def translate(self, text):
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device) 
        translated_tokens = self.model.generate(**inputs, forced_bos_token_id=self.tokenizer.lang_code_to_id["eng_Latn"], max_length=512)
        return self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    
    def translate_article(self, text):
        sents = self.split_text_into_sent(text)
        print(f"After tokenization we obtain {len(sents)} sentences")
        transl_sents = []
        for sent in tqdm(sents):
            if sent != '\n':
                translated_sent = self.translate(sent)
                transl_sents.append(translated_sent)
            else:
                transl_sents.append('/n')

        new_list = []
        temp_string = ''

        for string in transl_sents:
            if string == '\n':
                if temp_string:  
                    new_list.append(temp_string)
                    temp_string = ''  
            else:
                temp_string += string
                temp_string += ' '
        if temp_string:
            new_list.append(temp_string)

        df = pd.DataFrame({"eng_paragraphs": new_list[0].split('/n')})
        return df

