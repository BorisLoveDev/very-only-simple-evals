import argparse
import json
import datetime
import os
from pathlib import Path
from utils.config import load_config
from sampler.chat_completion_sampler import OpenAISampler
from sampler.openrouter_sampler import OpenRouterSampler
from simpleqa_eval import SimpleQAEval
import common

def get_sampler(provider: str, model: str, config: dict, is_grader: bool = False):
    if provider == "openai":
        return OpenAISampler(
            model=model,
        )
    elif provider == "openrouter":
        return OpenRouterSampler(
            model=model,
            base_url=config["providers"]["openrouter"]["base_url"],
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument("--provider", default="openai", help="Provider to use (openai/openrouter)")
    parser.add_argument("--model", help="Override model from config")
    parser.add_argument("--grader-provider", default="openai", help="Provider for grader (openai/openrouter)")
    parser.add_argument("--grader-model", help="Override grader model from config")
    parser.add_argument("--examples", type=int, default=10)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    
    # Get provider configs
    provider_config = config["providers"][args.provider]
    grader_provider_config = config["providers"][args.grader_provider]
    
    # Get model names
    test_model = args.model or provider_config["models"]["default"]
    grader_model = args.grader_model or grader_provider_config["models"]["grader"]
    
    print(f"\nUsing models:")
    print(f"Provider: {args.provider}")
    print(f"Test model: {test_model}")
    print(f"Grader provider: {args.grader_provider}")
    print(f"Grader model: {grader_model}")
    
    # Initialize test model and grader
    model = get_sampler(args.provider, test_model, config)
    grader = get_sampler(args.grader_provider, grader_model, config, is_grader=True)
    
    # Run evaluation
    eval_obj = SimpleQAEval(
        grader_model=grader,
        num_examples=args.examples,
    )
    
    result = eval_obj(model)

    # Create results directory
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Prepare model configuration info
    model_config = {
        "test": {
            "provider": args.provider,
            "model": test_model
        },
        "grader": {
            "provider": args.grader_provider,
            "model": grader_model
        }
    }
    
    # Save results with updated model information
    results = {
        "timestamp": timestamp,
        "models": model_config,
        "evaluation": {
            "num_examples": args.examples,
            "metrics": result.metrics,
            "score": result.score
        }
    }
    
    # Save JSON results with pretty printing
    json_path = results_dir / f"results_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    # Save HTML report
    html_path = results_dir / f"report_{timestamp}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(common.make_report(result))

    # Print results
    if args.debug:
        print("\nDetailed metrics:")
        for name, value in result.metrics.items():
            print(f"{name}: {value:.3f}")
    else:
        print("\nAggregate Metrics:")
        print(f"Accuracy Given Attempted: {result.metrics.get('accuracy_given_attempted', 0):.3f}")
        print(f"F1 Score: {result.metrics.get('f1', 0):.3f}")
        print(f"Overall Score: {result.score:.3f}")

    print(f"\nResults saved to:")
    print(f"JSON: {json_path}")
    print(f"HTML Report: {html_path}")


if __name__ == "__main__":
    main()
