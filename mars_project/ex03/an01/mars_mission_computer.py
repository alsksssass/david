import DummySensor


def main():
    ds = DummySensor.DummySensor()

    ds.set_env()

    print(ds.get_env())


if __name__ == "__main__":
    main()
