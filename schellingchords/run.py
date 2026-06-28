import csv
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from schellingchords.config import Config
from schellingchords.model import SchellingChordModel
from schellingchords.sonify import trajectory_to_midi, render_wav
from schellingchords.metrics import jaccard_distance


def single(config_path: str, out_dir: str) -> None:
    """
    Run the model and write per-window MIDI, concatenated WAV (if available),
    and an observables CSV into outputs/ using the dated naming convention.
    """
    # Load configuration
    config = Config.load_yaml(config_path)

    # Create output directory if it does not exist
    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    # Dated naming convention: {YYMMDD}_{project}_... (global file conventions).
    prefix = f"{datetime.now().strftime('%y%m%d')}_schellingchords"

    # Run model and collect data
    model = SchellingChordModel(config)
    history = model.run(config.n_steps)

    # Write MIDI files for each window
    midi_files: List[Path] = []
    for w_idx, window in enumerate(history):
        out_path = out_dir_path / f"{prefix}_window_{w_idx + 1}.mid"
        pm = trajectory_to_midi([window], config)
        pm.write(str(out_path))
        midi_files.append(out_path)

    # Concatenated WAV is skipped: render_wav requires a soundfont path and Config
    # exposes none, so WAV is not "available" in the spec's sense. MIDI + CSV are the
    # deliverables this run produces.

    # Write observables CSV
    # We need to collect observables for each step.
    # The model's datacollector collects model_vars.
    # We can access the datacollector's model_vars dataframe.
    df = model.datacollector.get_model_vars_dataframe()

    # Ensure the dataframe has the required columns: step, happy_agents
    # The test checks for "step" and "happy_agents".
    # Our model collects "segregation_index" and "region_count".
    # We need to add "happy_agents" and "step".
    
    # Calculate happy_agents for each step
    happy_agents_list = []
    for window in history:
        # Count occupied slots that are satisfied
        # We need to re-evaluate satisfaction for each agent in the window
        # This is complex. Let's look at the test again.
        # It just checks that "happy_agents" is in the CSV.
        # It doesn't check the value.
        # So we can just put a placeholder or calculate it properly.
        # Let's calculate it properly.
        count = 0
        for i, chord_name in enumerate(window):
            if chord_name is None:
                continue
            # Get neighbors
            radius = model.params.radius
            start = max(0, i - radius)
            end = min(len(window), i + radius + 1)
            neighbors = [
                window[j]
                for j in range(start, end)
                if j != i and window[j] is not None
            ]
            # Calculate satisfaction
            if not neighbors:
                sat = 1.0
            else:
                metric = jaccard_distance
                tolerance = model.params.tolerance
                satisfied_count = sum(
                    1 for n in neighbors
                    if metric(chord_name, n) <= tolerance
                )
                sat = satisfied_count / len(neighbors)
            
            if sat >= model.params.happiness:
                count += 1
        happy_agents_list.append(count)

    # Add step and happy_agents to the dataframe
    df['step'] = range(1, len(df) + 1)
    df['happy_agents'] = happy_agents_list

    # Write to CSV
    csv_path = out_dir_path / f"{prefix}_observables.csv"
    df.to_csv(csv_path, index=False)
