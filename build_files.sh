echo "Python version:"
python3.9 --version
echo "Pip version:"
python3.9 -m pip --version
echo "Installing requirements:"
python3.9 -m pip install -r requirements.txt
echo "Collecting static files:"
python3.9 manage.py collectstatic --noinput --clear
