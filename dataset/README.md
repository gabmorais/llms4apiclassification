# Dataset

The FinTechAPIs dataset is organized as follows :

- `filename`: Index of the dataset. References the original OpenAPI filename.
- `content`: The API description. All API descriptions are in this format:
  ```text
  TITLE: {title}
  DESCRIPTION:
      {description}
  ENDPOINTS:
      - {endpoint 1}
        {description/summary of endpoint 1}
      - {endpoint 2}
        {description/summary of endpoint 2}
      ...
  ```
- `label`: Category of the API description. Below are the categories and their distribution in the dataset.

## Distribution

| label         | count |
|:--------------|------:|
| banking       |    41 |
| payment       |    25 |
| loan-mortgage |    24 |
| user-password |    22 |
| client        |    21 |
| currency      |    20 |
| savings       |    20 |
| transfer      |    20 |
| trading       |    19 |
| blockchain    |    19 |
