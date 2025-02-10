# Gunicorn configuration file
import multiprocessing

max_requests = 1000
max_requests_jitter = 50

# log_file = "-"
# Logging settings (stdout/stderr)
accesslog = "-"  # Log access requests to stdout
errorlog = "-"   # Log errors to stderr
loglevel = "debug"  # Set to "debug" for troubleshooting

bind = "0.0.0.0:3100"

worker_class = "uvicorn.workers.UvicornWorker"
workers = (multiprocessing.cpu_count() * 2) + 1
# workers = 16

timeout = 300
graceful_timeout = 30  # Allows workers to shut down gracefully
keepalive = 5  # Keep connections open for 5 seconds
