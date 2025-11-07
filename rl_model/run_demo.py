from .sample_sequences import get_case
from .train import train


def main():
    case = get_case()
    print(f"🌱 Demo case: {case.title}")
    print(
        f"   Start from {case.initial_name} ({len(case.initial_sequence)} bp) "
        f"and push toward {case.target_name}."
    )
    _, env, rewards = train(episodes=120, max_edits=8, case_id=case.case_id)
    print("\nDemo finished.")
    print(f"Final sequence: {env.sequence}")
    print(f"Reward trace (last 5): {[round(r, 3) for r in rewards[-5:]]}")


if __name__ == "__main__":
    main()
