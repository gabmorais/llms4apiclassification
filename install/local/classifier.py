import os
from pathlib import Path

import pandas as pd
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv

available_models = {
    # Generic
    "meta-llama/Meta-Llama-3.1-70B-Instruct": "llama-3.jinja",
    "google/gemma-2-27b-it": "gemma-it.jinja",
    "mistralai/Mistral-Large-Instruct-2407": "mixtral.jinja",
    "Qwen/Qwen2-72B-Instruct": "qwen2.jinja",
    "microsoft/Phi-3-medium-128k-instruct": "phi-3.jinja",
    # Code
    "Qwen/CodeQwen1.5-7B-Chat": "qwen2.jinja",
    "Artigenz/Artigenz-Coder-DS-6.7B": "artigenz.jinja",
    "WizardLMTeam/WizardCoder-33B-V1.1": "wizard.jinja",
    # Finance
    "instruction-pretrain/finance-Llama3-8B": "deepseek.jinja",
    "ceadar-ie/FinanceConnect-13B": "llama-2.jinja"
}


def model_slug(model):
    return model.split('/')[-1].lower().replace(".", "_")


class Classifier:
    def __init__(self, model):
        load_dotenv()
        self.model = self._select_model(model)

        self.auto_model = AutoModelForCausalLM.from_pretrained(model, torch_dtype="auto", device_map="auto", token=os.getenv("HF_TOKEN"))
        self.tokenizer = AutoTokenizer.from_pretrained(model, token=os.getenv("HF_TOKEN"))
        self._select_chat_template()

    def _select_model(self, model):
        if model not in available_models.keys():
            raise ValueError(f"This model is not supported.")
        return model

    def _select_chat_template(self):
        with open(f"./chat_templates/{available_models[self.model]}") as f:
            chat_template = f.read()
            chat_template = chat_template.replace("    ", "").replace("\n", "")
        self.tokenizer.chat_template = chat_template

    def predict(self, prompt, document):
        messages = prompt + [{"role": "user", "content": document.replace("\\n", "\n")}]
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            return_tensors="pt",
            add_generation_prompt=True
        ).to(self.auto_model.device)

        outputs = self.auto_model.generate(input_ids, max_new_tokens=512, pad_token_id=self.tokenizer.eos_token_id)
        decoded = self.tokenizer.batch_decode(outputs[:, input_ids.shape[1]:], skip_special_tokens=True)
        return decoded[0].strip().lower()

    def predict_multiple(self, prompt, documents):
        predicted_labels = []
        for document in tqdm(documents.content):
            label = self.predict(prompt, document)
            predicted_labels.append(label)
        results = pd.DataFrame({model_slug(self.model): predicted_labels})
        return results

    def predict_all_prompts(self, prompts, documents, output):
        for prompt_name, system_prompt in prompts.items():
            predicted_labels = []
            for document in tqdm(documents.content, desc=prompt_name):
                label = self.predict(system_prompt, document)
                predicted_labels.append(label)
            results = pd.DataFrame({model_slug(self.model): predicted_labels})
            filename = Path(output) / f"{prompt_name}.csv"
            results.to_csv(filename, index=False, sep=';')
