from typing import Any, Callable, List, Optional
from mesa import Agent


class ChordAgent(Agent):
    """
    Agent representing a chord in the Schelling segregation model.

    Attributes:
        unique_id: Unique identifier for the agent.
        model: Reference to the model instance.
        chord_name: Name of the chord held by the agent.
        chord_type: Type of chord (e.g., major, minor).
    """

    def __init__(
        self,
        unique_id: int,
        model: Any = None,
        chord_type: str = "major",
    ) -> None:
        """
        Initialize the ChordAgent.

        Args:
            unique_id: Unique identifier for the agent.
            model: Reference to the model instance. May be ``None`` when the agent
                is constructed standalone for unit-testing the pure satisfaction
                logic — in that case we skip Mesa's ``Agent.__init__`` (which would
                call ``model.register_agent(self)`` and crash on ``None``).
            chord_type: Type of chord.
        """
        if model is not None:
            super().__init__(model)
        self.unique_id = unique_id
        self.model = model
        self.chord_name: Optional[str] = None
        self.chord_type = chord_type

    def satisfaction(
        self, neighbors: List[str], metric: Callable, tolerance: float
    ) -> float:
        """
        Calculate the fraction of occupied neighbors within tolerance.

        Args:
            neighbors: List of chord names for occupied neighboring slots.
            metric: Callable that computes distance between two chord names.
            tolerance: Maximum acceptable distance.

        Returns:
            Fraction of neighbors within tolerance. Vacuously 1.0 if no neighbors.
        """
        if not neighbors:
            return 1.0
        satisfied_count = sum(
            1 for n in neighbors if metric(self.chord_name, n) <= tolerance
        )
        return satisfied_count / len(neighbors)

    def is_satisfied(
        self,
        neighbors: List[str],
        metric: Callable,
        tolerance: float,
        happiness: float,
    ) -> bool:
        """
        Determine if the agent is satisfied with its current position.

        Args:
            neighbors: List of chord names for occupied neighboring slots.
            metric: Callable that computes distance between two chord names.
            tolerance: Maximum acceptable distance.
            happiness: Satisfaction threshold.

        Returns:
            True if satisfaction fraction >= happiness, False otherwise.
        """
        return self.satisfaction(neighbors, metric, tolerance) >= happiness

    def step(self) -> None:
        """Execute one step of the agent's behavior."""
        pass

    def get_agent_data(self) -> dict:
        """Return agent-level data for reporting."""
        return {}
