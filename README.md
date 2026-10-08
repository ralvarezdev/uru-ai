# uru-ai

**Note:** This repository is archived and read-only.

Projects and practices from the Artificial Intelligence college course (URU), in Python.

## Contents

- **`emotions-classifier`** — emotion image classifier on a YOLO classification model (`yolo11n-cls.pt`, 100 epochs at image size 48, trained in `notebooks/train.ipynb`). `src/` has dataset tooling and a Streamlit inference UI (`test.py`).
- **`trash-classifier`** — same pipeline on the TrashNet dataset: resize to 256x256, 10 augmented versions per image, split, training in Google Colab with Ultralytics, Streamlit testing. Its own `README.md` (in Spanish) documents the steps.
- **`random-projects/qr-code`** — Tkinter GUI that scans a QR code from the webcam (OpenCV + pyzbar) and checks whether it starts with `https`.
- **`random-projects/rpa`** — reads `data/sales.xlsx` with pandas, builds a summary and PDF report, uploads it to GoFile.io and sends a Twilio message. `proxy/server.py` is a small FastAPI proxy for GoFile downloads.

Datasets and trained weights are not included.

## Running

Each sub-project has its own `requirements.txt`; some are UTF-16 encoded (Windows), so convert them if `pip` fails.

```bash
cd emotions-classifier        # or trash-classifier
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/test.py     # needs trained weights at the path set in src/files.py
```

`server.bat` does the same on Windows, and `config.toml` sets `maxUploadSize = 10`.

For `rpa`, copy `.env.example` to `.env` and set `TWILIO_ACCOUNT_SSID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_PHONE_NUMBER`, `TWILIO_TO_PHONE_NUMBER` and `PROXY_SERVER_URL`, then run `python main.py`.

## License

GNU General Public License v3.0 (see `LICENSE`).
