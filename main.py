import uvicorn

import config.config
from app.сore import App


def main():
    cfg = config.config.Configuration()
    uvicorn.run(App(cfg).app, host=cfg.host, port=int(cfg.port))
    # no ssl required so no cert args in uvicorn.run()


if __name__ == "__main__":
    main()
