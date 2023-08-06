import numpy as np
import warnings

need_state_equation_function_msg = ("if dim_state > 0, DynamicalSystem must"
                                    + " have a state_equation_function")

need_output_equation_function_msg = ("if dim_state == 0, DynamicalSystem must"
                                     + " have an output_equation_function")

zero_dim_output_msg = "A DynamicalSystem must provide an output"


def full_state_output(*args):
    """
    A drop-in ``output_equation_function`` for stateful systems that provide
    output the full state directly.
    """
    return np.r_[args][1:]


class DynamicalSystem(object):
    """
    A dynamical system which models systems of the form::

        xdot(t) = state_equation_function(t,x,u)
        y(t) = output_equation_function(t,x)

    or::

        y(t) = output_equation_function(t,u)

    These could also represent discrete-time systems, in which case xdot(t)
    represents x[k+1].

    This can also model discontinuous systems. Discontinuities must occur on
    zero-crossings of the ``event_equation_function``, which take the same
    arguments as ``output_equation_function``, depending on ``dim_state``.
    At the zero-crossing, ``update_equation_function`` is called with the same
    arguments. If ``dim_state`` > 0, the return value of
    ``update_equation_function`` is used as the state of the system immediately
    after the discontinuity.
    """
    def __init__(self, state_equation_function=None,
                 output_equation_function=None, event_equation_function=None,
                 update_equation_function=None, dim_state=0, dim_input=0,
                 dim_output=0, dt=0, initial_condition=None):
        """
        Parameters
        ----------
        state_equation_function : callable, optional
            The derivative (or update equation) of the system state. Not needed
            if ``dim_state`` is zero.
        output_equation_function : callable, optional
            The output equation of the system. A system must have an
            ``output_equation_function``. If not set, uses full state output.
        event_equation_function : callable, optional
            The function whose output determines when discontinuities occur.
        update_equation_function : callable, optional
            The function called when a discontinuity occurs.
        dim_state : int, optional
            Dimension of the system state. Optional, defaults to 0.
        dim_input : int, optional
            Dimension of the system input. Optional, defaults to 0.
        dim_output : int, optional
            Dimension of the system output. Optional, defaults to dim_state.
        dt : float, optional
            Sample rate of the system. Optional, defaults to 0 representing a
            continuous time system.
        initial_condition : array_like of numerical values, optional
            Array or Matrix used as the initial condition of the system.
            Defaults to zeros of the same dimension as the state.
        """
        self.dim_state = dim_state
        self.dim_input = dim_input
        self.dim_output = dim_output or dim_state

        self.state_equation_function = state_equation_function

        self.output_equation_function = (
            full_state_output
            if output_equation_function is None and self.dim_state > 0
            else output_equation_function
        )

        self.event_equation_function = event_equation_function
        self.update_equation_function = update_equation_function
        self.initial_condition = initial_condition
        self.dt = dt

        self.validate()

    @property
    def initial_condition(self):
        return (self._initial_condition
                if self._initial_condition is not None
                else np.zeros(self.dim_state))

    @initial_condition.setter
    def initial_condition(self, initial_condition):
        self._initial_condition = initial_condition

    def prepare_to_integrate(self):
        return

    def validate(self):
        if self.dim_output == 0:
            raise ValueError(zero_dim_output_msg)

        if (self.dim_state > 0
                and getattr(self, 'state_equation_function', None) is None):
            raise ValueError(need_state_equation_function_msg)

        if (self.dim_state == 0
                and getattr(self, 'output_equation_function', None) is None):
            raise ValueError(need_output_equation_function_msg)


def SystemFromCallable(incallable, dim_input, dim_output, dt=0):
    """
    Construct a memoryless system from a callable.

    Parameters
    ----------
    incallable : callable
        Function to use as the output_equation_function. Should have signature
        (t, u) if dim_input > 0 or (t) if dim_input = 0.
    dim_input : int
        Dimension of input.
    dim_output : int
        Dimension of output.
    """
    system = DynamicalSystem(output_equation_function=incallable,
                             dim_input=dim_input, dim_output=dim_output, dt=dt)
    return system


class SwitchedSystem(DynamicalSystem):
    """
    Provides a useful pattern for discontinuous systems where the state and
    output equations change depending on the value of a function of the state
    and/or input (``event_variable_equation_function``). Most of the usefulness
    comes from constructing the ``event_equation_function`` with a Bernstein
    basis polynomial with roots at the boundaries. This class also provides
    logic for outputting the correct state and output equation based on the
    ``event_variable_equation_function`` value.
    """
    def __init__(self, state_equations_functions=None,
                 output_equations_functions=None,
                 event_variable_equation_function=None, event_bounds=None,
                 state_update_equation_function=None, dim_state=0, dim_input=0,
                 dim_output=0, dt=0, initial_condition=None):
        """
        Parameters
        ----------
        state_equation_functions : array_like of callables, optional
            The derivative (or update equation) of the system state. Not needed
            if ``dim_state`` is zero. The array indexes the
            event-state and should be one more than the number of event bounds.
            This should also be indexed to match the boundaries (i.e., the
            first function is used when the event variable is below the first
            event_bounds value). If only one callable is provided, the callable
            is used in each condition.
        output_equation_functions : array_like of callables, optional
            The output equation of the system. A system must have an
            ``output_equation_function``. If not set, uses full state output.
            The array indexes the event-state and should be one more than the
            number of event bounds. This should also be indexed to match the
            boundaries (i.e., the first function is used when the event
            variable is below the first event_bounds value). If only one
            callable is provided, the callable is used in each condition.
        event_variable_equation_function : callable
            When the output of this function crosses the values in
            ``event_bounds``, a discontuity event occurs.
        event_bounds : array_like of floats
            Defines the boundary points the trigger discontinuity events based
            on the output of ``event_variable_equation_function``.
        state_update_equation_function : callable, optional
            When an event occurs, the state update equation function is called
            to determine the state update. If not set, uses full state output,
            so the state is not changed upon a zero-crossing of the event
            variable function.
        dim_state : int, optional
            Dimension of the system state. Optional, defaults to 0.
        dim_input : int, optional
            Dimension of the system input. Optional, defaults to 0.
        dim_output : int, optional
            Dimension of the system output. Optional, defaults to dim_state.
        dt : float, optional
            Sample rate of the system. Optional, defaults to 0 representing a
            continuous time system.
        """
        self.dim_state = dim_state
        self.dim_input = dim_input
        self.dim_output = dim_output or dim_state
        self.event_bounds = event_bounds

        self.state_equations_functions = np.empty(self.n_conditions,
                                                  dtype=object)
        self.state_equations_functions[:] = state_equations_functions

        self.output_equations_functions = np.empty(self.n_conditions,
                                                   dtype=object)
        self.output_equations_functions[:] = (
            full_state_output
            if output_equations_functions is None and self.dim_state > 0
            else output_equations_functions
        )

        self.event_variable_equation_function = \
            event_variable_equation_function

        self.state_update_equation_function = (
            state_update_equation_function or
            full_state_output
        )

        self.initial_condition = initial_condition or np.zeros(dim_state)
        self.dt = dt

        self.validate()

    def validate(self):
        super().validate()

        if (self.dim_state > 0
                and np.any(np.equal(self.state_equations_functions, None))):
            raise ValueError(need_state_equation_function_msg)

        if (self.dim_state == 0
                and np.any(np.equal(self.output_equations_functions, None))):
            raise ValueError(need_output_equation_function_msg)

        if self.event_variable_equation_function is None:
            raise ValueError("A SwitchedSystem requires " +
                             "event_variable_equation_function")

    @property
    def event_bounds(self):
        return self._event_bounds

    @event_bounds.setter
    def event_bounds(self, event_bounds):
        if event_bounds is None:
            raise ValueError("A SwitchedSystem requires event_bounds")
        self._event_bounds = np.array(event_bounds).reshape(1, -1)
        self.n_conditions = self._event_bounds.size + 1
        if self.n_conditions == 2:
            self.event_bounds_range = 1
        else:
            self.event_bounds_range = np.diff(self.event_bounds[0, [0, -1]])

    def output_equation_function(self, *args):
        return self.output_equations_functions[self.condition_idx](*args)

    def state_equation_function(self, *args):
        return self.state_equations_functions[self.condition_idx](*args)

    def event_equation_function(self, *args):
        event_var = self.event_variable_equation_function(*args)
        return np.prod(
            (self.event_bounds_range-self.event_bounds)*event_var -
            self.event_bounds*(self.event_bounds_range - event_var),
            axis=1
        )

    def update_equation_function(self, *args):
        event_var = self.event_variable_equation_function(*args)
        if self.condition_idx is None:
            self.condition_idx = np.where(np.all(np.r_[
                    np.c_[[[True]], event_var >= self.event_bounds],
                    np.c_[event_var <= self.event_bounds, [[True]]]
                    ], axis=0))[0][0]
        else:
            sq_dist = (event_var - self.event_bounds)**2
            crossed_root_idx = np.where(sq_dist == np.min(sq_dist))[1][0]
            if crossed_root_idx == self.condition_idx:
                self.condition_idx += 1
            elif crossed_root_idx == self.condition_idx-1:
                self.condition_idx -= 1
            else:
                warnings.warn("SwitchedSystem did not cross a neighboring " +
                              "boundary. This may indicate an integration " +
                              "error. Continuing without updating " +
                              "condition_idx", UserWarning)
        return self.state_update_equation_function(*args)

    def prepare_to_integrate(self):
        self.condition_idx = None


class LTISystem(DynamicalSystem):
    """
    A linear, time-invariant system.
    """
    def __init__(self, *args, initial_condition=None, dt=0):
        """
        Construct an LTI system with the following input formats:

        1. A, B, C matrices for systems with state::
            x' = Ax + Bu
            y = Hx
        2. A,B matrices for systems with state, assume full state output::
            x' = Ax + Bu
            y = Ix
        3. K matrix for systems without state::
            y = Kx

        The matrices should be numeric arrays of the appropriate shape.
        """
        self.dt = dt

        if len(args) not in (1, 2, 3):
            raise ValueError("LTI system expects 1, 2, or 3 args")

        # TODO: setup jacobian functions
        if len(args) == 1:
            self.K = K = args[0]
            self.dim_input = self.K.shape[1] if len(K.shape) > 1 else 1
            self.dim_output = self.K.shape[0]
            self.dim_state = 0
            self.initial_condition = np.zeros(self.dim_state)
            self.output_equation_function = lambda t, x: (K@x).reshape(-1)
            return

        if len(args) == 2:
            F, G = args
            H = np.eye(F.shape[0])

        elif len(args) == 3:
            F, G, H = args

        if len(G.shape) == 1:
            G = G.reshape(-1, 1)

        self.dim_state = F.shape[0]
        self.dim_input = G.shape[1]
        self.dim_output = H.shape[0]

        self.F = F
        self.G = G
        self.H = H

        self.initial_condition = initial_condition or np.zeros(self.dim_state)
        self.state_equation_function = lambda t, x, u: (F@x + G@u).reshape(-1)
        self.output_equation_function = lambda t, x: (H@x).reshape(-1)

        self.validate()

    def validate(self):
        super().validate()
        if self.dim_state:
            assert self.F.shape[1] == self.dim_state
            assert self.G.shape[0] == self.dim_state
            assert self.H.shape[1] == self.dim_state

    @property
    def data(self):
        if self.dim_state:
            return self.F, self.G, self.H
        else:
            return self.K
