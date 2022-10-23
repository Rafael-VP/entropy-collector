import cv2
import hashlib
import time
import random
import textwrap
import numpy as np


def simple_capture(seeds):
    cap = cv2.VideoCapture(0)
    print("Starting entropy collector...")

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            readable_hash = hashlib.sha256(image).hexdigest()
            print(readable_hash)
            seeds.append(readable_hash)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Stopping entropy collection.")
                break

        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    return seeds


def max_brightness(frame, value=255):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    final_hsv = cv2.merge((h, s, v))
    frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return frame


def capture(seeds):
    cap = cv2.VideoCapture(0)
    last_frame = None
    start = time.time()

    while cap.isOpened():
        ret, curr_frame = cap.read()

        if not ret:
            break

        if last_frame is not None:
            frame = curr_frame

            # 1. diff two frames
            frame = cv2.absdiff(last_frame, curr_frame)

            # 2. maximize the luminance
            frame = max_brightness(frame)

            # 3. convert to black-and-white
            frame = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 127,
                                  255, cv2.THRESH_BINARY)[1]

            shake = hashlib.shake_128()
            shake.update(bytes(frame))

            data = textwrap.wrap(str(int(shake.hexdigest(8192), 32)), 8)

            for i in data:
                seeds.append(int(i))
                # fifo.write(i+"\n")
                # fifo.flush()

            cv2.imshow('webcam noise', frame)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

        last_frame = curr_frame

    end = time.time()
    print(f"Runtime: {end - start}\nSeeds: {len(seeds)}\nSeeds/s: {len(seeds)/(end-start)}")
    cap.release()
    cv2.destroyAllWindows()

    return seeds


def coinflip(seeds):
    sides = ["Heads", "Tails"]
    random.seed(seeds[0])
    seeds.pop(0)
    result = random.choice(sides)

    return result, seeds


def roll(seeds, roll):
    result = ""

    for i in range(0, roll[0]):
        # random.seed(seeds[0])
        number = 1 + seeds[0] % roll[1]
        seeds.pop(0)
        # number = random.randint(0, roll[1])
        result += f", {number}"

    return result[2:], seeds


def main():
    seeds = []

    while True:
        command = input("> ")

        if command == "exit":
            break

        elif command == "help":
            print("List of available commands:\nhelp, entropy, collect, coinflip, exit.")

        elif command == "entropy":
            print(f"Available entropy: {len(seeds)}")

        elif command == "collect":
            seeds = capture(seeds)
            print(f"Entropy collected successfully. Available entropy: {len(seeds)}")

        elif command == "coinflip":
            if len(seeds) == 0:
                print("At least one seed is required for a coin flip.")

            else:
                result, seeds = coinflip(seeds)
                print(result)

        elif command[:4] == "roll":
            dice = command[5:].split("d")
            dice[0] = int(dice[0])
            dice[1] = int(dice[1])
            required = dice[0]

            if required > len(seeds):
                print(f"Required entropy: {required}.\nAvailable entropy: {len(seeds)}.")

            else:
                result, seeds = roll(seeds, dice)
                print(result)

        elif command[:11] == "montecarlo ":
            from montecarlo import monte_carlo
            seeds = monte_carlo(seeds, command[11:])

        elif command[:14] == "montecarlotrig":
            from montecarlo import monte_carlo_trig
            seeds = monte_carlo_trig(seeds, command[15:])

        elif command == "montecarlopi":
            from montecarlo import monte_carlo_pi
            result, seeds = monte_carlo_pi(seeds)
            print(f"Pi estimate: {result}")

        elif command[:8] == "simulate":
            amount, rtype = command[9:].split(" ")
            from simulation import simulate
            seeds = simulate(seeds, int(amount), int(rtype))


if __name__ == "__main__":
    main()
