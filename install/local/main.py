import json
from pathlib import Path

import pandas as pd

from parser import parse_cli_args
from classifier import available_models, Classifier, model_slug


def main():
    args = parse_cli_args()
    if args.list:
        list_models()
    else:
        documents = pd.read_csv(args.input, sep=';')
        with open("prompts.json", "r", encoding="utf-8") as file:
            prompts = json.load(file)
        if args.all:
            if not hasattr(args, "model"):
                run_all_models_all_prompts(prompts, documents, args.output)
            else:
                run_single_model_all_prompts(args.model, prompts, documents, args.output)
        else:
            run_single_model_single_prompt(args.model, prompts["v3"], documents, args.output)


def list_models():
    for i, model in enumerate(available_models.keys()):
        print(f"{i + 1}. {model}")


def run_single_model_single_prompt(model, prompt, documents, output):
    classifier = Classifier(model)
    df_out = classifier.predict_multiple(prompt, documents)
    if output is None:
        output = f"{model_slug(model)}.csv"
    df_out.to_csv(output, sep=';', index=False)


def run_single_model_all_prompts(model, prompts, documents, output):
    classifier = Classifier(model)
    if output is None:
        output = f"./{model_slug(model)}"
    Path(output).mkdir(parents=True, exist_ok=True)
    print(f"{'=' * 50}\n{model}\n{'=' * 50}")
    classifier.predict_all_prompts(prompts, documents, output)


def run_all_models_all_prompts(prompts, documents, output):
    if output is None:
        output = "./results"

    for model in available_models.keys():
        print(f"{'='*50}\n{model}\n{'='*50}")
        classifier = Classifier(model)
        output_dir = Path(output) / model_slug(model)
        output_dir.mkdir(parents=True, exist_ok=True)
        classifier.predict_all_prompts(prompts, documents, str(output_dir))


if __name__ == '__main__':
    main()
