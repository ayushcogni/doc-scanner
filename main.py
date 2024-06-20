from app import create_app
from app.utils import monitor_and_process_files

app = create_app()

if __name__ == '__main__':
    monitor_and_process_files()
    app.run(debug=True)
