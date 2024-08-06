import os
import random

import torch


def set_seed(seed=42):
    """
    Fix all random seeds we use for reproducibility.
    """
    # Python random seed
    random.seed(seed)

    # PyTorch random seed
    torch.manual_seed(seed)

    # If you are using CUDA
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if you are using multi-GPU.

    # PyTorch backend settings
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    # Python hash seed
    os.environ["PYTHONHASHSEED"] = str(seed)


def assert_verbose_allclose(tensor1, tensor2, rtol=1e-05, atol=1e-08, max_print=5):
    """
    Assert that two tensors are element-wise equal within a tolerance, providing detailed information about mismatches.

    Parameters:
    tensor1 (torch.Tensor): First tensor to compare.
    tensor2 (torch.Tensor): Second tensor to compare.
    rtol (float): Relative tolerance.
    atol (float): Absolute tolerance.
    max_print (int): Maximum number of mismatched elements to print.

    Raises:
    AssertionError: If the tensors are not all close within the given tolerance.
    """
    # Check if the shapes of the tensors match
    if tensor1.shape != tensor2.shape:
        raise AssertionError("Input tensors must have the same shape.")

    # Calculate the difference between the tensors
    diff = torch.abs(tensor1 - tensor2)

    # Determine the tolerance
    tolerance = atol + rtol * torch.abs(tensor2)

    # Find mismatched elements
    mismatched = diff > tolerance

    # Get the indices of mismatched elements
    mismatched_indices = torch.nonzero(mismatched)

    # Count the number of mismatched elements
    num_mismatched = mismatched.sum().item()

    # Check if all elements are close
    all_close = num_mismatched == 0

    # Raise AssertionError with detailed information if there are mismatches
    if not all_close and num_mismatched > 1:
        mismatch_details = [f"Number of mismatched elements: {num_mismatched}"]
        print_count = min(max_print, num_mismatched)
        for index in mismatched_indices[:print_count]:
            i = tuple(index.tolist())
            mismatch_details.append(
                f"Mismatch at index {i}: tensor1[{i}] = {tensor1[i]}, tensor2[{i}] = {tensor2[i]}"
            )
        if num_mismatched > max_print:
            mismatch_details.append(
                f"... and {num_mismatched - max_print} more mismatched elements."
            )

        raise AssertionError("\n".join(mismatch_details))
