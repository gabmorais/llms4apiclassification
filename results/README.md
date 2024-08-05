# Results

This directory shows the raw data obtained following our experiments.

## File Structure

- `{model}/`: Each base folder contains the model's results.
- `{model}/run{i}/`: Each `model` folder stores the results of 5 classification runs.
- `{model}/run{i}/v{j}.csv`: Each `run` folder contains 6 `.csv` files of the LLM response for every prompt and every
  document of the dataset. Here is the filename-prompt correspondence we used:
    - `v1`: *Ins* prompt.
    - `v2`: *CD+Ins* prompt.
    - `v3`: *CD+Ins+FS* prompt.
    - `v4`: *Ins+CoT* prompt.
    - `v5`: *CD+Ins+CoT* prompt.
    - `v6`: *CD+Ins+CoT+FS* prompt.
