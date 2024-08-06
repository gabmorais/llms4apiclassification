# LLMS Selection
This folder contains the files used during our analysis. Below, we explain how we proceeded. 

## LLMs Identification
We relied on two LLMs leaderboards: [Evalplus](https://evalplus.github.io/leaderboard.html) and [LMSYS Chatbot Arena Leaderboard](https://chat.lmsys.org/?leaderboard).

We extract the ranks on 2024-06-25.
For the Evalplus learderboard, we extracted the "Average" rank.
For the LMSYS ChatBot Arena Leaderboard, we extracted the "Full Leaderboard" rank and considered the models based on their MMLU score[cf. csv from LMSYS](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard/blob/main/leaderboard_table_20240623.csv).

Below the steps we followed:

1. Extraction of the 30 first lines of each leaderboard (Total extracted from both leaderboards: 73).
2. Exclusion of models taged as preview.
3. Exclusion of duplicated models, i.e., present in both leaderbords.
4. Exclusion of previous versions of the same model present in the leaderboards (e.g., exclude version 1.5 of a modelA with version 2 in the list)
5. Ignoring various models entries with different parameters numbers, we kept only the models and major versions.
6. Ignoring access modes, i.e., different access for proprietary LLMs. For proprietary LLMs the choice of the plan will be done during analysis, based on costs.
7. Start the analysis of the remaining 34 models.

## Analysis of the LLMs candidates
### Gathering information
For the remaining models, we gathered the information bellow (see models_identification.xlsx):

1. LLM type (decoder-only, encoder-only, encoder-decoder).
2. Release date in the leaderbord.
3. Local installation or remote access (throughout an API).
3.1. For remote access, mainly proprietary one, assess individual access allowed (not restricted to professional purposes)
3.2. For proprietary LLMs, the price and query conditions (prompt limitations)
4. Safetensor version present.
4.1. Do not need external code (e.g., trust_remote_code=true)
5. Compatible with Hugginface Transformers library.
6. GPU needed.
7. Provide an installation guide.

### Preselection
We applied the rules bellow to select the models to be installed (see candidates.xlsx models analysis sheet).
1) They must be decoder-only pre-trained LLMs.
2) Their release date must not be before 2023-12-01.
3) LLM provider must allow unrestricted on-premise installation
or remote access (through an API).
4) LLMs to be installed must have a safetensors version to
avoid security breaches.
5) They must be compatible with the Transformers library.
6) LLMs to be installed must be compatible with the target
infrastructure (using a maximum of 8 GPUs with 80GB
HBM2E).

We pre-selected 16 general and code domain LLMs (cf. candidates.xlsx selected sheet).

## Final selection
We added two models of the finance domain. 
We discarded 2 code models because of install failures.
The final selection comprise models (cf. final.xlsx).

We excluded two models because they exposed errors during installation and could not be replaced by a remote version.
We replaced DeepSeek and DeepSeek-Coder local installation version by the remote version because of our infrastructure limitation, even if in these models documentation it was stated they required GPU power in the limits of our infrastructure. 