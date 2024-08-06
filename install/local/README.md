# Local LLMs

## Overview

This directory contains the code and configuration files necessary to run local LLMs within a Singularity container.

## Building the Container

Use the [`api_classification.def`](api_classification.def) file to build the container. Make sure you have a working
version of [Singularity](https://docs.sylabs.io/guides/4.1/user-guide/introduction.html)
or [Apptainer](https://apptainer.org/docs/user/latest/introduction.html) installed. Execute the following command in
your terminal:

```shell
sudo -E singularity build api_classification.sif api_classification.def
```

This command will create a Singularity image file (`api_classification.sif`) that includes all the necessary
dependencies for the Python code in this directory, including CUDA drivers for GPU support. Singularity is optimized for
High-Performance Computing (HPC) environments. If you prefer to use Docker or another containerization tool, you can use
the `api_classification.def` file as a reference.

## Execution

### Setting up the Environment Variables

To run the container successfully, you first need to add a `.env` file in this directory. This file should contain
the `HF_TOKEN` environment variable, representing your HuggingFace Access Token. Make sure that you have access to all
the models below :

- [`meta-llama/Meta-Llama-3.1-70B-Instruct`](https://huggingface.co/meta-llama/Meta-Llama-3.1-70B-Instruct)
- [`google/gemma-2-27b-it`](https://huggingface.co/google/gemma-2-27b-it)
- [`mistralai/Mistral-Large-Instruct-2407`](https://huggingface.co/mistralai/Mistral-Large-Instruct-2407)
- [`Qwen/Qwen2-72B-Instruct`](https://huggingface.co/Qwen/Qwen2-72B-Instruct)
- [`microsoft/Phi-3-medium-128k-instruct`](https://huggingface.co/microsoft/Phi-3-medium-128k-instruct)
- [`Qwen/CodeQwen1.5-7B-Chat`](https://huggingface.co/Qwen/CodeQwen1.5-7B-Chat)
- [`Artigenz/Artigenz-Coder-DS-6.7B`](https://huggingface.co/Artigenz/Artigenz-Coder-DS-6.7B)
- [`WizardLMTeam/WizardCoder-33B-V1.1`](https://huggingface.co/WizardLMTeam/WizardCoder-33B-V1.1)
- [`instruction-pretrain/finance-Llama3-8B`](https://huggingface.co/instruction-pretrain/finance-Llama3-8B)
- [`ceadar-ie/FinanceConnect-13B`](https://huggingface.co/ceadar-ie/FinanceConnect-13B)

### Running the Container

The Singularity *postscript* section is configured to execute the [`main.py`](main.py) Python script. To run the
container, use the following command:

```shell
singularity run --nv api_classification.sif [arguments]
```

Replace `[arguments]` with any arguments you need to pass to `main.py`. Here is the list of available arguments and
their descriptions:

- `input` (required): Path to the input dataset (**semicolon separated `.csv`**). The dataset needs to follow the same
  structure as the [`fintechapis.csv`](fintechapis.csv) file.
- `--output` (optional): Path to the output file generated. By default, the output file is a `.csv` file containing all
  the responses from the LLM. If you use the `--all` option, the output file is a **directory**.
- `--list` (optional): List all the supported open-source large language models (HuggingFace).
- `--model` (optional): Name of the model to use. Default is `meta-llama/Meta-Llama-3.1-70B-Instruct`.
- `--all` (optional): Run classification with all prompts and all models. This can be a long process! (more than 12
  hours) Otherwise, if this argument is not passed, only the `v3` prompt is tested.

To run all models with all prompt using the Singularity container, use the following command:

```shell
singularity run --nv api_classification.sif fintechapis.csv --all --output results/first_test/
```

In Linux, you can continue to run this process even after exiting the shell using the `nohup` command. It also lets you
redirect any output to a log file.

```shell
nohup singularity run --nv api_classification.sif fintechapis.csv --all --output results/first_test/ > results/first_test/log.txt &
```

## Prompts

The `prompts.json` file contains all prompts used in our experiments. These prompts are built by combining multiple
prompt engineering techniques in the hope to find the optimal prompt for API classification. All prompt sections and
their correspondence in `prompts.json` are described below.

- *Base Instructions (Ins)*: The instructions are structured in a numbered list and enclosed within `<instructions>`
  tags. In these instructions, the *user* asks the model to read, analyze, and classify the provided API description,
  and to return the category in a specific format.
- *Category Description (CD)*: This prompt section gives the LLM definitions for the categories into which API documents
  should be classified, providing domain-specific and contextual data to the LLMs. Category descriptions are placed
  before the base instructions (*Ins*) and added inside `<categories>` tags.
- *Chain of Thought (CoT)*: This part of the prompt instructs the model to output its rationale and selected category
  inside `<thinking>` and `<category>` tags, respectively. When incorporating the *CoT* approach in our prompt, we
  replace the fourth step of the base instructions.
- *Few-Shot Prompting (FS)*: Few-shot prompting involves including examples in the prompt to guide the model's responses
  and improve its understanding of the task by leveraging its in-context learning capabilities. In our experiments, we
  included three examples of accurate API classifications through back-and-forth interactions between the *user* and
  *assistant* roles.

| Prompt Sections | Correspondence in `prompts.json` |
|:----------------|:--------------------------------:|
| *Ins*           |               `v1`               |
| *CD+Ins*        |               `v2`               |
| *CD+Ins+FS*     |               `v3`               |
| *Ins+CoT*       |               `v4`               |
| *CD+Ins+CoT*    |               `v5`               |
| *CD+Ins+CoT+FS* |               `v6`               |
