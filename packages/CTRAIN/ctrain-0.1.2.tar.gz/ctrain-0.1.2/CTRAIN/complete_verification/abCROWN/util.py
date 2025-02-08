import torch

import yaml
from yaml import Loader

from io import StringIO

STD_CONF = '''
general:
  device: cuda  # Select device to run verifier, cpu or cuda (GPU).
  seed: 100  # Random seed.
  conv_mode: patches  # Convolution mode during bound propagation: "patches" mode (default) is very efficient, but may not support all architecture; "matrix" mode is slow but supports all architectures.
  deterministic: false  # Run code in CUDA deterministic mode, which has slower performance but better reproducibility.
  double_fp: false  # Use double precision floating point. GPUs with good double precision support are preferable (NVIDIA P100, V100, A100, H100; AMD Radeon Instinc MI50, MI100).
  loss_reduction_func: sum  # When batch size is not 1, this reduction function is applied to reduce the bounds into a scalar (options are "sum" and "min").
  sparse_alpha: true  # Enable/disable sparse alpha.
  sparse_interm: true  # Enable/disable sparse intermediate bounds.
  save_adv_example: false  # Save returned adversarial example in file.
  eval_adv_example: false  # Whether to validate the saved adversarial example.
  show_adv_example: false  # Print the adversarial example.
  precompile_jit: false  # Precompile jit kernels to speed up after jit-wrapped functions, but will cost extra time at the beginning.
  complete_verifier: bab  # Complete verification verifier. "bab": branch and bound with beta-CROWN or GCP-CROWN; "mip": mixed integer programming (MIP) formulation; "bab-refine": branch and bound with intermediate layer bounds computed by MIP; "Customized": customized verifier, need to specially def by user.
  enable_incomplete_verification: true  # Enable/Disable initial alpha-CROWN incomplete verification (disable this can save GPU memory).
  csv_name: null  # Name of .csv file containing a list of properties to verify (VNN-COMP specific).
  results_file: out.txt  # Path to results file.
  root_path: ''  # Root path of the specification folder if using vnnlib.
  deterministic_opt: false  # Try to ensure that the bound parameters always match with the optimized bounds.
  graph_optimizer: 'Customized("custom_graph_optimizer", "default_optimizer")'  # BoundedModule model graph optimizer function name. For examples of customized graph optimizer, please see the config files for the gtrsb benchmark in VNN-COMP 2023.
  buffer_has_batchdim: false  # In most cases, the shape of buffers in an ONNX graph do not have a batch dimension. Enabling this option will help load models with a buffer object that has a batch dimension. In most case this can be inferred in the verifier automatically, and this option is not needed.
  save_output: true  # Save output for test.
  output_file: out.pkl  # Path to the output file.
  return_optimized_model: false  # Return the model with optimized bounds after incomplete verification is done.
model:
  name: null  # Model name. Will be evaluated as a python statement.
  path: null  # Load pretrained model from this specified path.
  onnx_path: null  # Path to .onnx model file.
  onnx_path_prefix: ''  # Add a prefix to .onnx model path to correct malformed csv files.
  cache_onnx_conversion: false  # Cache the model converted from ONNX.
  onnx_quirks: null  # Load onnx model with quirks to workaround onnx model issue. This string will be passed to onnx2pytorch as the 'quirks' argument, and it is typically a literal of a python dict, e.g., "{'Reshape': {'fix_batch_size: True'}}".
  input_shape: null  # Specified input shape of the model.Usually the shape can be automatically determined from dataset or onnx model, but some onnx models may have an incompatible shape (without batch dim). You can specify shape explicitly here.The shape should be (-1, input_shape) like (-1, 3, 32, 32) and -1 indicates the batch dim.
  onnx_loader: default_onnx_and_vnnlib_loader  # ONNX model loader function name. Can be the Customized() primitive; for examples of customized model loaders, please see the config files for the marabou-cifar10 benchmark in VNN-COMP 2021 and the Carvana benchmark in VNN-COMP 2022.
  onnx_optimization_flags: none  # Onnx graph optimization config.
  onnx_vnnlib_joint_optimization_flags: none  # Joint optimization that changes both onnx model and vnnlib.
  check_optmized: false  # Check the optimized onnx file instead the original one when converting to pytorch. This is used when input shape is changed during optimization.
  flatten_final_output: false  # Manually add a flatten layer at the end of the model.
  optimize_graph: null  # Specify a custom function for optimizing the graph on the BoundedModule.
  with_jacobian: false  # Indicate that the model contains JacobianOP.
data:
  start: 0  # Start from the i-th property in specified dataset.
  end: 10000  # End with the (i-1)-th property in the dataset.
  select_instance: null  # Select a list of instances to verify.
  num_outputs: 10  # Number of classes for classification problem.
  mean: 0.0  # Mean vector used in data preprocessing.
  std: 1.0  # Std vector used in data preprocessing.
  pkl_path: null  # Load properties to verify from a .pkl file (only used for oval20 dataset).
  dataset: null  # Dataset name (only if not using specifications from a .csv file). Dataset must be defined in utils.py. For customized data, checkout custom/custom_model_data.py.
  data_idx_file: null  # A text file with a list of example IDs to run.
specification:
  type: lp  # Type of verification specification. "lp" = L_p norm, "box" = element-wise lower and upper bound provided by dataloader.
  robustness_type: verified-acc  # For robustness verification: verify against all labels ("verified-acc" mode), or just the runnerup labels ("runnerup" mode), or using a specified label in dataset ("speicify-target" mode, only used for oval20). Not used when a VNNLIB spec is used.
  norm: .inf  # Lp-norm for epsilon perturbation in robustness verification (1, 2, inf).
  epsilon: null  # Set perturbation size (Lp norm). If not set, a default value may be used based on dataset loader.
  epsilon_min: 0.0  # Set an optional minimum perturbation size (Lp norm).
  vnnlib_path: null  # Path to .vnnlib specification file. Will override any Lp/robustness verification arguments.
  vnnlib_path_prefix: ''  # Add a prefix to .vnnlib specs path to correct malformed csv files.
  rhs_offset: null  # Adding an offset to RHS.
solver:
  batch_size: 64  # Batch size in bound solver (number of parallel splits).
  auto_enlarge_batch_size: false  # Automatically increase batch size based on --batch_size in bab if current VRAM usage < 45%%, only support input_split.
  min_batch_size_ratio: 0.1  # The minimum batch size ratio in each iteration (splitting multiple layers if the number of domains is smaller than min_batch_size_ratio * batch_size).
  use_float64_in_last_iteration: false  # Use double fp (float64) at the last iteration in alpha/beta CROWN.
  early_stop_patience: 10  # Number of iterations that we will start considering early stop if tracking no improvement.
  start_save_best: 0.5  # Start to save best optimized bounds when i > int(iteration*start_save_best). Early iterations are skipped for better efficiency.
  bound_prop_method: alpha-crown  # Bound propagation method used for incomplete verification and input split based branch and bound.
  init_bound_prop_method: same  # Bound propagation method used for the initial bound in input split based branch and bound. If "same" is specified, then it will use the same method as "bound_prop_method".
  prune_after_crown: false  # After CROWN pass, prune verified labels before starting the alpha-CROWN pass.
  optimize_disjuncts_separately: false  # If set, each neuron computes seperate bounds for each disjunct. If set, do not set prune_after_crown=True.
  crown:
    batch_size: 1000000000  # Batch size in batched CROWN.
    max_crown_size: 1000000000  # Max output size in CROWN (when there are too many output neurons, only part of them will be bounded by CROWN).
    relu_option: adaptive  # Options for specifying the the way to initialize CROWN bounds for ReLU function.
  alpha-crown:
    alpha: true  # Disable/Enable alpha crown.
    lr_alpha: 0.1  # Learning rate for the optimizable parameter alpha in alpha-CROWN bound.
    iteration: 100  # Number of iterations for alpha-CROWN incomplete verifier.
    share_alphas: false  # Share some alpha variables to save memory at the cost of slightly looser bounds.
    lr_decay: 0.98  # Learning rate decay factor during alpha-CROWN optimization. Need to use a larger value like 0.99 or 0.995 when you increase the number of iterations.
    full_conv_alpha: true  # Enable/disable the use of independent alpha for conv layers.
    max_coeff_mul: .inf  # Maximum coefficient value in the optimizable parameters for BoundMul.
    matmul_share_alphas: false  # Check alpha sharing for matmul.
    disable_optimization: []  # A list of the names of operators which have bound optimization disabled.
  invprop:
    apply_output_constraints_to: []  # Includes the output constraint in the optimization of linear layers. Can be a comma seperated list of layer types (e.g. "BoundLinear"), layer names (e.g. "/input.7") or "all". This will disable patch mode for listed conv layers. When set, --optimize_disjuncts_separately must be set, too, if the safety property uses a disjunction.
    tighten_input_bounds: false  # Tighten input bounds using output constraints. If set, --apply_output_constraints_to should contain "BoundInput" or the corresponding layer name.
    best_of_oc_and_no_oc: false  # Computes bounds of each layer both with and without output constraints. The best of both is used. Increases the runtime, but may improve the bounds.
    directly_optimize: []  # A list of layer names whose bounds should be directly optimized for. IBP is disabled for these layers. Should only be needed for backward verification (approximation of input bounds) where the first linear layer defines the cs and should be optimized.
    oc_lr: 0.1  # The learning rate for the dualized output constraints.
    share_gammas: false  # Shares gammas across neurons in the optimized layer.
  beta-crown:
    lr_alpha: 0.01  # Learning rate for optimizing alpha during branch and bound.
    lr_beta: 0.05  # Learning rate for optimizing beta during branch and bound.
    lr_decay: 0.98  # Learning rate decay factor during beta-CROWN optimization. Need to use a larger value like 0.99 or 0.995 when you increase the number of iterations.
    optimizer: adam  # Optimizer used for alpha and beta optimization.
    iteration: 50  # Number of iteration for optimizing alpha and beta during branch and bound.
    enable_opt_interm_bounds: false  # Enable optimizing intermediate bounds for beta-CROWN, only used when mip refine for now.
    all_node_split_LP: false  # When all nodes are split during Bab but not verified, using LP to check.
  forward:
    refine: false  # Refine forward bound with CROWN for unstable neurons.
    dynamic: false  # Use dynamic forward bound propagation where new input variables may be dynamically introduced for nonlinearities.
    max_dim: 10000  # Maximum input dimension for forward bounds in a batch.
    reset_threshold: 1.0  # Reset the start layer if timeout neurons are above the threshold.
  multi_class:
    label_batch_size: 32  # Maximum target labels to handle in alpha-CROWN. Cannot be too large due to GPU memory limit.
    skip_with_refined_bound: true  # By default we skip the second alpha-CROWN execution if all alphas are already initialized. Setting this to avoid this feature.
  mip:
    parallel_solvers: null  # Number of multi-processes for mip solver. Each process computes a mip bound for an intermediate neuron. Default (None) is to auto detect the number of CPU cores (note that each process may use multiple threads, see the next option).
    solver_threads: 1  # Number of threads for echo mip solver process (default is to use 1 thread for each solver process).
    refine_neuron_timeout: 15  # MIP timeout threshold for improving each intermediate layer bound (in seconds).
    refine_neuron_time_percentage: 0.8  # Percentage (x100%%) of time used for improving all intermediate layer bounds using mip. Default to be 0.8*timeout.
    early_stop: true  # Enable/disable early stop when finding a positive lower bound or a adversarial example during MIP.
    adv_warmup: true  # Disable using PGD adv as MIP refinement warmup starts.
    mip_solver: gurobi  # MLP/LP solver package (SCIP support is experimental).
bab:
  initial_max_domains: 1  # Number of domains we can add to domain list at the same time before bab. For multi-class problems this can be as large as the number of labels.
  max_domains: .inf  # Max number of subproblems in branch and bound.
  decision_thresh: 0  # Decision threshold of lower bounds. When lower bounds are greater than this value, verification is successful. Set to 0 for robustness verification.
  timeout: 360  # Timeout (in second) for verifying one image/property.
  timeout_scale: 1  # Scale the timeout for development purpose.
  max_iterations: -1  # Maximum number of BaB iterations.
  override_timeout: null  # Override timeout.
  pruning_in_iteration: true  # Disable verified domain pruning within iteration.
  pruning_in_iteration_ratio: 0.2  # When ratio of positive domains >= this ratio, prunning in iteration optimization is open.
  sort_targets: false  # Sort targets before BaB.
  batched_domain_list: true  # Disable batched domain list. Batched domain list is faster but picks domain to split in an unsorted way.
  optimized_interm: ''  # A list of layer names that will be optimized during branch and bound, separated by comma.
  recompute_interm: false  # Recompute all the intermediate bounds during BaB.
  sort_domain_interval: -1  # If unsorted domains are used, sort the domains every sort_domain_interval iterations.
  vanilla_crown: false  # Use vanilla CROWN during BaB.
  cut:
    enabled: false  # Enable cutting planes using GCP-CROWN.
    implication: false  # Enable neuron implications.
    bab_cut: false  # Enable cut constraints optimization during BaB.
    method: null  # Cutting plane generation method (unused, for future extensions).
    lr: 0.01  # Learning rate for optimizing cuts.
    lr_decay: 1.0  # Learning rate decay for optimizing betas in GCP-CROWN.
    iteration: 100  # Iterations for optimizing betas in GCP-CROWN.
    bab_iteration: -1  # Iterations for optimizing betas in GCP-CROWN during branch and bound. Set to -1 to use the same number of iterations without cuts.
    lr_beta: 0.02  # Learning rate for optimizing betas in GCP-CROWN.
    number_cuts: 50  # Maximum number of cuts that we want to add.
    topk_cuts_in_filter: 1000  # Only keep top K constraints when filtering cuts.
    batch_size_primal: 100  # Batch size when calculate primals, should be negative correlated to number of unstable neurons.
    max_num: 1000000000  # Maximum number of cuts.
    patches_cut: false  # Enable GCP-CROWN optimization for intermediate layer bounds in patches mode.
    cplex_cuts: false  # Build and save mip mps models, let cplex find cuts, and use found cuts to improve lower bounds.
    cplex_cuts_wait: 0  # Wait a bit after cplex warmup in seconds, so that we tend to get some cuts at early stage of branch and bound.
    cplex_cuts_revpickup: true  # Enable/disable the inverse order domain pickout when cplex is enabled.
    cut_reference_bounds: true  # Enable/disable using reference bounds when GCP-CROWN cuts are used.
    fix_intermediate_bounds: false  # Fix intermediate bounds when GCP-CROWN cuts are used.
  branching:
    method: kfsb  # Branching heuristic. babsr is fast but less accurate; fsb is slow but most accurate; kfsb is usually a balance; kfsb-intercept-only is faster but may lead to worse branching; sb is fast smart branching which relies on the A matrix.
    candidates: 3  # Number of candidates to consider when using fsb or kfsb. More candidates lead to slower but better branching.
    reduceop: min  # Reduction operation to compute branching scores from two sides of a branch (min or max). max can work better on some models.
    enable_intermediate_bound_opt: false  # Enable optimizing intermediate bounds for during bab.
    branching_input_and_activation: false  # Branching input domains and relu domains (experimental).
    branching_input_and_activation_order: [input, relu]  # Order of branching input domains and relu domains (experimental).
    branching_input_iterations: 30  # Number of iterations to run input split before we run relu split.
    branching_relu_iterations: 50  # Number of iterations to run relu split before we run input split.
    nonlinear_split:
      method: shortcut  # Branching heuristic for the general nonlinear functions.
      branching_point_method: uniform  # For general non-linear functions, the method for choosing the branching point.
      num_branches: 2  # Number of branches for nonlinear branching.
      filter: false  # KFSB-like filtering in general nonlinear branching.
      filter_beta: false  # Use beta in the KFSB-like filtering.
      filter_batch_size: 10000  # Batch size for filtering.
      filter_iterations: 25  # Number of iterations for filtering.
      use_min: false  # Use min instead of mean to aggregate the branching scores of multiple branches.
      loose_tanh_threshold: null  # Set a threshold for tanh/sigmoid to use a different relaxation when the pre-activation bounds are too loose.
      dynamic_bbps: false  # Decide branching points dynamically by BBPS.
      dynamic_options: [uniform, three_left, three_right]  # Different options of branching points.
      # branching_point_node: ''  # The node type using pre-computed branching points.
      # branching_point_db: []  # Path to pre-computed branching points.
    input_split:
      enable: false  # Branch on input domain rather than unstable neurons.
      enhanced_bound_prop_method: alpha-crown  # Specify a tighter bound propagation method if a problem cannot be verified after --input_split_enhanced_bound_patience.
      enhanced_branching_method: naive  # Specify a branching method if a problem cannot be verified after --input_split_enhanced_bound_patience.
      enhanced_bound_patience: 100000000.0  # Time in seconds that will use an enhanced bound propagation method (e.g., alpha-CROWN) to bound input split sub domains.
      attack_patience: 100000000.0  # Time in seconds that will start PGD attack to find adv examples during input split.
      adv_check: 0  # After the number of visited nodes, we will run adv_check in input split.
      split_partitions: 2  # How many domains to split to for each dimension at each time. By default, it is 2. In very few limited experimental cases, can change to larger numbers.
      sb_margin_weight: 1.0  # Weight for the margin term in the sb heuristic.
      sb_sum: false  # Use sum for multiple specs in sb.
      bf_backup_thresh: -1  # Threshold for using the SB score as the backup when the brute force score is too bad.
      bf_rhs_offset: 0  # An offset on RHS used in computing the brute force heuristic.
      bf_iters: 1000000000.0  # Number of iterations to use brute force.
      bf_batch_size: 100000  # A special batch size for brute force.
      bf_zero_crossing_score: false  # A zero crossing score in BF.
      touch_zero_score: 0  # A touch-zero score in BF.
      ibp_enhancement: false  # Use IBP bounds to enhance.
      catch_assertion: false  # Catch assertion (when the bounds are extremely loose).
      compare_with_old_bounds: false  # Compare bounds after an input split with bounds before the split and take the better one.
      update_rhs_with_attack: false  # Run attack during input split and update RHS. BaB does not stop even if any counterexample is found.
      sb_coeff_thresh: 0.001  # Clamp values of coefficient matrix (A matrix) for sb branching heuristic.
      sort_index: null  # The output index to use for sorting domains in the input split.
      sort_descending: true  # Sort input split domains in an ascending/descending way.
      show_progress: false  # Show progress during input split.
  attack:
    enabled: false  # Enable beam search based BaB-attack.
    beam_candidates: 8  # Number of candidates in beam search.
    beam_depth: 7  # Max additional level of splits to expand during beam search in BaB-Attack.
    max_dive_fix_ratio: 0.8  # Maximum ratio of fixed neurons during diving in BaB-Attack.
    min_local_free_ratio: 0.2  # Minimum ratio of free neurons during local search in BaB-Attack.
    mip_start_iteration: 5  # Iteration number to start sub-MIPs in BaB-Attack.
    mip_timeout: 30.0  # Sub-MIP timeout threshold.
    adv_pool_threshold: null  # Minimum value of difference when adding to adv_pool; default `None` means auto select.
    refined_mip_attacker: false  # Use full alpha crown bounds to refined intermediate bounds for sub-MIPs.
    refined_batch_size: null  # Batch size for full alpha-CROWN to refined intermediate bounds for mip solver attack (to avoid OOM), default None to be the same as mip_multi_proc.
attack:
  pgd_order: before  # Run PGD attack before/after/during incomplete verification, only during input bab, or skip it.
  pgd_steps: 100  # Steps of PGD attack.
  pgd_restarts: 30  # Number of random PGD restarts.
  pgd_batch_size: 100000000  # Batch size for number of restarts in PGD.
  pgd_early_stop: true  # Enable/disable early stop PGD when an adversarial example is found.
  pgd_lr_decay: 0.99  # Learning rate decay factor used in PGD attack.
  pgd_alpha: auto  # Step size of PGD attack. Default (auto) is epsilon/4.
  pgd_alpha_scale: false  # Scale PGD alpha according to data_max-data_min.
  pgd_loss_mode: null  # Loss mode for choosing the best delta.
  enable_mip_attack: false  # Use MIP (Gurobi) based attack if PGD cannot find a successful adversarial example.
  adv_saver: default_adv_saver  # Customized saver of adverserial examples.
  early_stop_condition: default_early_stop_condition  # Customized early stop condition.
  adv_example_finalizer: default_adv_example_finalizer  # Customized generation of adversarial examples, margins computation, etc.
  pgd_loss: default_pgd_loss  # Customized pgd loss.
  cex_path: ./test_cex.txt  # Save path for counter-examples.
  attack_mode: PGD  # Attack algorithm, including vanilla PGD and PGD with diversified output (Tashiro et al.), and GAMA loss (Sriramanan et al.).
  attack_tolerance: 0.0  # Tolerance of floating point error when checking whether attack is successful or not.
  attack_func: attack_with_general_specs  # The specific customized attack.
  gama_lambda: 10.0  # Regularization parameter in GAMA attack.
  gama_decay: 0.9  # Decay of regularization parameter in GAMA attack.
  check_clean: false  # Check clean prediction before attack.
  input_split:
    pgd_steps: 100  # Steps of PGD attack in input split before branching starts.
    pgd_restarts: 30  # Number of random PGD restarts in input split before branching starts.
    pgd_alpha: auto  # Step size (alpha) in input split before branching starts.
  input_split_enhanced:
    pgd_steps: 200  # Steps of PGD attack in enhanced pgd attack in input split.
    pgd_restarts: 500000  # Number of random PGD restarts in enhanced pgd attack in input split.
    pgd_alpha: auto  # Step size (alpha) in enhanced pgd attack in input split.
  input_split_check_adv:
    pgd_steps: 5  # Steps of PGD attack in input split after each branching.
    pgd_restarts: 5  # Number of random PGD restarts in input split after each branching.
    pgd_alpha: auto  # Step size (alpha) in input split after each branching.
    max_num_domains: 10  # Maximum number of domains for running attack during input split.
debug:
  view_model: false  # Print more detailed model information for analyis.
'''


def get_abcrown_standard_conf(timeout=600, no_cores=28):
    """
    Generates the standard configuration for abCROWN.
    This function reads the standard configuration from a predefined string,
    updates the device setting based on the available hardware, and sets the 
    timeout and number of parallel solvers.
    
    Args:
      timeout (int, optional): The timeout value for the BAB solver in seconds. Defaults to 600.
      no_cores (int, optional): The number of parallel solvers to use. Defaults to 28.
    
    Returns:
      (dict): The updated standard configuration dictionary.
    """
    f = StringIO(STD_CONF)

    std_conf = yaml.load(f, Loader=Loader)
    
    device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
    
    std_conf['general']['device'] = device
    std_conf['bab']['timeout'] = timeout
    std_conf['solver']['mip']['parallel_solvers'] = no_cores
    
    return std_conf


def write_adversarial_robustness_vnnlib(filename, initial_comment, input_domain, ground_truth, n_classes=10):
    """
    Create a vnnlib specification for an adversarial robustness property.

    The function writes the following to the specified file:
      - A comment at the top of the file.
      - Declarations for input and output variables.
      - Input constraints based on the provided input domain.
      - Output constraints encoding the conditions for a property counter-example.

    Parameters:
      filename (str): The name of the file to write the vnnlib specification to.
      initial_comment (str): A comment to include at the top of the vnnlib file.
      input_domain (torch.Tensor): A tensor representing the input domain, i.e. lower und upper bounds per input, with shape (n, 2), where n is the number of input variables.
      ground_truth (int): The index of the ground truth class.
      n_classes (int, optional): The number of output classes. Default is 10.
    """
    
    with open(filename, "w") as f:
        f.write(f"; {initial_comment}\n")

        # Declare input variables.
        f.write("\n")
        linearized_domain = input_domain.view(-1, 2)
        for i in range(linearized_domain.shape[0]):
            f.write(f"(declare-const X_{i} Real)\n")
        f.write("\n")

        # Declare output variables.
        for i in range(n_classes):
            f.write(f"(declare-const Y_{i} Real)\n")
        f.write("\n")

        # Define input constraints.
        f.write(f"; Input constraints:\n")
        for i in range(linearized_domain.shape[0]):
            f.write(f"(assert (<= X_{i} {linearized_domain[i, 1]}))\n")  # UB
            f.write(f"(assert (>= X_{i} {linearized_domain[i, 0]}))\n")  # LB
            f.write("\n")
        f.write("\n")

        # Define output constraints, providing an unnecessary "and" to ease parsing in vnn-comp-21.
        f.write(f"; Output constraints (encoding the conditions for a property counter-example):\n")
        f.write(f"(assert (or\n")
        for i in range(n_classes):
            if i != ground_truth:
                f.write(f"\t(and (<= Y_{ground_truth} Y_{i}))\n")
        f.write(f"))\n")
        f.write("\n")


def instances_to_vnnlib(indices, data, vnnlib_path, experiment_name, eps, eps_temp, data_min, data_max, no_classes):
    """
    Converts a set of inputs and an epsilon value into VNN-LIB format files for adversarial robustness verification.
    
    Args:
      indices (list of int): List of indices of the data instances to be converted.
      data (torch.utils.data.Dataset): Dataset containing the data instances.
      vnnlib_path (str): Path where the VNN-LIB files will be saved.
      experiment_name (str): Name of the experiment for documentation purposes.
      eps (float): Epsilon value for the adversarial robustness property.
      eps_temp (float): Temporary epsilon value used for domain calculation.
      data_min (float): Minimum value for data normalization/clamping.
      data_max (float): Maximum value for data normalization/clamping.
      no_classes (int): Number of classes in the classification task.
    
    Returns:
      (list of str): List of file paths to the generated VNN-LIB files.
    """
    vnnlib_list_test = []
    for idx in indices:
        x, ground_truth = data[idx]
        ground_truth = ground_truth.numpy()
        print(f'idx_{idx}_eps_{eps}')
        # Record the results: vnn-lib specification.
        filename = vnnlib_path + f"idx_{idx}-eps{eps}.vnnlib"
        comment = f"Adversarial robustness property for {experiment_name}. l_inf radius: {eps}, " \
                f"Test Image {idx}."
        comment = ' '.join(comment.splitlines()).strip()
        # ground_truth = np.argmax(ground_truth)
        domain = torch.stack(
            [(x - eps_temp).clamp(data_min, data_max),
            (x + eps_temp).clamp(data_min, data_max)], dim=-1)
        write_adversarial_robustness_vnnlib(filename, comment, domain, ground_truth, n_classes=no_classes)
        vnnlib_list_test.append(filename)
    
    return vnnlib_list_test