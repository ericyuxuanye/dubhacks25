from .train import train


def main():
    print("Starting a short demo training run (toy).")
    agent, env = train(episodes=20, seq_len=20, max_edits=8)
    print("Demo finished. Final sequence:")
    env.render()


if __name__ == "__main__":
    main()
