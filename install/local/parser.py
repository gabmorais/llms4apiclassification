import argparse
from classifier import available_models


def parse_cli_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("input", nargs='?', type=str, default=None,
                        help="Path to the input dataset")
    parser.add_argument("--output", type=str, default=None,
                        help="Path to the output results")
    parser.add_argument("--model",
                        default=argparse.SUPPRESS,
                        const="meta-llama/Meta-Llama-3.1-70B-Instruct",
                        nargs="?",
                        choices=list(available_models.keys()),
                        help="Name of the LLM model to use.")
    parser.add_argument("--list", action="store_true",
                        help="List the available models")
    parser.add_argument("-a", "--all", action="store_true",
                        help="Run all the tests for all models")
    args = parser.parse_args()

    if not args.list:
        if not args.input:
            parser.error("The following argument is required: input")

    if not args.all and not hasattr(args, "model"):
        args.model = "meta-llama/Meta-Llama-3.1-70B-Instruct"

    return args
