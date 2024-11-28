# SimpleQA Evaluation Tool

This tool implements the evaluation methodology from the paper ["SimpleQA: Measuring short-form factuality in large language models"](https://arxiv.org/abs/2304.07513) by Jason Wei et al.

## Features

- Support for multiple LLM providers (OpenAI, OpenRouter)
- Configurable prompt templates
- Custom grader model selection
- Detailed evaluation metrics and HTML reports
- JSON export of results

## Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/simple-evals.git
cd simple-evals
pip install -r requirements.txt
```

## Configuration

Create a `config.yaml` file in the root of the project. The configuration includes details for model providers, prompt templates, and grader settings.

### Example `config.yaml`

```yaml
providers:
  openai:
    models:
      default: gpt-4o-mini
      grader: gpt-4o-mini

  openrouter:
    base_url: https://openrouter.ai/api/v1
    models:
      default: qwen/qwen1.5-72b
      grader: meta-llama/llama-2-70b-chat

prompts:
  active: "none"  # Options: "none", "confidence", "custom"
  custom_text: null  # Your custom prompt template
```

### Set up environment variables

Set your API keys for OpenAI and OpenRouter:

```bash
export OPENAI_API_KEY=your_key_here
export OPENROUTER_API_KEY=your_key_here
```

## Usage

### Basic usage

To evaluate a model, run the following command:

```bash
python run_eval.py --provider openai --model gpt-4o-mini --examples 10
```

### With custom grader

To use a custom grader model:

```bash
python run_eval.py --provider openrouter \
                  --model qwen/qwen1.5-72b \
                  --grader-provider openrouter \
                  --grader-model meta-llama/llama-3.1-8b-instruct \
                  --examples 3
```

## Command Line Arguments

- `--config`: Path to config file (default: `config.yaml`)
- `--provider`: Model provider (openai/openrouter)
- `--model`: Model to test
- `--grader-provider`: Provider for grader model
- `--grader-model`: Model to use as grader
- `--examples`: Number of examples to evaluate
- `--debug`: Show detailed debug information

## Prompt Templates

The tool supports three types of prompts:

### 1. None (direct question)

```python
SIMPLE_PROMPT = """{question}"""
```

### 2. Confidence Score

```python
CONFIDENCE_PROMPT = """Here is the question:
{question}
Please provide your best guess and a confidence score between 0% to 100% in the following JSON format:
{
"answer": "Your answer here",
"confidence_score": number
}"""
```

### 3. Custom Prompt

Configure a custom prompt in `config.yaml`:

```yaml
prompts:
  active: "custom"
  custom_text: "Question: {question}\nYour custom instructions here"
```

## Output

The tool generates two types of output:

### JSON Results

Stored in `results/results_TIMESTAMP.json`:

```json
{
  "provider": "openai",
  "test_model": "gpt-4o-mini",
  "grader_provider": "openrouter",
  "grader_model": "meta-llama/llama-2-70b-chat",
  "num_examples": 10,
  "timestamp": "20240128_123456",
  "metrics": {
    "accuracy_given_attempted": 0.75,
    "f1": 0.8
  },
  "score": 0.75
}
```

### HTML Report

Stored in `results/report_TIMESTAMP.html`:

- Detailed view of each question
- Model responses
- Grading results
- Aggregate metrics

## Metrics

The evaluation provides several metrics to assess model performance:

- **Accuracy Given Attempted**: Proportion of correct answers out of those attempted.
- **F1 Score**: Harmonic mean of precision and recall.
- **Overall Score**: Aggregate score based on the model's accuracy.
- **Is Correct Rate**: Proportion of questions correctly answered.
- **Is Incorrect Rate**: Proportion of questions incorrectly answered.
- **Not Attempted Rate**: Proportion of questions not attempted.

## Contributing

Feel free to open issues or submit pull requests. Contributions are welcome!

## Citation

If you use this tool in your research, please cite the original SimpleQA paper:

```
@article{wei2024simpleqa,
  title={Measuring short-form factuality in large language models},
  author={Wei, Jason and Karina, Nguyen and Chung, Hyung Won and Jiao, Yunxin Joy and Papay, Spencer and Glaese, Amelia and Schulman, John and Fedus, William},
  journal={arXiv preprint arXiv:2411.04368},
  year={2024},
  url={https://doi.org/10.48550/arXiv.2411.04368},
  note={Submitted on 7 Nov 2024},
  doi={10.48550/arXiv.2411.04368}
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

