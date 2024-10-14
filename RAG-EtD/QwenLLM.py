from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, BitsAndBytesConfig
from threading import Thread
from abc import ABC
from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from peft import AutoPeftModelForCausalLM
from torch import torch
import json
import re

#Qwen2(not Qwen or Qwen2.5) needs to be aligned with Langchain, and the following code ensures streaming output during alignment.

device = "cuda"
class Qwen(LLM, ABC):
     max_token: int = 2048
     temperature: float = 0.4
     default_temperature: float = 0.05
     top_p = 0.8
     history_len: int = 20
     tokenizer: object = None
     model: object = None
     callbackers: List = []

     def __init__(self):
         super().__init__()

     @property
     def _llm_type(self) -> str:
         return "Qwen"

     def load_model(self, model_name_or_path=None,is_lora=False,quantization_type=False):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        quantization_config = None
        if(quantization_type == "fp4" or quantization_type == "nf4"):
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type=quantization_type,
                bnb_4bit_use_double_quant=True
            )
        elif(quantization_type == "fp8" or quantization_type == "nf8"):
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True,
                bnb_8bit_compute_dtype=torch.float16,
                bnb_8bit_quant_type=quantization_type,
                bnb_8bit_use_double_quant=True
            )
        if(not is_lora):
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name_or_path,
                torch_dtype="auto",
                device_map="auto",
                quantization_config=quantization_config     
            ).eval()
        else:
            self.model = AutoPeftModelForCausalLM.from_pretrained(
                model_name_or_path,
                device_map="auto",
                torch_dtype="float16",
                quantization_config=quantization_config,
                trust_remote_code=True
            ).half().merge_and_unload().cuda().eval()
     @property
     def _history_len(self) -> int:
         return self.history_len
     def set_history_len(self, history_len: int = 10) -> None:
         self.history_len = history_len
     def set_stream_callbackers(self, callbackers: List) -> None:
         self.callbackers = callbackers
     def format_history_str2list(self, history_str: str):
        history_list = []
        avaliable_prefix = ["AI","Human","System","Observation","Thought","Action"]
        history_2way = []
        for i in range(len(avaliable_prefix)):
            prefix = avaliable_prefix[i]
            prefix_pos = [m.start() for m in re.finditer(prefix, history_str)]
            for i in range(len(prefix_pos)):
                history_2way.append((prefix,prefix_pos[i]))
        history_2way.sort(key=lambda x:x[1])
        history_2way.append(("End",len(history_str)))

        #处理：第一个AI前的部分都是System
        for i in range(len(history_2way)):
            if history_2way[i][0] == "Human":
                history_2way=history_2way[i:]
                history_2way.insert(0,("System",0))
                break;
        #print(history_2way)
        for i in range(len(history_2way)-1):
            history_list.append({
                "role": history_2way[i][0],
                "content": history_str[history_2way[i][1]+len(history_2way[i][0])+2:history_2way[i+1][1]]
            })
        return history_list
     def preformat_history_list(self, history_list: List):
        #将所有role转为小写，AI转写为assistant,human转为user，并移除除了["system", "user", "assistant", "observation"]外的所有role
        final_history_list = []
        for i in range(len(history_list)):
            history_list[i]["role"] = history_list[i]["role"].lower()
            if history_list[i]["role"] == "ai":
                history_list[i]["role"] = "assistant"
            if history_list[i]["role"] == "human":
                history_list[i]["role"] = "user"
            if history_list[i]["role"] == "observation":
                history_list[i]["role"] = "user"
            if history_list[i]["role"] == "assistant":
                temp_content=history_list[i]["content"]
                matched_jsoncontent = re.findall(r"```json(.*)```", temp_content.replace('\n',''))
                if matched_jsoncontent:
                    history_list[i]["content"] = json.dumps(json.loads(matched_jsoncontent[0]),indent=2, ensure_ascii=False)
            if history_list[i]["role"] in ["system", "user", "assistant"]:
                final_history_list.append(history_list[i])
        return final_history_list
     def  _find_num_of_tokens(self, text: str,find_str: str):
        return text.count(find_str)
     def _call(
         self,
         prompt: str,
         stop: Optional[List[str]] = None,
         run_manager: Optional[CallbackManagerForLLMRun] = None,
     ) -> str:
         messages = self.preformat_history_list(self.format_history_str2list(prompt))
         text = self.tokenizer.apply_chat_template(
             messages,
             tokenize=False,
             add_generation_prompt=True
         )
         model_inputs = self.tokenizer([text], return_tensors="pt").to(device)
         streamer = TextIteratorStreamer(tokenizer=self.tokenizer, skip_prompt=True, timeout=60.0, skip_special_tokens=True)
         kwargs = dict(
             input_ids=model_inputs.input_ids,
             max_new_tokens=512,
             forced_bos_token_id=90,
             use_cache=True,
             streamer=streamer
         )
         thread = Thread(target=self.model.generate, kwargs=kwargs)
         thread.start()
         response = ""
         for new_text in streamer:
            for callbacker in self.callbackers:
                callbacker(new_text)
            response += new_text
            if len(response) <= 1:
                continue
            if response[0] != "{":
                print("Start token not found, upgrade temperature and restart")
                return """
AI: ```json
{
    "action":"Final Answer",
    "action_input":"Start token not found, upgrade temperature and restart"
}
```
"""
            if "}" in response:
                if self._find_num_of_tokens(response,"{") == self._find_num_of_tokens(response,"}"):
                    #Possible Bug:if llm returned { without },it will nerver break.
                    #But it will nerver happen in RAG Tasks.
                    break
         finalAns = "AI: \n```json\n"+response+"\n```"
         return finalAns
     @property
     def _identifying_params(self) -> Mapping[str, Any]:
         """Get the identifying parameters."""
         return {"max_token": self.max_token,
                 "temperature": self.temperature,
                 "top_p": self.top_p,
                 "history_len": self.history_len}