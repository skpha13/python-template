from src.logging_config import logger


def main() -> None:
    logger.info("Hello from python-template!")

    try:
        from src.hello_world_cpp.hello_world import hello_world

        logger.info(hello_world())
    except ImportError:
        logger.warning("C++ extension not built - run: uv pip install -e .")


if __name__ == "__main__":
    main()
