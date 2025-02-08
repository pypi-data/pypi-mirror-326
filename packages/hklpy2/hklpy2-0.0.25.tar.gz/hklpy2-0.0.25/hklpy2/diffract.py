"""
Base class for all diffractometers

.. autosummary::

    ~DiffractometerBase
    ~pick_first_item
"""

import logging

from ophyd import Component as Cpt
from ophyd import PseudoPositioner
from ophyd.pseudopos import pseudo_position_argument
from ophyd.pseudopos import real_position_argument
from ophyd.signal import AttributeSignal

from .operations.misc import roundoff
from .operations.reflection import Reflection
from .operations.sample import Sample
from .ops import Operations
from .wavelength_support import DEFAULT_WAVELENGTH
from .wavelength_support import MonochromaticXrayWavelength

__all__ = ["DiffractometerBase"]
logger = logging.getLogger(__name__)

DEFAULT_PHOTON_ENERGY_KEV = 8.0


def pick_first_item(now: tuple, solutions: list):
    """
    Choose first item from list.

    Used by '.forward()' method to pick the first solution
    from a list of possible solutions.

    User can provide an alternative function and assign to diffractometer's
    :meth:`~hklpy2.diffract.DiffractometerBase._forward_solution` method.

    .. rubric:: Parameters

    * ``now`` (*tuple*) : Current position.
    * ``solutions`` (*[tuple]*) : List of positions.
    """
    return solutions[0]


class DiffractometerBase(PseudoPositioner):
    """
    Base class for all diffractometers.

    .. rubric:: Parameters

    *   ``solver`` (*str*) : Name of |solver| library.
        (default: unspecified)
    *   ``geometry``: (*str*) : Name of |solver| geometry.
        (default: unspecified)
    *   ``solver_kwargs`` (*dict*) : Any additional keyword arguments needed
        by |solver| library. (default: empty)
    *   ``pseudos`` ([str]) : List of diffractometer axis names to be used
        as pseudo axes. (default: unspecified)
    *   ``reals`` ([str]) : List of diffractometer axis names to be used as
        real axes. (default: unspecified)

    .. rubric:: (ophyd) Components

    .. rubric :: (ophyd) Attribute Components

    .. autosummary::

        ~configuration
        ~geometry
        ~solver
        ~wavelength

    .. rubric:: Python Methods

    .. autosummary::

        ~add_reflection
        ~add_sample
        ~auto_assign_axes
        ~forward
        ~inverse
        ~wh

    .. rubric:: Python Properties

    .. autosummary::
        ~pseudo_axis_names
        ~real_axis_names
        ~sample
        ~samples
        ~solver_name
    """

    # These two attributes are used by the PseudoPositioner class.
    # _pseudo = []  # List of pseudo-space objects.
    # _real = []  # List of real-space objects.
    # This code does NOT redefine them.

    configuration = Cpt(
        AttributeSignal,
        attr="_configuration",
        doc="Diffractometer configuration details (including orientation).",
        write_access=True,
        kind="config",
    )
    """Diffractometer configuration details."""

    geometry = Cpt(
        AttributeSignal,
        attr="operator.geometry",
        doc="Name of backend |solver| geometry.",
        write_access=False,
        kind="config",
    )
    """Name of backend |solver| geometry."""

    solver = Cpt(
        AttributeSignal,
        attr="solver_name",
        doc="Name of backend |solver| (library).",
        write_access=False,
        kind="config",
    )
    """Name of backend |solver| (library)."""

    wavelength = Cpt(
        AttributeSignal,
        attr="_wavelength.wavelength",
        doc="Wavelength of incident radiation.",
        write_access=True,
        kind="config",
    )
    """Wavelength of incident radiation."""

    def __init__(
        self,
        prefix: str = "",
        *,
        solver: str = None,
        geometry: str = None,
        solver_kwargs: dict = {},
        pseudos: list[str] = None,
        reals: list[str] = None,
        **kwargs,
    ):
        self._backend = None
        self._forward_solution = pick_first_item
        self._wavelength = MonochromaticXrayWavelength(DEFAULT_WAVELENGTH)

        self.operator = Operations(self)

        super().__init__(prefix, **kwargs)

        if isinstance(solver, str) and isinstance(geometry, str):
            self.operator.set_solver(solver, geometry, **solver_kwargs)

        self.operator.assign_axes(pseudos, reals)

    def add_reflection(
        self,
        pseudos,
        reals=None,
        wavelength=None,
        name=None,
        replace: bool = False,
    ) -> Reflection:
        """
        Add a new reflection with this geometry to the selected sample.

        .. rubric:: Parameters

        * ``pseudos`` (various): pseudo-space axes and values.
        * ``reals`` (various): dictionary of real-space axes and values.
        * ``wavelength`` (float): Wavelength of incident radiation.
          If ``None``, diffractometer's current wavelength will be assigned.
        * ``name`` (str): Reference name for this reflection.
          If ``None``, a random name will be assigned.
        * ``replace`` (bool): If ``True``, replace existing reflection of
          this name.  (default: ``False``)
        """
        return self.operator.add_reflection(
            pseudos, reals, wavelength or self.wavelength.get(), name, replace
        )

    def add_sample(
        self,
        name: str,
        a: float,
        b: float = None,
        c: float = None,
        alpha: float = 90.0,  # degrees
        beta: float = None,  # degrees
        gamma: float = None,  # degrees
        digits: int = 4,
        replace: bool = False,
    ) -> Sample:
        """Add a new sample."""
        return self.operator.add_sample(
            name,
            a,
            b,
            c,
            alpha,
            beta,
            gamma,
            digits,
            replace,
        )

    def auto_assign_axes(self):
        """
        Automatically assign diffractometer axes to this solver.

        .. seealso:: :meth:`hklpy2.ops.Operations.auto_assign_axes`

        A |solver| geometry specifies expected pseudo, real, and extra axes
        for its ``.forward()`` and ``.inverse()`` coordinate transformations.

        This method assigns this diffractometer's:

        *   first PseudoSingle axes
            to the pseudo axes expected by the selected |solver|.
        *   first Positioner axes (or subclass,
            such as EpicsMotor or SoftPositioner) to the real axes expected
            by the selected |solver|.
        *   any remaining PseudoSingle and Positioner axes to the
            extra axes expected by the selected |solver|.

        Any diffractometer axes not expected by the |solver| will
        not be assigned.
        """
        self.operator.auto_assign_axes()

    @property
    def _configuration(self) -> dict:
        """Diffractometer configuration (orientation)."""
        return self.operator._asdict()

    @_configuration.setter
    def _configuration(self, config: dict) -> dict:
        """
        Diffractometer configuration (orientation).

        PARAMETERS

        config: dict
            Dictionary of diffractometer configuration, geometry, constraints,
            samples, reflections, orientations, solver, ...
        """
        return self.operator._fromdict(config)

    @pseudo_position_argument
    def forward(self, pseudos: dict, wavelength: float = None) -> tuple:
        """Compute real-space coordinates from pseudos (hkl -> angles)."""
        logger.debug("forward: pseudos=%r", pseudos)
        solutions = self.operator.forward(pseudos, wavelength=wavelength)
        return self._forward_solution(self.real_position, solutions)

    @real_position_argument
    def inverse(self, reals: dict, wavelength: float = None) -> tuple:
        """Compute pseudo-space coordinates from reals (angles -> hkl)."""
        logger.debug("inverse: reals=%r", reals)
        pos = self.operator.inverse(reals, wavelength=wavelength)
        return self.PseudoPosition(**pos)  # as created by namedtuple

    # ---- get/set properties

    @property
    def pseudo_axis_names(self):
        """
        Names of all the pseudo axes, in order of appearance.

        Example::

            >>> fourc.pseudo_axis_names
            ['h', 'k', 'l']
        """
        return [o.attr_name for o in self.pseudo_positioners]

    @property
    def real_axis_names(self):
        """
        Names of all the real axes, in order of appearance.

        Example::

            >>> fourc.real_axis_names
            ['omega', 'chi, 'phi', 'tth']
        """
        return [o.attr_name for o in self.real_positioners]

    @property
    def samples(self):
        """Dictionary of samples."""
        if self.operator is None:
            return {}
        return self.operator.samples

    @property
    def sample(self):
        """Current sample object."""
        if self.operator is None:
            return None
        return self.operator.sample

    @sample.setter
    def sample(self, value: str) -> None:
        self.operator.sample = value

    @property
    def solver_name(self):
        """Backend |solver| library name."""
        if self.operator is not None and self.operator.solver is not None:
            return self.operator.solver.name
        return ""

    def wh(self, digits=4, full=False):
        """Concise report of the current diffractometer positions."""

        def wh_round(label, value):
            return f"{label}={roundoff(value, digits)}"

        def print_axes(names):
            print(" ".join([wh_round(nm, getattr(self, nm).position) for nm in names]))

        if full:
            print(f"diffractometer={self.name!r}")
            print(f"{self.operator.solver}")
            print(f"{self.sample!r}")
            print(f"U={self.operator.solver.U}")
            print(f"UB={self.operator.solver.UB}")
            for v in self.operator.sample.reflections.values():
                print(f"{v}")
            for v in self.operator.constraints.values():
                print(f"constraint: {v}")

        print_axes(self.pseudo_axis_names)
        print(f"wavelength={self.wavelength.get()}")
        print_axes(self.real_axis_names)

        extras = self.operator.solver.extras
        if len(extras) > 0:
            print(" ".join([wh_round(k, v) for k, v in extras.items()]))
