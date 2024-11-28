# SimpleQA Evaluation Tool

This is a simplified and easy-to-use version of OpenAI's SimpleQA evaluation framework for factual accuracy in language models. Based on the paper [SimpleQA: Measuring short-form factuality in large language models](https://cdn.openai.com/papers/simpleqa.pdf).

## Features

- Easy to set up and run
- Automatic dataset download
- Detailed HTML reports
- JSON metrics output
- Support for any OpenAI models
- Extensible for other LLM providers

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/simpleqa-eval.git
cd simpleqa-eval
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-key-here'
```

4. Run evaluation:
```bash
python run_eval.py --model gpt-4-turbo-preview --examples 10
```

## Command Line Arguments

- `--model`: Model to test (default: gpt-4-turbo-preview)
- `--examples`: Number of examples to test (default: 10)
- `--debug`: Show detailed metrics output

## Output

The tool generates two types of output in the `results/` directory:
- JSON file with metrics (`results_[timestamp].json`)
- HTML report with detailed examples (`report_[timestamp].html`)

## Metrics

- `accuracy_given_attempted`: Accuracy for questions where the model made an attempt
- `f1`: F1 score combining accuracy and attempt rate
- Additional detailed metrics in debug mode

## How It Works

1. The tool uses the SimpleQA dataset to test factual knowledge
2. Each answer is evaluated using GPT-4 as a grader
3. Answers are classified as:
   - CORRECT: Fully correct answer
   - INCORRECT: Contains factual errors
   - NOT_ATTEMPTED: No clear answer given

## Credits

This is based on the work from the SimpleQA paper by OpenAI:
- Authors: Jason Wei, Nguyen Karina, Hyung Won Chung, Yunxin Joy Jiao, Spencer Papay, Amelia Glaese, John Schulman, William Fedus
- Paper: https://cdn.openai.com/papers/simpleqa.pdf

## License

MIT License

