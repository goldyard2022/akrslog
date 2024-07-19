from streamlit.web import bootstrap
from streamlit import config as _config


def main():
    _config.set_option("server.headless", False)
    _config.set_option("server.port", 8501)
    bootstrap.run(
        main_script_path="akrs_log/app.py",
        is_hello=False,
        args=[],
        flag_options={},
    )

if __name__ == "__main__":
    main();