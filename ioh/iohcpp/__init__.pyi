from typing import Any, ClassVar

Maximization: OptimizationType
Minimization: OptimizationType

class IntegerConstraint:
    def __init__(self, *args, **kwargs) -> None: ...
    def check(self, *args, **kwargs) -> Any: ...
    @property
    def lb(self) -> Any: ...
    @property
    def ub(self) -> Any: ...

class IntegerSolution:
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def x(self) -> Any: ...
    @property
    def y(self) -> Any: ...

class IntegerState:
    def __init__(self, arg0: IntegerSolution) -> None: ...
    @property
    def current(self) -> IntegerSolution: ...
    @property
    def current_best(self) -> IntegerSolution: ...
    @property
    def current_best_internal(self) -> IntegerSolution: ...
    @property
    def current_internal(self) -> IntegerSolution: ...
    @property
    def evaluations(self) -> int: ...
    @property
    def optimum_found(self) -> bool: ...

class LogInfo:
    def __init__(self, arg0: int, arg1: float, arg2: float, arg3: float, arg4: RealSolution, arg5: RealSolution) -> None: ...
    @property
    def current(self) -> RealSolution: ...
    @property
    def evaluations(self) -> int: ...
    @property
    def objective(self) -> RealSolution: ...
    @property
    def transformed_y(self) -> float: ...
    @property
    def transformed_y_best(self) -> float: ...
    @property
    def y_best(self) -> float: ...

class MetaData:
    def __init__(self, arg0: int, arg1: int, arg2: str, arg3: int, arg4: OptimizationType) -> None: ...
    @property
    def instance(self) -> int: ...
    @property
    def n_variables(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def optimization_type(self) -> OptimizationType: ...
    @property
    def problem_id(self) -> int: ...

class OptimizationType:
    __doc__: ClassVar[str] = ...  # read-only
    __members__: ClassVar[dict] = ...  # read-only
    Maximization: ClassVar[OptimizationType] = ...
    Minimization: ClassVar[OptimizationType] = ...
    __entries: ClassVar[dict] = ...
    def __init__(self, value: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class RealConstraint:
    def __init__(self, *args, **kwargs) -> None: ...
    def check(self, *args, **kwargs) -> Any: ...
    @property
    def lb(self) -> Any: ...
    @property
    def ub(self) -> Any: ...

class RealSolution:
    def __init__(self, *args, **kwargs) -> None: ...
    @property
    def x(self) -> Any: ...
    @property
    def y(self) -> Any: ...

class RealState:
    def __init__(self, arg0: RealSolution) -> None: ...
    @property
    def current(self) -> RealSolution: ...
    @property
    def current_best(self) -> RealSolution: ...
    @property
    def current_best_internal(self) -> RealSolution: ...
    @property
    def current_internal(self) -> RealSolution: ...
    @property
    def evaluations(self) -> int: ...
    @property
    def optimum_found(self) -> bool: ...
