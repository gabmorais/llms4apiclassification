import os
import time
from pathlib import Path

import openai
import pandas as pd
from dotenv import load_dotenv
from google.generativeai import GenerationConfig
from tqdm import tqdm
import google.generativeai as genai

available_models = ["gpt-4o-mini", "gemini-1.5-flash", "deepseek-chat", "deepseek-coder"]


def model_slug(model):
    return model.split('/')[-1].lower().replace(".", "_")


class Classifier:
    def create(self, model):
        if model == "gpt-4o-mini":
            return GPTClassifier(model)
        if model == "gemini-1.5-flash":
            return GeminiClassifier(model)
        if model in ["deepseek-chat", "deepseek-coder"]:
            return DeepSeekClassifier(model)
        raise ValueError(f"This model is not supported.")


class BaseClassifier:
    def __init__(self, model):
        load_dotenv()
        self.model = model

    def predict(self, prompt, document):
        raise NotImplementedError

    def predict_multiple(self, prompt, documents):
        predicted_labels = []
        for document in tqdm(documents.content):
            label = "EXCEPTION"
            for tries in range(2):
                try:
                    label = self.predict(prompt, document)
                    break
                except Exception:
                    time.sleep(5)
            predicted_labels.append(label)
        results = pd.DataFrame({model_slug(self.model): predicted_labels})
        return results

    def predict_all_prompts(self, prompts, documents, output):
        for prompt_name, prompt in prompts.items():
            predicted_labels = []
            for document in tqdm(documents.content, desc=prompt_name):
                label = "EXCEPTION"
                for tries in range(2):
                    try:
                        label = self.predict(prompt, document)
                        break
                    except Exception:
                        time.sleep(5)
                predicted_labels.append(label)
            results = pd.DataFrame({model_slug(self.model): predicted_labels})
            filename = Path(output) / f"{prompt_name}.csv"
            results.to_csv(filename, index=False, sep=';')


class GPTClassifier(BaseClassifier):
    def predict(self, prompt, document):
        messages = prompt + [{"role": "user", "content": document}]
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=512
        )
        return response.choices[0].message.content.strip().lower()


class GeminiClassifier(BaseClassifier):
    def _gemini_convert_prompt(self, prompt):
        new_prompt = []
        roles = {"user": "user", "assistant": "model"}
        for message in prompt:
            new_prompt.append({"role": roles[message["role"]], "parts": [message["content"]]})
        return new_prompt

    def predict(self, prompt, document):
        messages = self._gemini_convert_prompt(prompt + [{"role": "user", "content": document.replace("\\n", "\n")}])
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        client = genai.GenerativeModel(
            model_name=self.model,
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ]
        )
        chat_session = client.start_chat(history=messages)
        config = GenerationConfig(max_output_tokens=512)
        response = chat_session.send_message(document, generation_config=config)
        return response.text.strip().lower()


class DeepSeekClassifier(BaseClassifier):
    def predict(self, prompt, document):
        messages = prompt + [{"role": "user", "content": document.replace("\\n", "\n")}]
        client = openai.OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=512
        )
        return response.choices[0].message.content.strip().lower()
