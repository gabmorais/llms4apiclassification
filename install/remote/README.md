# Remote LLMs

## Overview

This directory contains the code and configuration files necessary to run remote LLMs using public APIs.

## Requirements

The provided code was tested with **Python 3.11**. Use the [`requirements.txt`](requirements.txt) file to install the
required dependencies. Execute the following command in
your terminal:

```shell
pip install -r requirements.txt
```

## Execution

### Setting up the Environment Variables

To run the code successfully, you first need to fill the `.env` file in this directory. This file should contain
the `OPENAI_API_KEY`, `GOOGLE_API_KEY` and `DEEPSEEK_API_KEY` environment variables, representing your OpenAI, Google
Gemini and DeepSeek API keys. Make sure you have access to these models before running the code.

- [`gpt-4o-mini`](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/)
- [`gemini-1.5-flash`](https://deepmind.google/technologies/gemini/flash/)
- [`deepseek-chat`](https://www.deepseek.com/) and [`deepseek-coder`](https://www.deepseek.com/)

### Running the Code

> [!WARNING]
> Running the provided code will deduct credits from your API key.

To run the code, execute the command below:

```shell
python main.py [arguments]
```

Replace `[arguments]` with any arguments you need to pass to `main.py`. Here is the list of available arguments and
their descriptions:

- `input` (required): Path to the input dataset (**semicolon separated `.csv`**). The dataset needs to follow the same
  structure as the [`fintechapis.csv`](fintechapis.csv) file.
- `--output` (optional): Path to the output file generated. By default, the output file is a `.csv` file containing all
  the responses from the LLM. If you use the `--all` option, the output file is a **directory**.
- `--list` (optional): List all the supported open-source large language models (HuggingFace).
- `--model` (optional): Name of the model to use. Default is `gpt-4o-mini`.
- `--all` (optional): Run classification with all prompts and all models. This can be a long process! (more than 12
  hours) Otherwise, if this argument is not passed, only the `v3` prompt is tested.

To run all models with all prompt, use the following command:

```shell
python main.py fintechapis.csv --all --output results/first_test/
```

In Linux, you can continue to run this process even after exiting the shell using the `nohup` command. It also lets you
redirect any output to a log file.

```shell
nohup python main.py fintechapis.csv --all --output results/first_test/ > results/first_test/log.txt &
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

## Batch API

OpenAI now allows running multiple chat completion queries in batches, which reduces the cost of operation by half.
The [`gpt_batch`](gpt_batch) folder encloses the batch files used to query GPT for each prompt.
A [python script](gpt_batch/batch.py) is also included to decode the resulting batch outputs. For example, to decode
batch output files in the `batch_output` directory into result files, you would execute

```shell
python batch.py batch_ouptut results
```

More information about batches are available [here](https://platform.openai.com/docs/guides/batch).