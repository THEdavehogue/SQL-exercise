psql -c "CREATE DATABASE sqlpractice09;"
echo "Verifying python dependencies . . . "
conda install pandas
conda install sqlalchemy
python setup_db.py
psql -U postgres sqlpractice09
