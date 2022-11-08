[Mesh]
  type = GeneratedMesh
  dim = 2
  nx =
  ny =
  nz = 0
  xmin =
  xmax =
  ymin =
  ymax =
  elem_type = QUAD4
[]

[GlobalParams]
  # let's output all material properties for demonstration purposes
  #outputs = exodus
[]

[Variables]
  [./c]
    order = FIRST
    family = LAGRANGE
    [./InitialCondition]
      type = FunctionIC
      function = c_txt
    [../]
  [../]
  [./eta]
    order = FIRST
    family = LAGRANGE
    [./InitialCondition]
      type = FunctionIC
      function = eta_txt
    [../]
  [../]
[]

[Kernels]
  #
  # Cahn-Hilliard kernel for the concentration variable.
  # Note that we are not using an interfcae kernel on this variable, but rather
  # rely on the interface width enforced on the order parameters. This allows us
  # to use a direct solve using the CahnHilliard kernel _despite_ only using first
  # order elements.
  #
  [./c_res]
    type = CahnHilliard
    variable = c
    f_name = F_total
    args = 'eta'
  [../]
  [./time]
    type = TimeDerivative
    variable = c
  [../]

  #
  # Order parameter eta1
  #
  [./deta1dt]
    type = TimeDerivative
    variable = eta
  [../]
  [./ACBulk1]
    type = AllenCahn
    variable = eta
    args = 'c'
    mob_name = L
    f_name = F_total
  [../]
  [./ACInterface1]
    type = ACInterface
    variable = eta
    mob_name = L
    kappa_name = 'kappa_eta'
  [../]
[]

[Materials]
  [./consts]
    type = GenericConstantMaterial
    prop_names  = 'M kappa_c L kappa_eta'
    prop_values =
  [../]
  [./epmap]
    type = GenericFunctionMaterial
    block = 0
    prop_names = ep
    prop_values = ep_txt
  [../]
  [./free_energy]
  type = DerivativeParsedMaterial
  block = 0
  f_name = F
  args = 'eta c'
  constant_names = 'cross_term h'
  constant_expressions = '1
  function = 'h*((-1-eta)^2*eta^2*(1-eta)^2+c^2*(1-c)^2+cross_term*(((-1-eta)^2*(1-eta)^2)*c^2+(eta^2)*(1-c)^2))'
  enable_jit = true
  derivative_order = 2
  [../]
  [./total_free_energy]
    type = DerivativeParsedMaterial
    block = 0
    f_name = F_total
    args = 'eta c'
    material_property_names = 'ep F(eta,c)'
    function = 'F+ep*3*eta^2-ep*2*eta^3'
    enable_jit = true
    derivative_order = 2
  [../]
[]

[Functions]
  [eta_txt]
    type = PiecewiseMultilinear
    data_file = Data/etas_
  []
  [c_txt]
    type = PiecewiseMultilinear
    data_file = Data/c_
  []
	[ep_txt]
		type = PiecewiseMultilinear
		data_file = Data/ep_
	[]
[]

[Preconditioning]
  # This preconditioner makes sure the Jacobian Matrix is fully populated. Our
  # kernels compute all Jacobian matrix entries.
  # This allows us to use the Newton solver below.
  [./SMP]
    type = SMP
    full = true
  [../]
[]

[Executioner]
  type = Transient
  scheme = 'bdf2'

  # Automatic differentiation provides a _full_ Jacobian in this example
  # so we can safely use NEWTON for a fast solve
  solve_type = 'NEWTON'

  l_max_its = 15
  l_tol = 1.0e-6

  nl_max_its = 50
  nl_rel_tol = 1.0e-6
  nl_abs_tol = 1.0e-6

  start_time = 0.0
  end_time   = 5

  [./TimeStepper]
    type = SolutionTimeAdaptiveDT
    dt = 0.002
  [../]
[]

[Outputs]
  execute_on = 'timestep_end'
  exodus = true
  [./other]
    type = VTK
  [../]
[]
