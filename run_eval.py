import argparse
import json
import datetime
from pathlib import Path
from sampler.chat_completion_sampler import (
    OPENAI_SYSTEM_MESSAGE_API,
    ChatCompletionSampler,
)
from simpleqa_eval import SimpleQAEval
import common

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4-turbo-preview")
    parser.add_argument("--examples", type=int, default=10)
    parser.add_argument("--debug", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    # Create results directory
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize models
    model = ChatCompletionSampler(
        model=args.model,
        system_message=OPENAI_SYSTEM_MESSAGE_API,
    )
    grader = ChatCompletionSampler(model="gpt-4-turbo-preview")

    print(f"\nUsing models:")
    print(f"Test model: {args.model}")
    print(f"Grader model: gpt-4-turbo-preview")
    
    # Run evaluation
    eval_obj = SimpleQAEval(
        grader_model=grader,
        num_examples=args.examples,
    )
    
    result = eval_obj(model)

    # Save results
    results = {
        "test_model": args.model,
        "grader_model": "gpt-4-turbo-preview",
        "num_examples": args.examples,
        "timestamp": timestamp,
        "metrics": result.metrics,
        "score": result.score
    }
    
    # Save JSON results
    json_path = results_dir / f"results_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
        
    # Save HTML report
    html_path = results_dir / f"report_{timestamp}.html"
    with open(html_path, "w") as f:
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
