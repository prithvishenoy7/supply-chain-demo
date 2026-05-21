FROM python:3.12-slim
WORKDIR /app
COPY main.py .
RUN useradd -u 1000 -m appuser && chown -R appuser:appuser /app
USER appuser
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080')" || exit 1
EXPOSE 8080
CMD ["python", "-u", "main.py"]
